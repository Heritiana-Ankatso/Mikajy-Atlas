# Mikajy Atlas (formerly Mikajy Free): licence, data and release rules

Mikajy Atlas lets the recogniser be trained on datasets whose licences forbid commercial use, and it can be **shared for
free** (source on GitHub, signed APKs from GitHub releases). It can **not** be sold or used commercially. Its sibling
[Mikajy Spark](https://github.com/ARHeritiana/Mikajy) has MIT-licensed first-party code on its current `main` branch (updated 2026-11-09), while the already-published `v5.0` release remains GPL-3.0-or-later. See [LICENSING.md](LICENSING.md); the models and rights of these editions must not be mixed.

## Licences here
* **Code:** PolyForm Noncommercial 1.0.0 ([LICENSE](../LICENSE)).
* **Research model weights:** CC BY-NC-SA 4.0 (the share-alike terms of the datasets below plausibly extend to them).
  Anyone who shares or adapts the weights must credit the datasets and keep the same licence.
* **Patrick Hand font:** SIL OFL 1.1, subset with thickened outlines (replaced Caveat on 2026-11-12).

## What "non-commercial" means here
Allowed: free download of the source and APK from GitHub or your own site; sharing with friends, classes, forums.
Not allowed: ads, in-app purchases, paid or "pro" tiers, selling the app or bundling it into something sold, paid
listings. Donation links are a grey area: keep them out of the app. If you want a store listing, check the store's terms
against this licence first. This is engineering guidance, not legal advice.

## Rules
1. **Cross-project flow.** Do not merge the repositories wholesale. Before reusing Atlas-edition code in original Mikajy, verify that its authors and third-party dependencies permit the intended licensing. The MathWriting-trained research weights, data, and derived artifacts must never be transferred to the original under an unrestricted MIT claim.
2. **Releases from here remain non-commercial only.** Tags are `vMAJOR.MINOR`; `.github/release-notes-free.md` puts "Non-commercial use only" and the
   credits at the top of every release note. Mikajy Atlas is a separate app (`com.mikajy.app.free`) with its own repository, so its updater
   (`releases/latest`) only ever sees Atlas releases.
3. **Record every dataset** in the register below before training on it: name, URL, licence as read from the licence text
   (not from memory), date checked, and which weights it contributed to.
4. **Keep trained weights separate** (`*-research*` naming) so their non-commercial restrictions and attribution cannot be lost.
5. The sibling's original `v5.0` release remains under its published GPL-3.0-or-later terms. Its `main` code is MIT from the documented 2026-11-09 correction; this Free licence does not amend either.

## Dataset register
Checked 2026-11-08 against the licence text shipped with each download.

| Dataset | Licence (as read) | Used for | Status |
|---------|-------------------|----------|--------|
| [MathWriting 2024](https://storage.googleapis.com/mathwriting_data/mathwriting-2024.tgz) (Google) | Archive: CC BY-NC-SA 4.0. LaTeX labels taken from Wikipedia: CC BY-SA 4.0 (`readme.md`, "Licensing Information") | `training/mathwriting_to_npz.py`: human train/valid/test splits, filtered to the calculator's symbols (45.6k train, 1.9k valid, 1.1k test expressions); synthetic split not used | shipped: weights `web/model/seq1-research.json` (run `combined2`, 2026-11-08) |
| OFL handwriting fonts (`fetch_assets.sh`) | SIL OFL 1.1 | synthetic strokes | in use |
| Pendigits (UCI) | no licence text in the archive; 8-point resampled digits only | — | downloaded, **not used** (too coarse; source terms unconfirmed) |
| CROHME 2011–2023 | research terms | benchmark / train | not obtained |
| Google QuickDraw | CC BY 4.0 (believed) | stroke-encoder pre-training | not used |
| MNIST | unclear | CNN digits | allowed here, not used for the sequence model |

Credits to ship with any release: MathWriting (Google LLC, CC BY-NC-SA 4.0) and Wikipedia contributors (LaTeX expressions, CC BY-SA 4.0).
