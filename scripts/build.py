"""Build static pages. Content stays readable without JavaScript or a web service."""
from pathlib import Path
from string import Template
from datetime import date
import argparse
import html
import math
import re
import shutil
import tomllib
from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parents[1]
MD = MarkdownIt('commonmark', {'html': False}).enable('table')


def escape(value):
    return html.escape(str(value), quote=True)


def read_post(path):
    source = path.read_text(encoding='utf-8-sig')
    parts = source.split('+++', 2)
    if len(parts) != 3 or parts[0].strip():
        raise ValueError(f'{path.name}: expected TOML metadata between +++ lines')
    meta = tomllib.loads(parts[1])
    for key in ('title', 'date', 'platform', 'difficulty', 'summary'):
        if not isinstance(meta.get(key), str) or not meta[key].strip():
            raise ValueError(f'{path.name}: {key} must be a nonempty string')
    date.fromisoformat(meta['date'])
    if not isinstance(meta.get('draft'), bool):
        raise ValueError(f'{path.name}: explicitly set draft = true or false')
    if meta.get('kind') not in ('solve', 'guide'):
        raise ValueError(f'{path.name}: kind must be solve or guide')
    status = meta.get('box_status', 'unknown')
    if status not in ('active', 'retired', 'unknown'):
        raise ValueError(f'{path.name}: box_status must be active, retired, or unknown')
    meta['box_status'] = status
    if meta.get('date_source') not in (None, 'source-created'):
        raise ValueError(f'{path.name}: unsupported date_source')
    tags = meta.get('tags', [])
    if not isinstance(tags, list) or not all(isinstance(x, str) for x in tags):
        raise ValueError(f'{path.name}: tags must be an array of strings')
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', path.stem):
        raise ValueError(f'{path.name}: use a lowercase hyphenated filename')
    meta.update(slug=path.stem, body=parts[2], tags=tags)
    meta['minutes'] = max(1, math.ceil(len(parts[2].split()) / 200))
    return meta


def read_notice(path):
    """Public metadata is separate from the private walkthrough and its spoilers."""
    meta = tomllib.loads(path.read_text(encoding='utf-8'))
    for key in ('title', 'date', 'platform', 'difficulty'):
        if not isinstance(meta.get(key), str) or not meta[key].strip():
            raise ValueError(f'{path.name}: {key} must be a nonempty string')
    date.fromisoformat(meta['date'])
    if meta.get('box_status') != 'active':
        raise ValueError(f'{path.name}: retirement notices require active status')
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', path.stem):
        raise ValueError(f'{path.name}: use a lowercase hyphenated filename')
    return dict(title=meta['title'], date=meta['date'], platform=meta['platform'],
                difficulty=meta['difficulty'], box_status='active', slug=path.stem,
                kind='solve', draft=False, withheld=True, tags=[], body='',
                summary='This writeup will be available after the machine retires.')


def render_markdown(source):
    tokens = MD.parse(source)
    toc, used = [], set()
    for index, token in enumerate(tokens):
        if token.type == 'heading_open':
            label = tokens[index + 1].content
            stem = 'section-' + (re.sub(r'[^a-z0-9]+', '-', label.lower()).strip('-') or 'heading')
            anchor, counter = stem, 2
            while anchor in used:
                anchor = f'{stem}-{counter}'
                counter += 1
            used.add(anchor)
            token.attrSet('id', anchor)
            if token.tag in ('h2', 'h3'):
                toc.append(f'<a href="#{anchor}">{escape(label)}</a>')
    return MD.renderer.render(tokens, MD.options, {}), ''.join(toc)


def page(title, content, active='', base='', description='DJ Wheeler — cybersecurity student at Penn State, focused on offensive security.'):
    nav = ''.join(f'<a href="{base + url or "./"}"' + (' aria-current="page"' if active == label else '') + f'>{label}</a>'
                  for label, url in [('Home', ''), ('Writeups', 'writeups.html'), ('About', 'about.html'), ('Résumé', 'resume.html')])
    return Template((ROOT / 'templates/page.html').read_text(encoding='utf-8')).substitute(
        title=escape(title), description=escape(description), base=base, home=base or './', nav=nav,
        content=content, year=date.today().year)


def badges(post):
    platform = f'<span class="tag tag-platform">{escape(post["platform"])}</span>'
    if post['kind'] != 'solve':
        return platform
    status = post.get('box_status', 'unknown')
    label = {'active': 'Active', 'retired': 'Retired', 'unknown': 'Status unconfirmed'}[status]
    return platform + f'<span class="tag tag-{status}">{label}</span>'


def date_label(post):
    if post.get('date_source') == 'source-created':
        return 'Written '
    return 'Draft prepared ' if post['draft'] else ''


