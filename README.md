# DJ Wheeler — security portfolio

A static portfolio with a Markdown publishing pipeline. No client-side framework, database, external fonts, or runtime Markdown dependency. Articles are readable with JavaScript disabled; JavaScript adds filters, code copying, and the terminal hover/focus animation.

## Build and preview

Requires Python 3.11 or newer.

```sh
python -m pip install -r requirements.txt
python scripts/build.py
python -m http.server 8000 --bind 127.0.0.1 --directory _site
```

Open http://localhost:8000. `_site` is the complete public site, including existing documents. The former root HTML pages have moved into the content/template pipeline; serve the generated `_site` folder, not the repository root. Build output is ignored by Git. Use `python scripts/build.py --drafts` and serve `_preview` instead to review drafts locally. Never deploy `_preview`.

## Add a writeup

Copy `content/post-template.md` into `content/posts/my-machine.md`. Use a lowercase, hyphenated filename; this becomes the permanent article URL. Metadata uses TOML between `+++` lines. Supported content includes ordinary Markdown, fenced code, tables, images, lists, and blockquotes. Raw HTML is escaped and unsafe link schemes are rejected by the Markdown renderer.

Or import a specific note from another local repository:

```sh
python scripts/import_note.py "C:/path/to/notes/machine.md" --slug machine-name --title "Machine name — central lesson" --platform HackTheBox --difficulty Medium
```

Imports always start as drafts and never overwrite existing posts. The importer copies only referenced local raster images located inside the selected note's folder and rewrites their paths. Use standard inline image links with URL-encoded spaces; convert Obsidian `[[wikilinks]]` / `![[embeds]]` first. Reference-style images, images with Markdown titles, and other attachments should be moved manually into `content/media/<slug>/` and linked as `../media/<slug>/filename`. Remote images remain remote. Do not commit private notes or secrets: **draft is a website publishing control, not privacy for a public Git repository**.

1. Edit the draft for clarity and verify it against your evidence.
2. Preview with `python scripts/build.py --drafts`.
3. Confirm the platform permits public publication. Set `publication_approved = true` for completed solves.
4. Set `draft = false`, rebuild, and review `_site` before publishing.

Only media folders named after published post slugs are included in the public build. Local draft previews include draft media too.

The included field-notes article is explicitly a **format example**, not a completed lab solve. Your private notes repository has not been connected or imported.

## Edit other pages

- `content/home.html`, `content/about.html`, `content/resume.html`: page copy.
- `templates/page.html`: navigation, contact URLs, and shared layout.
- `css/portfolio.css`: new visual theme; `css/legacy.css`: compatibility for original coursework.
- `scripts/site.js`: progressive enhancements.
- `samples/`: original coursework pages and downloads. Their wrappers are modernized during the build; standalone document redesigns retain their original presentation.
- `docs/content-roadmap.md`: suggested About and résumé updates, plus an AI editing prompt.

## Validation

```sh
python -m unittest discover -s tests -v
python scripts/build.py
python scripts/check_links.py _site
node --check scripts/site.js
```

## Hosting

Publish the contents of `_site` on any static host. All local links are relative, including at a GitHub Pages project subpath. The included GitHub Actions workflow validates and builds the site on pull requests, and deploys on pushes to `main` only. To activate it, choose **GitHub Actions** in the repository's Pages settings. No hosting settings were changed and nothing has been pushed or deployed by this redesign.
