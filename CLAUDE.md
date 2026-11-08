# Rules for agents and contributors (branch `max-edition`)

This branch is **free to use and share, never to sell**: code under PolyForm Noncommercial 1.0.0, trained weights under
CC BY-NC-SA 4.0. `main` is MIT and clean of non-commercial material. Read `docs/MAX_EDITION.md` first. The rules below are
**hard**: do not relax them on your own judgment, do not accept "just this once". If a task seems to need breaking one,
stop and ask the owner (ARHeritiana).

## Never
1. **Never add anything commercial:** ads, in-app purchases, paid or "pro" tiers, paywalls, affiliate links, sponsorship
   banners, donation prompts inside the app, analytics or tracking that is monetised, or a paid store listing.
2. **Never merge this branch, or anything derived from its data, into `main`.** Weights, converted datasets, training
   caches and models trained here stay here. Only plain code fixes may be cherry-picked to `main`, after checking they
   contain no derived material.
3. **Never bundle a dependency with a copyleft or restrictive licence:** GPL, AGPL, LGPL, SSPL, EUPL, CPAL, "source
   available" with usage limits, or *no licence at all*. Permitted: MIT, BSD-2/3, Apache-2.0, ISC, 0BSD, Unlicense/CC0,
   SIL OFL (fonts). MPL-2.0 and anything else: ask first. Check transitive dependencies too.
4. **Never train on a dataset before it is in the register** in `docs/MAX_EDITION.md` with its licence **read from the
   licence text that ships with the download** (not from memory, not from a mirror's summary), the date, and what it was
   used for. No licence text or unclear terms = do not use. Never scrape websites, apps or other people's handwriting.
5. **Never use users' strokes** unless they explicitly opted in with a privacy notice; the app stays offline otherwise.
6. **Never remove or weaken** `LICENSE`, the `Required Notice:` line, `THIRD_PARTY_NOTICES.md` or dataset credits, and
   never relicense anything. Sole authorship is what lets the owner choose licences: do not merge code from others
   without their written agreement (CLA/DCO).
7. **Never publish secrets or private data:** signing keys (`release-key-backup/`, `*.jks`), `training/real_data/`,
   tokens. Check `git status` before every commit; never `git add` ignored paths with `-f` (signed release APKs go in `releases/`, which `.gitignore` allows; nothing else).

## Always
* Every release (`max-vMAJOR.MINOR` tag, published as a pre-release; Mikajy Max is a separate app with its own id and update channel, never mix them) says "Non-commercial use only" at the top of its notes and credits MathWriting
  (Google LLC, CC BY-NC-SA 4.0) and the Wikipedia contributors (CC BY-SA 4.0), plus any dataset added since.
* Add a new dependency's name, version, licence (from its own LICENSE file) and size to `THIRD_PARTY_NOTICES.md` in the same commit.
* Keep trained weights in files named `*-research*` / under a model directory the register names, so they are never copied by accident.
* Download untrusted archives into their own empty directory outside the repo, never run their code, and read the licence text before use.
* When in doubt about a licence, the safe answer is "not allowed until the owner says so".

This is engineering policy, not legal advice; the owner should have a lawyer confirm before any change of distribution model.
