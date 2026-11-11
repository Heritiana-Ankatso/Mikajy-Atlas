**Non-commercial use only.** Free to download and share, never to sell (code: PolyForm Noncommercial 1.0.0; trained model: CC BY-NC-SA 4.0).

**Mikajy Atlas 6.4** — signed with a new key of its own, so it does not install over 6.3 or older: uninstall the old app, then install this APK. Later versions update in place from the app.

## What changed since 6.3

**Fixed**
- **Erasing is exact.** A scribble removes only the characters the pen passed over, whole; the rest of the line stays exactly as read (erasing `÷` from `24 ÷ 97` no longer brings it back as `×`).
- **Writing into a finished reading works.** A character written over a glyph replaces it, one written between glyphs is inserted, one written after the last glyph is appended. An 8, 3, 5 or S written over a glyph is no longer taken for a scribble.
- **Writing on past the end of a line is not erased.** A 6 or an 8 written where the previous answer is shown used to erase it instead of being written.
- **Smoother ink:** the stroke follows the pen tip, jitter is smoothed, and the board is sharp on high-density screens.

Full list: `CHANGELOG.md`.

---
Training data credits: **MathWriting** © Google LLC, CC BY-NC-SA 4.0; mathematical expressions in its labels from **Wikipedia** contributors, CC BY-SA 4.0. Other credits and licences: `LICENSE`, `licenses/`, `THIRD_PARTY_NOTICES.md`.
