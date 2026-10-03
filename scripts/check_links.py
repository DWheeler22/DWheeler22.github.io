"""Check local HTML links, assets, and fragment targets in a generated site."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import sys


class Links(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.links, self.ids = [], set()
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.add(attrs['id'])
        for key in ('href', 'src'):
            if attrs.get(key):
                self.links.append(attrs[key])


def check(root):
    root = root.resolve()
    pages = {p: Links(p.read_text(encoding='utf-8')) for p in root.rglob('*.html')}
    failures = []
    for source, parsed in pages.items():
        for link in parsed.links:
            parts = urlsplit(link)
            if parts.scheme or parts.netloc:
                continue
            target = (source.parent / unquote(parts.path)).resolve() if parts.path else source
            if target.is_dir():
                target = target / 'index.html'
            if not target.is_relative_to(root) or not target.exists():
                failures.append(f'{source.relative_to(root)}: missing {link}')
            elif parts.fragment and target in pages and unquote(parts.fragment) not in pages[target].ids:
                failures.append(f'{source.relative_to(root)}: missing anchor {link}')
    return pages, failures


if __name__ == '__main__':
    pages, failures = check(Path(sys.argv[1] if len(sys.argv) > 1 else '_site'))
    print('\n'.join(failures) if failures else f'Checked {len(pages)} HTML pages: local links and anchors pass.')
    sys.exit(bool(failures))
