# Third-party notices

What is **inside the shipped app** (the APK):

| Component | Licence | Notes |
|-----------|---------|-------|
| Mikajy source (everything under `web/`, `android/src/`) | PolyForm Noncommercial 1.0.0 on this branch (see [LICENSE](LICENSE)); MIT on `main` | Written by the repository owner; see [docs/LICENSING.md](docs/LICENSING.md) for what that means commercially |
| Caveat font, subset in `web/fonts/hand.woff2` | SIL Open Font License 1.1 — [licenses/OFL-Caveat.txt](licenses/OFL-Caveat.txt) | © 2014 The Caveat Project Authors. The licence text must travel with the font |
| CNN weights `web/model/model4.f16.json` | Own work, trained as described in [docs/LICENSING.md](docs/LICENSING.md) | Training-data provenance is documented there |
| Research weights (stroke-sequence model, any `*-research*` model file) | CC BY-NC-SA 4.0 | Trained on the datasets in the register of [docs/RESEARCH_BRANCH.md](docs/RESEARCH_BRANCH.md); credit those datasets, non-commercial use only |
| Android platform classes | Apache-2.0 (Android Open Source Project) | Linked at build time through `android.jar`; no third-party library is bundled |

The app has **no JavaScript or Java runtime dependency**: no npm package, no AAR, no CDN, no SDK.

Training data credits (research branch): **MathWriting** © Google LLC, CC BY-NC-SA 4.0; mathematical expressions in its labels from **Wikipedia** contributors, CC BY-SA 4.0.

Used only to build, test or train (never shipped): Node.js (MIT), Playwright (Apache-2.0), JAX and Optax (Apache-2.0),
NumPy, SciPy and scikit-image (BSD-3-Clause), OpenCV (Apache-2.0), Pillow (HPND), fontTools (MIT).
