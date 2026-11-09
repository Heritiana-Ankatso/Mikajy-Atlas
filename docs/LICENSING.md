# Licensing and distribution

**Current product name:** Mikajy Atlas (formerly Mikajy Atlas). The historic GitHub repository, package ID and prior release names are unchanged.

This document describes the **current Mikajy Atlas** repository. It supersedes earlier text that mistakenly described this edition as commercially reusable and stated it bundled no libraries. It is project documentation, not legal advice.

## Mikajy Atlas

- **First-party application source:** [PolyForm Noncommercial 1.0.0](../LICENSE). This is source-available, **not** an unrestricted commercial or OSI open-source grant. Selling the app or using it for commercial purposes is not permitted by that grant.
- **Research handwriting model** (`web/model/seq1-research.json`): **CC BY-NC-SA 4.0**. It includes training on MathWriting (Google LLC, CC BY-NC-SA 4.0), whose expression labels also require Wikipedia attribution (CC BY-SA 4.0). See [FREE.md](FREE.md) and [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md).
- **Caveat font** (`web/fonts/hand.woff2`): **SIL Open Font License 1.1**.
- **Bundled Nerdamer CAS 2.0.1:** **Apache-2.0**; the bundled **decimal.js 10.6.0** is **MIT**. Their copyright and licence notices must be retained. See [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md) and `licenses/`.
- Other original project files and assets must be assessed separately where noted; the non-commercial code grant does not replace their individual rights or notices.

Free downloads and sharing under the applicable notices are allowed. Commercial reuse of the **Free** edition is not allowed without obtaining the necessary separate permissions, including for the trained weights.

## Original Mikajy (separate repository)

The **`main` branch** of [ARHeritiana/Mikajy](https://github.com/ARHeritiana/Mikajy) was changed to the **MIT code licence on 2026-11-09**. Its pre-existing **`v5.0` tag and signed APK** were published with **GPL-3.0-or-later** source terms and remain unchanged; changing `main` does not relicense old release artifacts. New original-edition releases should disclose their exact licences. Code licencing alone does not establish rights in fonts, models, or training data.

The main-branch MIT grant permits use, modification, redistribution and commercial use of the original project code, subject to its licence conditions. Before commercially distributing a build, verify the provenance and rights of bundled recognizer weights and third-party materials. The original project's recognizer model should not be assumed automatically cleared merely because the first-party code has been relicensed.

## Separation rule

Code from the original project may be reused in Mikajy Atlas subject to its own licence. Reusing improvements from Mikajy Atlas in the original project requires checking the actual copyright grant and all dependencies: **never copy Free's MathWriting-trained weights, data, or other non-commercially restricted materials into the MIT original**. Avoid merging repositories wholesale.

## Trained data provenance

See [FREE.md](FREE.md) for the dataset register, usage restrictions, attribution obligations, and model identifiers. See [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md) for components in the actual app.

This documentation distinguishes source licences, trained-model rights, and release history; it is not a certification of commercial clearance.
