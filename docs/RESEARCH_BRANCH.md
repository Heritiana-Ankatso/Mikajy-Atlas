# Research branch (`research/noncommercial`)

This branch lets the recogniser be trained on datasets whose licences forbid commercial use, and it can be **shared for
free** (source on GitHub, signed APKs from GitHub releases). It can **not** be sold or used commercially. `main` keeps the
MIT licence and the clean-data rules in [LICENSING.md](LICENSING.md); the two must not be mixed.

## Licences on this branch
* **Code:** PolyForm Noncommercial 1.0.0 ([LICENSE](../LICENSE)).
* **Research model weights:** CC BY-NC-SA 4.0 (the share-alike terms of the datasets below plausibly extend to them).
  Anyone who shares or adapts the weights must credit the datasets and keep the same licence.
* **Caveat font:** SIL OFL 1.1, unchanged.

## What "non-commercial" means here
Allowed: free download of the source and APK from GitHub or your own site; sharing with friends, classes, forums.
Not allowed: ads, in-app purchases, paid or "pro" tiers, selling the app or bundling it into something sold, paid
listings. Donation links are a grey area: keep them out of the app. If you want a store listing, check the store's terms
against this licence first. This is engineering guidance, not legal advice.

## Rules
1. **One-way flow.** Code fixes may be cherry-picked from this branch to `main`. Weights, training caches, converted
   datasets and anything derived from them must never be merged into `main`.
2. **Releases from here are free releases only.** Use ordinary `vMAJOR.MINOR` tags (the release workflow and the in-app
   updater only accept that form), and put "Non-commercial use only" plus the dataset credits at the top of every release
   note. The updater follows the repository's `latest` release, so an installed MIT build will offer this one as an update.
3. **Record every dataset** in the register below before training on it: name, URL, licence as read from the licence text
   (not from memory), date checked, and which weights it contributed to.
4. **Keep trained weights separate** (`*-research*` naming) so they can't be copied into a `main` build by accident.
5. Releases already published under MIT stay MIT; this branch does not revoke them.

## Dataset register
Checked 2026-11-08 against the licence text shipped with each download.

| Dataset | Licence (as read) | Used for | Status |
|---------|-------------------|----------|--------|
| [MathWriting 2024](https://storage.googleapis.com/mathwriting_data/mathwriting-2024.tgz) (Google) | Archive: CC BY-NC-SA 4.0. LaTeX labels taken from Wikipedia: CC BY-SA 4.0 (`readme.md`, "Licensing Information") | `training/mathwriting_to_npz.py`: human train/valid/test splits, filtered to the calculator's symbols (45.6k train, 1.9k valid, 1.1k test expressions); synthetic split not used | in training (`combined1`) |
| OFL handwriting fonts (`fetch_assets.sh`) | SIL OFL 1.1 | synthetic strokes | in use |
| Pendigits (UCI) | no licence text in the archive; 8-point resampled digits only | — | downloaded, **not used** (too coarse; source terms unconfirmed) |
| CROHME 2011–2023 | research terms | benchmark / train | not obtained |
| Google QuickDraw | CC BY 4.0 (believed) | stroke-encoder pre-training | not used |
| MNIST | unclear | CNN digits | allowed on this branch, not used for the sequence model |

Credits to ship with any release: MathWriting (Google LLC, CC BY-NC-SA 4.0) and Wikipedia contributors (LaTeX expressions, CC BY-SA 4.0).
