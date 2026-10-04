# Portfolio writeup selection — October 4, 2026

Seven editorial drafts were prepared from the local Obsidian notes. The recursive inventory contained 69 Markdown files: 55 in HackTheBox, seven in TryHackMe, four in OffSec, two in Red Labs, and one at the Boxes root. This includes empty indexes, templates, and duplicate notes; it is not a count of completed machines.

Selection emphasized a recorded end-to-end result, evidence for transitions between accounts, reasoning beyond tool output, and a varied set of portfolio skills. A completion checkmark alone was not sufficient. The selected notes received a closer review of their narrative, relevant command output, and chosen screenshots. External references support technical explanations; they are not evidence that these lab steps were independently rerun.

## Selected drafts

| Suggested reading order | Draft | Why it contributes | Remaining editorial work |
| --- | --- | --- | --- |
| 1 | [Cascade](../content/posts/cascade.md) | Clear investigation across LDAP, SMB, SQLite, .NET decompilation, and deleted objects; strong screenshots and an explicit final authentication result. | Confirm wording and publish date. |
| 2 | [Principal](../content/posts/principal.md) | Strong distinction between authentication and authorization, plus a concrete SSH certificate troubleshooting lesson. | Complete Java class and minimal Nimbus 9.31 POM added from the supplied implementation. Principal is now Medium; Maven compilation was not rerun during editing. |
| 3 | [Blackfield](../content/posts/blackfield.md) | A complete, readable AD chain that includes forensic artifacts and explains the impact of backup access. | Final author review of the expanded commands and account transitions. |
| 4 | [Artificial](../content/posts/artificial.md) | Adds model-processing security, Linux enumeration, tunneling, and privileged backup access. | Final author review; the encoded Backrest credential recovery now includes commands. |
| 5 | [DevArea](../content/posts/devarea.md) | Good evidence-driven pivots from Java inspection to SOAP SSRF, Hoverfly, and interpreter permissions. | Root-shell screenshot supplied by the author now confirms the result and restoration of Bash. |
| 6 | [Logging](../content/posts/logging.md) | Shows authentication troubleshooting, account control, update-package loading, and the interaction of certificate and DNS permissions. | All command gaps filled. Encoded callback content remains an explicitly labeled placeholder. |
| 7 | [Garfield](../content/posts/garfield.md) | The most advanced AD case; successful replication and final administrator authentication are recorded explicitly. | Author-supplied command sequences and complete key/hash values incorporated; final author review. |

The first four need the least reconstruction. The last three earn their places through technical depth and a recorded result, with explicit limits on reproducibility. All seven remain editable Markdown sources; the current publication decisions are recorded in [publication status](publication-status.md).

## Promising follow-ups and reasons for deferral

- **DarkZero:** strong cross-forest and SQL material; a good next AD article, but overlaps with the advanced coverage provided by Garfield and Logging.
- **DevHub:** interesting MCP and internal-service coverage; a strong next application-security candidate after checking its full authorization narrative.
- **Paperwork:** unusual UNIX file-descriptor exposure; worth expanding after separating the successful mechanism from the preceding secret-cracking attempts.
- **Nimbus:** broad cloud-emulation and container coverage, but the final working CodeBuild sequence relies on a friend's configuration, and the overlay/host explanation needs closer reconstruction.
- **Ping Pong:** substantial technical work, but the notes explicitly leave the decisive certificate-template permission unexplained.
- **Pirate:** a major relay transition still has a TODO explanation.
- **Checkpoint:** marked complete, but the closing VM-backup/Volatility section does not clearly narrate the final result.
- **Connected, Kobold, Interpreter, Enigma:** useful material with compressed or uncertain transitions, mixed exploratory notes, or summaries that need reconciliation with evidence.
- **Active, Forest, Sauna, Bastion, Chemistry:** viable shorter pieces; deferred to avoid repeating the same introductory credential and AD themes in this first set.
- **WingData, VariaType, Silentium, Reactor, Pterodactyl, Browsed:** promising application chains, but the chosen set offers a better first balance of explanatory detail and evidence; these merit a second editorial pass.
- **Layover and Touch:** interesting pivoting and kiosk material; selected for a later set rather than crowding the first release.
- **Writer, Abducted, Bedside, Relevant, Jerry, Netmon, and other sparse notes:** templates, partial investigations, or too little explanatory content for this batch.
- **TryHackMe / OffSec / Red Labs:** scanned as part of the inventory. Attacktive Directory and the Azure lab are the strongest alternatives outside HTB. The Azure material deserves a separate review of tenant-specific data and the exact Conditional Access behavior; this batch stays focused on the requested HTB portfolio.

