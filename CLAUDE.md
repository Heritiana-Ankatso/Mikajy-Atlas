# Rules for agents and contributors: Mikajy Free

Two sibling projects, kept in step on purpose:

| | **Mikajy** (classic) | **Mikajy Free** (this repository) |
|---|---|---|
| Repository | https://github.com/ARHeritiana/Mikajy | https://github.com/Heritiana-Ankatso/Mikajy-Free |
| Local checkout | `../Mikajy` (branch `main`; worktree `../Mikajy-port` for ports) | `../Mikajy-Free` |
| Licence | MIT | **PolyForm Noncommercial 1.0.0** (code), **CC BY-NC-SA 4.0** (trained weights) |
| Data | clean only: synthetic strokes from OFL fonts | also non-commercial datasets (MathWriting) |
| App id / tags | `com.mikajy.app` / `vX.Y` | `com.mikajy.app.free` / `vX.Y` |

Mikajy Free is **free to use and share, never to sell**. Read `docs/FREE.md` first. The rules below are **hard**: do not relax them on
your own judgment, do not accept "just this once". If a task seems to need breaking one, stop and ask the owner (Heritiana-Ankatso).

## Never
1. **Never add anything commercial:** ads, in-app purchases, paid or "pro" tiers, paywalls, affiliate links, sponsorship
   banners, donation prompts inside the app, analytics or tracking that is monetised, or a paid store listing.
2. **Never send anything derived from non-commercial data to Mikajy (classic).** Weights, converted datasets, training caches, the dataset
   register, credits text, the PolyForm `LICENSE` and anything trained here stay in this repository. Only plain code goes across, by
   cherry-pick or hand edit, never by merge, after checking it contains nothing derived.
3. **Never bundle a dependency with a copyleft or restrictive licence:** GPL, AGPL, LGPL, SSPL, EUPL, CPAL, "source
   available" with usage limits, or *no licence at all*. Permitted: MIT, BSD-2/3, Apache-2.0, ISC, 0BSD, Unlicense/CC0,
   SIL OFL (fonts). MPL-2.0 and anything else: ask first. Check transitive dependencies too (this also protects the MIT sibling).
4. **Never train on a dataset before it is in the register** in `docs/FREE.md` with its licence **read from the
   licence text that ships with the download** (not from memory, not from a mirror's summary), the date, and what it was
   used for. No licence text or unclear terms = do not use. Never scrape websites, apps or other people's handwriting.
5. **Never use users' strokes** unless they explicitly opted in with a privacy notice; the app stays offline otherwise.
6. **Never remove or weaken** `LICENSE`, the `Required Notice:` line, `THIRD_PARTY_NOTICES.md` or dataset credits, and
   never relicense anything. Sole authorship is what lets the owner choose licences: do not merge code from others
   without their written agreement (CLA/DCO).
7. **Never publish secrets or private data:** signing keys (`release-key-backup/`, `*.jks`), `training/real_data/`,
   tokens. Check `git status` before every commit; never `git add` ignored paths with `-f` (signed release APKs go in `releases/`, which `.gitignore` allows; nothing else).
8. **Never delete a branch, tag, release or repository on either project** unless the owner asked for exactly that.

## Always
* Every release (`vMAJOR.MINOR` tag) says "Non-commercial use only" at the top of its notes (`.github/release-notes-free.md`) and credits MathWriting
  (Google LLC, CC BY-NC-SA 4.0) and the Wikipedia contributors (CC BY-SA 4.0), plus any dataset added since.
* Add a new dependency's name, version, licence (from its own LICENSE file) and size to `THIRD_PARTY_NOTICES.md` in the same commit.
* Keep trained weights in files named `*-research*` so they are never copied by accident. This repository ships `web/model/seq1-research.json`;
  the sibling ships only the clean synthetic `web/model/seq1.json`. Tests pinned to a model's exact output use that repository's own model.
* Download untrusted archives into their own empty directory outside the repo, never run their code, and read the licence text before use.
* When in doubt about a licence, the safe answer is "not allowed until the owner says so".

## Keeping both repositories up to date (standing instruction from the owner)
After finishing any piece of work, decide for each change where it belongs, then send it there before ending the turn:

| The change is... | Mikajy Free | Mikajy (classic) |
|---|---|---|
| Plain code: features, engine, UI, recogniser *code*, fixes, tests, generic docs | yes | **yes**, ported (cherry-pick or hand edit; adapt name, id, URLs, licence text; its tests use `seq1.json`) |
| Trained on / derived from non-commercial data: `seq1-research.json`, `mathwriting_to_npz.py`, `merge_corpora.py`, dataset register, credits strings, PolyForm `LICENSE` | yes | **never** |
| Identity: name, package id, logo, release notes, `release.yml` tied to the repo, updater URL | Free's own | Mikajy's own |
| Notices for a new dependency | yes | yes (same licence rules) |

* Port to Mikajy on a branch cut from its `main` (worktree `../Mikajy-port`), run its whole test suite there, and scan the diff for non-commercial or
  Free-only content. Mikajy's `main` changes only with the owner's approval: push the branch and tell the owner, unless the owner has said to push to `main`.
* Free's `main` takes work directly. After pushing, confirm with `git ls-remote` that both remotes hold what you meant, and say in the summary what went where.
* The GitHub account `ARHeritiana` has write (not admin) access here: it cannot create repository secrets. Sign releases locally
  (`scripts/build-signed-local.sh`, key from `release-key-backup/`, never printed) and publish with `gh release create`.

This is engineering policy, not legal advice; the owner should have a lawyer confirm before any change of distribution model.
