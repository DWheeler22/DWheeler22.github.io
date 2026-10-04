# Publication review — October 4, 2026

The user requested publication readiness before merging to main. No merge, push, or live deployment was performed.

| Writeup | Original file creation date | Publication status | Evidence |
| --- | --- | --- | --- |
| Artificial | 2025-11-04 | Retired; enabled | [HTB machine listing](https://www.hackthebox.com/machines/artificial) |
| Blackfield | 2025-11-08 | Retired; enabled | [HTB machine listing](https://www.hackthebox.com/machines/blackfield) |
| Cascade | 2026-09-30 | Retired; enabled | [HTB machine listing](https://www.hackthebox.com/machines/cascade) |
| DevArea | 2026-03-30 | Retired; enabled | [HTB machine listing](https://www.hackthebox.com/machines/devarea) |
| Principal | 2026-03-12 | Retired; enabled; Medium | [HTB machine listing](https://www.hackthebox.com/machines/principal) |
| Garfield | 2026-04-06 | Active; public notice only | Author confirmed Active on October 4, 2026. |
| Logging | 2026-04-21 | Retired; enabled | Author confirmed Retired on October 4, 2026. |

Official machine descriptions were available in indexed HTB results; direct requests to several machine URLs redirected to the general landing page. Status should be rechecked in the authenticated platform before release if it differs from these records. Free access and expired seasonal status are not retirement indicators.

Creation timestamps were read from the original files in the Obsidian HackTheBox directory and saved in `writeup-source-dates.json`. Dates are stored explicitly in Markdown so copying or checking out this repository will not change them.

## Password protection and release boundary

The linked [HTB guidelines](https://help.hackthebox.com/en/articles/5188925-streaming-writeups-walkthrough-guidelines), updated August 20, 2026, allow public solutions for retired content and private sharing confined to a team. They do not state that a password makes an active-machine public writeup permissible.

[GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages) serves static files. A browser-side password form over plaintext content would leave HTML and images directly accessible. This change therefore implements a publication guard, not a password gate or a claim of secure private hosting. A separate authenticated private host and private source storage would be needed for team-only access.

The author confirmed all six other boxes are retired and requested a linked retirement notice for Garfield, following [this presentation reference](https://adhyanagarwal.com/writeups/smarthire). Garfield’s public record contains only its name, platform, difficulty, status, and original date. The public build does not use its walkthrough title, summary, tags, body, or screenshots. Its full Markdown and media are Git-ignored and retained locally. The draft preview still shows the full article when those local files are present. Nothing was deleted or moved. Retirement requires an explicit metadata and commit update; no automatic release date is promised.
