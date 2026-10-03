"""Import one explicitly selected Markdown note as a draft (never an entire private vault)."""
import argparse
from datetime import date
import json
from pathlib import Path
import re
import shutil
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


def import_note(source, slug, title, platform, difficulty):
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', slug):
        raise ValueError('Slug must contain lowercase letters, numbers, and single hyphens.')
    source = source.resolve(strict=True)
    if source.suffix.lower() != '.md':
        raise ValueError('Select a Markdown (.md) file.')
    target = ROOT / 'content/posts' / f'{slug}.md'
    media_dir = ROOT / 'content/media' / slug
    if target.exists() or media_dir.exists():
        raise ValueError('This slug already exists; choose another to avoid overwriting work.')
    body = source.read_text(encoding='utf-8-sig')
    # Existing metadata belongs to the source vault, not the public article.
    body = re.sub(r'\A(?:---\r?\n.*?\r?\n---|\+\+\+\r?\n.*?\r?\n\+\+\+)\r?\n', '', body, count=1, flags=re.S)
    if re.search(r'!?\[\[', body):
        raise ValueError('Convert Obsidian wikilinks/embeds to standard Markdown links before importing.')
    assets = {}
    def image(match):
        alt, url = match.group(1), match.group(2)
        parsed = urlsplit(url)
        if parsed.scheme or parsed.netloc:
            return match.group(0)
        asset = (source.parent / unquote(parsed.path)).resolve(strict=True)
        if not asset.is_relative_to(source.parent):
            raise ValueError('Local images must be inside the selected note folder; copy them there first.')
        if asset.suffix.lower() not in ('.png', '.jpg', '.jpeg', '.webp', '.gif'):
            raise ValueError('Only PNG, JPEG, WebP, and GIF image attachments are imported.')
        if asset not in assets:
            assets[asset] = f'image-{len(assets) + 1}{asset.suffix.lower()}'
        return f'![{alt}](../media/{slug}/{assets[asset]})'
    body = re.sub(r'!\[([^\]]*)\]\(<?([^\s)>]+)>?\)', image, body)
    metadata = {
        'title': title, 'date': date.today().isoformat(), 'platform': platform,
        'difficulty': difficulty, 'tags': [], 'summary': 'Draft imported from lab notes. Edit before publication.',
        'draft': True, 'kind': 'solve', 'publication_approved': False,
    }
    header = '\n'.join(f'{key} = {json.dumps(value, ensure_ascii=False)}' for key, value in metadata.items())
    if assets:
        media_dir.mkdir(parents=True)
        for asset, name in assets.items():
            shutil.copy2(asset, media_dir / name)
    target.write_text(f'+++\n{header}\n+++\n\n{body}', encoding='utf-8')
    return target


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('--slug', required=True)
    parser.add_argument('--title', required=True)
    parser.add_argument('--platform', default='HackTheBox')
    parser.add_argument('--difficulty', default='Unspecified')
    args = parser.parse_args()
    print(import_note(args.source, args.slug, args.title, args.platform, args.difficulty))