## Editorial conventions

- The displayed dates now use each original Obsidian file's creation metadata, at the author's request. [The source-date record](writeup-source-dates.json) preserves those values. They identify when writing began, not a solve or website publication date.
- Difficulty values come from the source notes; the author subsequently confirmed Principal as Medium.
- First-person narrative describes the original documented lab work, not new exploitation performed during editing.
- Articles retain attribution for published research. Source provenance and editorial discussion belong in this guide, not in the reader-facing walkthroughs. The source material also records AI assistance for DevArea's strategy and Principal's project scaffolding, and a friend's help with Garfield's payload.
- Failed hypotheses are distinguished from successful steps. No root shell, CVE, or causal explanation is invented to fill an evidence gap.
- Command examples include recovered lab credentials where needed to follow the account transitions. Flags remain omitted. Screenshots are selected, unchanged lab evidence and can show lab credentials, addresses, and usernames.
- Fourteen screenshots are stored in per-article media folders: thirteen selected from the vault and one root-shell image supplied by the author. The remaining images and raw notes stay in Obsidian. [The media manifest](writeup-media-manifest.json) records the source filename, destination, and SHA-256 for each copy.
- The revised articles include more commands and explain their execution context. Specific `[TODO]` markers identify content left for manual insertion or verification; uncertain detours that do not help explain the successful chain have been removed.
- Editing corrected identifiable syntax and interpretation errors, but did not rerun the lab exploits. The author supplied the complete Principal implementation and DevArea root-shell evidence in the follow-up. The Java example was cleaned up and its POM reduced to the dependency it uses; Maven is unavailable locally, so compilation was not rerun.

## Edit and preview

The editable source of truth is `content/posts/<machine>.md`, with images in `content/media/<machine>/`. This is a one-time editorial import, not a live sync with Obsidian; editing the original vault will not overwrite the portfolio drafts.

From the repository root, run:

```sh
python scripts/preview.py
```

Open `http://127.0.0.1:8765/writeups.html`. Saving Markdown, image, template, or style changes rebuilds the local preview and refreshes the browser. Stop it with Ctrl+C. Use `--port 8766` if another application uses port 8765.

Use normal Markdown image links, for example:

```markdown
![Describe the evidence](../media/cascade/audit-decryption.png)
```

Do not edit `_preview` or `_site`: those are generated. There is no need to maintain a separate article index; filenames and TOML metadata populate the listing, search, tags, table of contents, and article pages automatically.

## Publication

Artificial, Blackfield, Cascade, DevArea, Logging, and Principal have `draft = false`, `publication_approved = true`, and `box_status = "retired"`. Garfield is confirmed Active: its full writeup remains a local, Git-ignored draft, with a spoiler-free retirement notice at its public URL. Public builds reject non-retired HTB solves. See [publication status](publication-status.md) for supporting sources and the active-content hosting limitation.

The existing GitHub workflow builds on pushes to `main` and can deploy the generated public site when Pages is configured. No deployment or repository push was performed here. Draft flags exclude website output, but do not hide source files or images if committed to a public Git repository.

## Follow-up integration

The supplied commands replace the Garfield TODOs and the certificate/DNS/WSUS gaps in Logging. The remaining Logging account-access and DLL steps were recovered from the source walkthrough. The archive command is an editorial reconstruction of the documented DLL-at-archive-root layout. Garfield imports the generated ticket file rather than repeating an abbreviated base64 blob.

Principal's supplied output used `$int_roles`, whereas the supplied final class uses `role=ROLE_ADMIN`. The article keeps the final class and omits the mismatched output and expired token rather than presenting them as a matching run. Unused imports and unused pac4j/JUnit dependencies were removed. No lab authentication, payload, or exploit was executed during this editing pass.

All inline `[TODO]` markers in the seven articles are resolved. Automated length checks confirm the supplied Garfield AES-256 key has 64 hexadecimal characters and both supplied NT hashes have 32. Deliberate per-run placeholders (ticket-cache filename, encoded callback, lab addresses) are explained next to their commands.