def card(post):
    tags = ''.join(f'<span class="tag">{escape(t)}</span>' for t in post['tags'])
    label = 'FORMAT EXAMPLE' if post['kind'] == 'guide' else escape(post['platform']).upper()
    if post['draft']:
        label = 'DRAFT PREVIEW / ' + label
    timing = ('Available after retirement' if post.get('withheld') else
              f"{date_label(post)}{escape(post['date'])} · {post['minutes']} min read")
    return f'''<article class="post-card" data-post data-platform="{escape(post['platform'])}" data-tags="{escape(' '.join(post['tags']))}">
      <div class="post-meta"><span class="accent mono">{label}</span><span>{timing}</span></div>
      <h3><a href="writeups/{post['slug']}.html">{escape(post['title'])}<span aria-hidden="true">↗</span></a></h3>
      <p>{escape(post['summary'])}</p><div class="tags">{badges(post)}<span class="tag">{escape(post['difficulty'])}</span>{tags}</div></article>'''


def build(preview=False):
    # Validate all content before replacing the generated output.
    all_posts = [read_post(p) for p in sorted((ROOT / 'content/posts').glob('*.md'))]
    posts = []
    for post in all_posts:
        if post['draft'] and not preview:
            continue
        if not post['draft'] and post['kind'] == 'solve' and post.get('publication_approved') is not True:
            raise ValueError(f"{post['slug']}: confirm publication_approved = true before publishing a solve")
        if not preview and post['kind'] == 'solve' and post['platform'] == 'HackTheBox' and post['box_status'] != 'retired':
            raise ValueError(f"{post['slug']}: public HTB solves require confirmed retired status; keep active or unconfirmed content as a local draft")
        posts.append(post)
    for path in sorted((ROOT / 'content/withheld').glob('*.toml')):
        notice = read_notice(path)
        existing = next((p for p in posts if p['slug'] == notice['slug']), None)
        if existing:
            if preview and existing['draft'] and existing['box_status'] == 'active':
                continue
            raise ValueError(f"{notice['slug']}: remove the retirement notice before publishing the full article")
        posts.append(notice)
    posts.sort(key=lambda p: (p['date'], p['slug']), reverse=True)
    output = ROOT / ('_preview' if preview else '_site')
    # Only these dedicated, generated directories may be replaced.
    assert output.parent == ROOT and output.name in ('_site', '_preview')
    if output.exists():
        shutil.rmtree(output)
    output.mkdir()
    for folder in ('assets', 'css', 'scripts', 'samples'):
        shutil.copytree(ROOT / folder, output / folder, ignore=shutil.ignore_patterns('*.py', '__pycache__'))
    media = ROOT / 'content/media'
    if media.exists():
        for post in posts:
            if post.get('withheld'):
                continue
            folder = media / post['slug']
            if folder.is_dir():
                shutil.copytree(folder, output / 'media' / post['slug'])
    (output / 'writeups').mkdir()
    (output / '.nojekyll').touch()

    def write(name, title, content, active='', base='', description=None):
        kwargs = {'description': description} if description else {}
        rendered = page(title, content, active, base, **kwargs)
        if preview:
            rendered = rendered.replace('</head>', '<meta name="robots" content="noindex, nofollow">\n</head>')
        (output / name).write_text(rendered, encoding='utf-8')

    latest = ''.join(card(p) for p in posts[:2]) or '<div class="empty-state"><h3>Field notes are on the way.</h3><p>Lab writeups will appear here as they are published.</p></div>'
    home = (ROOT / 'content/home.html').read_text(encoding='utf-8').replace('$latest', latest)
    write('index.html', 'Offensive security & field notes', home, 'Home')
    write('about.html', 'About', (ROOT / 'content/about.html').read_text(encoding='utf-8'), 'About')
    resume = (ROOT / 'content/resume.html').read_text(encoding='utf-8')
    write('resume.html', 'Résumé', '<div class="resume-content prose">' + resume + '</div>', 'Résumé')
    platforms = sorted(set(p['platform'] for p in posts))
    options = ''.join(f'<option>{escape(p)}</option>' for p in platforms)
    archive_note = ('Local draft preview. Draft articles and their images are excluded from the public build.'
                    if preview else 'Selected lab investigations and technical field notes. Completed solves appear after editorial review.')
    listing = f'''<section class="page-heading"><p class="eyebrow">THE LAB NOTEBOOK</p><h1>Field notes<span class="accent">.</span></h1><p>Lab writeups, technical observations, and the reasoning behind the result.</p></section>
    <div class="filters" hidden><div><label for="search">Search writeups</label><input id="search" type="search" placeholder="Search a topic, tool, or technique…"></div><div><label for="platform">Platform</label><select id="platform"><option value="">All platforms</option>{options}</select></div><button class="btn" type="button" id="clear-filters">Reset</button></div>
    <p class="result-count mono" id="result-count" role="status">{len(posts)} {'entry' if len(posts) == 1 else 'entries'}</p>
    <div class="post-list">{''.join(card(p) for p in posts)}</div><div id="no-results" class="empty-state" hidden><h2>No matching writeups.</h2><p>Try another term or reset the filters.</p></div>
    <p class="archive-note">{archive_note}</p>'''
    write('writeups.html', 'Writeups', listing, 'Writeups')
    for post in posts:
        if post.get('withheld'):
            content = f'''<a class="back-link" href="../writeups.html">← All field notes</a>
            <header class="page-heading article-heading"><div class="tags">{badges(post)}<span class="tag">{escape(post['difficulty'])}</span></div><h1>{escape(post['title'])}</h1></header>
            <section class="retirement-notice" aria-labelledby="retirement-title">
            <span class="lock-icon" aria-hidden="true">&#128274;</span><p class="eyebrow">ACTIVE MACHINE</p>
            <h2 id="retirement-title">Writeup available after retirement</h2>
            <p>This machine is still active on Hack The Box. To avoid spoilers and respect the platform's publication guidelines, the walkthrough will be published once it retires.</p>
            <a class="text-link" href="https://help.hackthebox.com/en/articles/5188925-streaming-writeups-walkthrough-guidelines">Read HTB's writeup guidelines ↗</a>
            </section>'''
            write(f"writeups/{post['slug']}.html", post['title'], content, 'Writeups', '../', post['summary'])
            continue
        body, toc = render_markdown(post['body'])
        banner = '<p class="notice">Draft preview — excluded from the public build.</p>' if post['draft'] else ''
        content = f'''<a class="back-link" href="../writeups.html">← All field notes</a>{banner}<header class="page-heading article-heading"><div class="tags">{badges(post)}<span class="tag">{escape(post['difficulty'])}</span></div><h1>{escape(post['title'])}</h1><p>{escape(post['summary'])}</p><div class="mono muted">DJ Wheeler · {date_label(post)}<time datetime="{post['date']}">{post['date']}</time> · {post['minutes']} min read</div></header><div class="article-layout"><article class="prose article-body">{body}</article><aside class="toc"><p class="eyebrow">ON THIS PAGE</p><nav aria-label="Table of contents">{toc}</nav></aside></div><a class="back-link" href="../writeups.html">← Back to field notes</a>'''
        write(f"writeups/{post['slug']}.html", post['title'], content, 'Writeups', '../', post['summary'])
    samples = [
        ('nittany', 'Network design', 'Nittany Network Solutions', 'WAN topology, infrastructure choices, and security considerations.'),
        ('kali', 'Instructional guide', 'Installing a Kali Linux VM', 'A practical introduction to setting up a virtual lab environment.'),
        ('polymorphic', 'Document redesign', 'Polymorphic Worms', 'Turning a dense academic essay into a more accessible web document.'),
        ('applications', 'Technical exposition', 'Induction & Recursion', 'Recursive patterns and proofs in computer science and mathematics.'),
        ('description', 'Technical description', 'The Systems of a Bicycle', 'Explaining how mechanical components work together.')]
    archive = '<section class="page-heading"><p class="eyebrow">SELECTED COURSEWORK</p><h1>Technical writing<span class="accent">.</span></h1><p>An archive of class projects in explanation, instruction, and document design.</p></section><div class="work-grid">'
    for slug, category, title, summary in samples:
        archive += f'<a class="work-card" href="samples/{slug}.html"><span class="eyebrow">{category}</span><h2>{title}</h2><p>{summary}</p><span class="text-link">View sample ↗</span></a>'
    write('samples.html', 'Technical writing', archive + '</div>')
    # Preserve existing sample content and URLs, replacing only the surrounding site shell.
    for path in (ROOT / 'samples').glob('*.html'):
        source = path.read_text(encoding='utf-8')
        match = re.search(r'<main\b[^>]*>(.*?)</main>', source, re.S)
        if 'css/style.css' in source and match:
            title = re.search(r'<title>(.*?)</title>', source, re.S).group(1).split(' — ')[0]
            write(f'samples/{path.name}', html.unescape(title), '<div class="legacy-content">' + match.group(1) + '</div>', base='../')
    print(f'Built {len(posts)} posts in {output.name}; drafts {"included" if preview else "excluded"}.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--drafts', action='store_true', help='Build a local preview including drafts into _preview')
    args = parser.parse_args()
    build(args.drafts)
