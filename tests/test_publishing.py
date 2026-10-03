import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


def module(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / f'{name}.py')
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


build = module('build')
importer = module('import_note')


class PublishingTests(unittest.TestCase):
    def test_html_and_unsafe_links_are_not_executable(self):
        rendered, _ = build.render_markdown('<script>alert(1)</script>\n\n[x](javascript:alert(1))')
        self.assertNotIn('<script>', rendered)
        self.assertNotIn('href="javascript:', rendered)

    def test_duplicate_heading_anchors_and_tables(self):
        rendered, toc = build.render_markdown('## Result\n\n## Result\n\n| A | B |\n|---|---|\n| 1 | 2 |')
        self.assertIn('id="section-result-2"', rendered)
        self.assertIn('href="#section-result-2"', toc)
        self.assertIn('<table>', rendered)

    def test_import_is_draft_with_portable_images(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'content/posts').mkdir(parents=True)
            note = root / 'note.md'
            note.write_text('# Test\n\n![Evidence](image.png)', encoding='utf-8')
            (root / 'image.png').write_bytes(b'example-image')
            with patch.object(importer, 'ROOT', root):
                result = importer.import_note(note, 'test-lab', 'Test lab', 'HackTheBox', 'Easy')
                post = build.read_post(result)
                self.assertTrue(post['draft'])
                self.assertFalse(post['publication_approved'])
                self.assertIn('../media/test-lab/image-1.png', post['body'])
                self.assertTrue((root / 'content/media/test-lab/image-1.png').exists())
                with self.assertRaises(ValueError):
                    importer.import_note(note, 'test-lab', 'Test', 'HackTheBox', 'Easy')

    def test_public_build_omits_drafts_and_draft_media(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for folder in ('templates', 'content/posts', 'content/media/hidden-lab', 'assets', 'css', 'scripts', 'samples'):
                (root / folder).mkdir(parents=True)
            (root / 'templates/page.html').write_text('$content', encoding='utf-8')
            for name in ('home', 'about', 'resume'):
                (root / f'content/{name}.html').write_text('$latest' if name == 'home' else '', encoding='utf-8')
            draft = (ROOT / 'content/post-template.md').read_text(encoding='utf-8')
            (root / 'content/posts/hidden-lab.md').write_text(draft, encoding='utf-8')
            (root / 'content/media/hidden-lab/private.png').write_bytes(b'private')
            with patch.object(build, 'ROOT', root):
                build.build()
                self.assertFalse((root / '_site/writeups/hidden-lab.html').exists())
                self.assertFalse((root / '_site/media/hidden-lab/private.png').exists())
                self.assertNotIn('Machine name', (root / '_site/writeups.html').read_text(encoding='utf-8'))
                build.build(preview=True)
                self.assertTrue((root / '_preview/writeups/hidden-lab.html').exists())
                self.assertTrue((root / '_preview/media/hidden-lab/private.png').exists())
                # Public builds must fail rather than accidentally publish an unreviewed solve.
                (root / 'content/posts/hidden-lab.md').write_text(draft.replace('draft = true', 'draft = false'), encoding='utf-8')
                with self.assertRaises(ValueError):
                    build.build()


if __name__ == '__main__':
    unittest.main()
