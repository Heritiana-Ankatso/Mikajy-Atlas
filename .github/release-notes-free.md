**Non-commercial use only.** Free to download and share, never to sell (code: PolyForm Noncommercial 1.0.0; trained model: CC BY-NC-SA 4.0).

**Mikajy Atlas 6.8** — updates 6.4, 6.5, 6.6 and 6.7 in place: tap *Get Mikajy Atlas 6.8* in the menu, your history and settings stay. On 6.3 or older (including any *Mikajy Free*), the app cannot update itself: export your history, uninstall the old app, then install this APK (6.4 changed the signing key).

## What changed since 6.7

**Fixed**
- **Answers follow what you wrote.** A calculation is computed from the structure that was read (what is under a root, in an exponent, in a fraction). `√(2²)³` is 8 (it said 2√3), `√9!` is 6, and `|−3|`, `arcsin 1`, `arctan 1` now have answers.
- **Exact answers keep every digit:** `2^34 = 17179869184` (it showed ≈17179869180). Very large approximations are written `≈1.43×10⁴⁵`, not `1.43e+45`.
- **Writing into a root, a power or a fraction lands where you wrote it.** An `=` or `+7` written after a root stays outside it, a number written in front of a root multiplies it, a small raised character is an exponent, drawing a root's bar further takes in what it covers, and a bar drawn under a number makes it a numerator.
- **Erasing:** erasing the base of a power keeps its exponent as plain writing; a straight line through symbols strikes them out.
- **Writing on a line reopened from history** edits it instead of replacing it. Numbers dropped into (or dragged out of) a calculation stay changed.

Full list: `CHANGELOG.md`.

---
Training data credits: **MathWriting** © Google LLC, CC BY-NC-SA 4.0; mathematical expressions in its labels from **Wikipedia** contributors, CC BY-SA 4.0. Other credits and licences: `LICENSE`, `licenses/`, `THIRD_PARTY_NOTICES.md`.
