**Non-commercial use only.** Free to download and share, never to sell (code: PolyForm Noncommercial 1.0.0; trained model: CC BY-NC-SA 4.0).

**Mikajy Atlas 6.7** — updates 6.4, 6.5 and 6.6 in place: tap *Get Mikajy Atlas 6.7* in the menu, your history and settings stay. On 6.3 or older (including any *Mikajy Free*), the app cannot update itself: export your history, uninstall the old app, then install this APK (6.4 changed the signing key).

## What changed since 6.6

**Fixed**
- **Erasing is reliable.** A scribble acts on what you see. Erased characters no longer come back when you write on the line again; a scribble over a fraction bar or a root sign is no longer read as writing (it erases the fraction, or the root sign alone); a scribble over an answer erases the calculation; a coarse zigzag across a line erases every glyph it passes through.
- **No more freezes on huge powers.** `x^99999 = 2`, `sin(x)^200 = 1` or `(1/3)^9999999` could freeze or crash the app; they now answer at once.
- **No incomplete answers.** `sin x + cos x = 1` listed 20 decimals as if they were every solution; it now says *unsupported* rather than guess.
- **Steep limits are right.** `lim (1+x)^400` at 0 said *undefined*; it is 1.
- **Statements in degrees:** `sin(30) = 0.5` in degree mode now says *True*.
- **Updates are only installed when their checksum is verified.**

Full list: `CHANGELOG.md`.

---
Training data credits: **MathWriting** © Google LLC, CC BY-NC-SA 4.0; mathematical expressions in its labels from **Wikipedia** contributors, CC BY-SA 4.0. Other credits and licences: `LICENSE`, `licenses/`, `THIRD_PARTY_NOTICES.md`.
