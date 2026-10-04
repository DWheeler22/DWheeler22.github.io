"""Serve a local draft preview, rebuilding and refreshing when source files change."""
import argparse
from functools import partial
from http.server import HTTPServer, SimpleHTTPRequestHandler
from io import BytesIO
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
SOURCE_FOLDERS = ('content', 'templates', 'css', 'assets', 'scripts', 'samples')


def snapshot(root=ROOT):
    result = {}
    for folder in SOURCE_FOLDERS:
        for path in (root / folder).rglob('*'):
            if path.is_file() and '__pycache__' not in path.parts:
                stat = path.stat()
                result[str(path.relative_to(root))] = (stat.st_mtime_ns, stat.st_size)
    return result


def rebuild():
    return subprocess.run([sys.executable, str(ROOT / 'scripts/build.py'), '--drafts'],
                          cwd=ROOT).returncode == 0


class PreviewHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Robots-Tag', 'noindex, nofollow')
        super().end_headers()

    def send_head(self):
        if self.path.split('?')[0] == '/__preview_version':
            payload = str(self.server.revision).encode()
            content_type = 'text/plain; charset=utf-8'
        else:
            path = Path(self.translate_path(self.path))
            if path.is_dir():
                path = path / 'index.html'
            if path.suffix != '.html' or not path.is_file():
                return super().send_head()
            # This script exists only in HTTP preview responses, never in build output.
            script = '''<script>
const previewRevision = "REVISION";
setInterval(async () => {
  try {
    const response = await fetch('/__preview_version', {cache: 'no-store'});
    if (response.ok && await response.text() !== previewRevision) location.reload();
  } catch (_) {}
}, 1000);
</script>'''.replace('REVISION', str(self.server.revision))
            payload = path.read_text(encoding='utf-8').replace('</body>', script + '</body>').encode('utf-8')
            content_type = 'text/html; charset=utf-8'
        self.send_response(200)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(payload)))
        self.end_headers()
        return BytesIO(payload)

    def log_message(self, format, *args):
        if self.path.split('?')[0] != '/__preview_version':
            super().log_message(format, *args)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=8765)
    args = parser.parse_args()
    if not rebuild():
        return 1
    handler = partial(PreviewHandler, directory=str(ROOT / '_preview'))
    with HTTPServer(('127.0.0.1', args.port), handler) as server:
        server.timeout = 0.5
        server.revision = time.time_ns()
        previous = snapshot()
        print(f'Draft preview: http://127.0.0.1:{args.port}/writeups.html', flush=True)
        print('Save a source file to rebuild and refresh. Ctrl+C stops the preview.', flush=True)
        try:
            while True:
                # One thread serializes builds and requests, avoiding reads mid-build.
                server.handle_request()
                current = snapshot()
                if current != previous:
                    previous = current
                    if rebuild():
                        server.revision = time.time_ns()
                    else:
                        print('Build failed. Fix the source and save again to retry.', flush=True)
        except KeyboardInterrupt:
            print('\nPreview stopped.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
