"""Exercise the preview HTTP responses and change detection without a browser."""
import importlib.util
from functools import partial
from http.server import HTTPServer
from pathlib import Path
import tempfile
import threading
import unittest
from urllib.request import urlopen

spec = importlib.util.spec_from_file_location('preview', Path(__file__).resolve().parents[1] / 'scripts/preview.py')
preview = importlib.util.module_from_spec(spec)
spec.loader.exec_module(preview)


class PreviewTests(unittest.TestCase):
    def test_source_add_edit_remove_detected_but_generated_output_ignored(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'content/posts').mkdir(parents=True)
            start = preview.snapshot(root)
            post = root / 'content/posts/example.md'
            post.write_text('first', encoding='utf-8')
            added = preview.snapshot(root)
            self.assertNotEqual(start, added)
            post.write_text('longer edit', encoding='utf-8')
            self.assertNotEqual(added, preview.snapshot(root))
            post.unlink()
            (root / '_preview').mkdir()
            (root / '_preview/index.html').write_text('generated', encoding='utf-8')
            self.assertEqual(start, preview.snapshot(root))

    def test_http_refresh_script_and_version_are_preview_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            page = Path(tmp) / 'index.html'
            page.write_text('<html><body>Draft</body></html>', encoding='utf-8')
            handler = partial(preview.PreviewHandler, directory=tmp)
            with HTTPServer(('127.0.0.1', 0), handler) as server:
                server.revision = 123
                worker = threading.Thread(target=server.serve_forever, daemon=True)
                worker.start()
                try:
                    base = f'http://127.0.0.1:{server.server_port}'
                    with urlopen(base + '/') as response:
                        content = response.read().decode()
                        self.assertIn('/__preview_version', content)
                        self.assertIn('location.reload()', content)
                        self.assertEqual(response.headers['Cache-Control'], 'no-store')
                        self.assertEqual(response.headers['X-Robots-Tag'], 'noindex, nofollow')
                    with urlopen(base + '/__preview_version') as response:
                        self.assertEqual(response.read(), b'123')
                    server.revision = 456
                    with urlopen(base + '/__preview_version') as response:
                        self.assertEqual(response.read(), b'456')
                    self.assertNotIn('<script>', page.read_text(encoding='utf-8'))
                finally:
                    server.shutdown()
                    worker.join()
