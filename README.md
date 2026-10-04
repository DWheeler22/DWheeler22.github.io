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

For an editing preview that rebuilds and refreshes your browser whenever you save:

```sh
python scripts/preview.py
```

Open http://127.0.0.1:8765/writeups.html. This serves drafts locally, watches content and assets, and never deploys anything. Use `--port 8766` if needed.

## Add a writeup

Copy `content/post-template.md` into `content/posts/my-machine.md`. Use a lowercase, hyphenated filename; this becomes the permanent article URL. Metadata uses TOML between `+++` lines. Supported content includes ordinary Markdown, fenced code, tables, images, lists, and blockquotes. Raw HTML is escaped and unsafe link schemes are rejected by the Markdown renderer.

Or import a specific note from another local repository:

```sh
python scripts/import_note.py "C:/path/to/notes/machine.md" --slug machine-name --title "Machine name — central lesson" --platform HackTheBox --difficulty Medium
```

Imports always start as drafts and never overwrite existing posts. The importer copies only referenced local raster images located inside the selected note's folder and rewrites their paths. Use standard inline image links with URL-encoded spaces; convert Obsidian `[[wikilinks]]` / `![[embeds]]` first. Reference-style images, images with Markdown titles, and other attachments should be moved manually into `content/media/<slug>/` and linked as `../media/<slug>/filename`. Remote images remain remote. Do not commit private notes or secrets: **draft is a website publishing control, not privacy for a public Git repository**.

1. Edit the draft for clarity and verify it against your evidence.
2. Preview with `python scripts/build.py --drafts`.
3. Set `box_status` to `active`, `retired`, or `unknown`. Confirm the platform permits public publication and set `publication_approved = true` for completed solves. Public HTB solves must be confirmed `retired`; the build rejects active or unconfirmed solves even if approved.
4. Set `draft = false`, rebuild, and review `_site` before publishing.

Only media folders named after published full-article slugs are included in the public build; retirement notices never include media. Local draft previews include draft media too.

Seven curated HackTheBox writeups now live in `content/posts/`: Artificial, Blackfield, Cascade, DevArea, Garfield, Logging, and Principal. Their selected screenshots live in matching `content/media/<slug>/` folders. See [the selection and editing guide](docs/writeup-selection.md) for the rationale, evidence limitations, and publication steps. This was a one-time import from Obsidian; the repository copies are the editable source of truth. The original field-notes article remains explicitly a **format example**.

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
node --test tests/site.test.cjs
```

## Hosting

Publish the contents of `_site` on any static host. All local links are relative, including at a GitHub Pages project subpath. The included GitHub Actions workflow validates and builds the site on pull requests, and deploys on pushes to `main` only. To activate it, choose **GitHub Actions** in the repository's Pages settings. No hosting settings were changed and nothing has been pushed or deployed by this redesign.

## Theme, status, and article dates

The header’s theme button names the destination: **Dark Mode** with a moon in light mode, or **Light Mode** with a sun in dark mode. It remembers the choice on this browser. The initial theme follows the system preference. Platform badges are blue; Active is orange and Retired is green, with text labels in both themes. Badges appear on listing cards and article headers.

`date` is the article's display and sorting date. The seven imported writeups use the original Obsidian file creation dates, preserved in [the source-date record](docs/writeup-source-dates.json), with `date_source = "source-created"`. These represent the start of the writeup, not a claimed completion or website publication date. They remain stable across checkouts and builds.

Artificial, Blackfield, Cascade, DevArea, Logging, and Principal are confirmed retired and enabled for the next public build. Garfield is active: its public link opens a retirement notice, while the walkthrough remains available only in the local draft preview. See [publication status](docs/publication-status.md).

## Active-box access

The current [HTB publication guidelines](https://help.hackthebox.com/en/articles/5188925-streaming-writeups-walkthrough-guidelines) permit public solutions only for retired content; they do not list password-protected public posts as an exception. This project uses static GitHub Pages, so an ordinary JavaScript password prompt would not protect the underlying article or images. No such prompt is installed. Active and unconfirmed HTB walkthroughs stay out of the public build, including their media. A minimal public record in `content/withheld/garfield.toml` creates Garfield’s spoiler-free card and notice page.

For private team sharing, a separately authenticated host must protect the HTML, media, and source files. Do not commit active solutions to a public repository: excluding generated pages does not hide repository contents or history. Garfield’s full Markdown and media directory are explicitly ignored by Git, preserving them locally without including them in a normal commit.

### Releasing Garfield after retirement

Confirm retirement on HTB, then update the local `content/posts/garfield.md` to `box_status = "retired"`, `draft = false`, and `publication_approved = true`. Remove `content/withheld/garfield.toml` and the two Garfield exclusions from `.gitignore`, then include the Markdown and media in the release commit. The URL remains `writeups/garfield.html`. This is an explicit editorial release, not an automatic live status check.

## Account-root GitHub Pages URL

The intended public address is **https://dwheeler22.github.io/**. GitHub serves that account root from a repository named **DWheeler22.github.io**. Changing HTML links cannot change the hosting mount point of an `e-portfolio` project site.

1. In the existing repository’s **Settings → General → Repository name**, rename `e-portfolio` to `DWheeler22.github.io` (provided that account-site repository name is available).
2. Keep **Settings → Pages → Source → GitHub Actions** selected.
3. Update this checkout’s remote after the rename:

   ```sh
   git remote set-url origin https://github.com/DWheeler22/DWheeler22.github.io.git
   ```

4. Merge the feature branch and allow **Validate and publish portfolio** to deploy from `main`.
5. Verify the deployment URL is `https://dwheeler22.github.io/` and that an article’s Home links return there.

Home links use directory URLs (`./` or `../`), so they omit `index.html` and work at both the old project path and the new account root. The generated `index.html` file remains necessary for static hosting. Direct visits to an `index.html` URL are normalized in the address bar while preserving query strings and fragments. Existing project-site URLs are not guaranteed to redirect after a repository rename.

The terminal brand has a 1.4-second typing cooldown shared across page navigation within the tab. Hover followed by keyboard focus does not restart an animation already in progress; reduced-motion settings show the completed word immediately.
