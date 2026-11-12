# Changelog

All notable changes to Mikajy. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and versions follow `MAJOR.MINOR` (the Android `versionName`).

## [Unreleased]

### Fixed
- **Writing into a fraction lands where you wrote it.** A digit written before or after a symbol of the numerator, the denominator or a root goes into that row, next to that symbol; one written over a symbol replaces it. Before, it was lost, or added after the whole fraction (`2/√3` with a 1 after the 3 became `2/√3 − 1`). A fraction's handwriting cannot be matched to the symbols on screen character by character, so the edit is made on the reading itself: the new character is read alone and its token put beside the nearest symbol of the same row (`structSlot` in `web/app.js`); a character not clearly in a row is read with the line as before.
- **Erasing inside a fraction** removes the symbols you scribbled over, by what is on screen, and the rest of the reading stays as it was.
- New test `tests/browser_struct_edit.py` (in CI).

## [6.5] - 2026-11-12

Updates 6.4 in place from the app (same key). `versionCode` 21.

### Branding
- **New Atlas logo:** four identical solid white chevrons between two white bars, on a rounded tile split black / red (`branding/logo-atlas.svg`, launcher icon `android/res/drawable/icon.png`). It replaces the M in a white disc. Same red / black / white.

### Fixed
- **Insertions are placed by where you wrote them, and read in context.** The new strokes are carried into the handwriting's own frame (the reading and the ink under it drift apart), the ink to the right makes room, and the whole line is read; the result is kept only if the other characters came out unchanged, otherwise the new character is read alone and inserted by position. Characters with turns written next to an earlier reading no longer erase the invisible ink under them, a doubtful scribble that touches nothing is kept as writing, and one unreadable stroke no longer switches the sequence recogniser off for the session.

## [6.4] - 2026-11-11

### Fixed
- **Writing on past the end of a line is not erased.** When you carry on writing after a line that already has an answer, the new characters land where the old answer is shown. A character with turns there (a 6, an 8, a 3) used to be taken for a scribble and erased the answer instead of being written (in 6.3: `24 ÷ 97 + 19 − 8 − 6` lost its last 6). A stroke that stays within one answer glyph is now settled by the recogniser like one over a glyph of the reading. The sequence-recogniser and scribble browser tests now run in CI.
- **Erasing is exact.** A scribble removes only the characters the pen actually passed over: glyphs are judged on the middle of their box and handwriting on the ink itself, so a neighbour written close by stays. A character goes whole (all its strokes), so no leftover stroke is read as a character you never wrote. On a plain reading (digits, letters, operators) the other characters are kept exactly as read instead of the whole line being read again, which used to invent symbols (a `÷` erased from `24 ÷ 97` came back as `×`).
- **Writing into a finished reading works.** A character written over a glyph replaces it, one written between glyphs is inserted there, one written after the last glyph is appended. Only the new strokes are read and the reading is edited in place (plain readings), so the old handwriting under it no longer garbles the result. A character with turns (8, 3, 5, S) written over a glyph is no longer taken for a scribble: a compact stroke over one glyph is erasing only when the recogniser reads it as a scribble-like letter (W, M, n ...).
- **Smoother ink.** The live stroke follows the pen tip, the pen is sampled more finely, the ink is drawn through a light average that removes sensor jitter (the recogniser still sees the raw points), and the canvas is sharp up to 3x pixel density (was 2x).

### Release
- **New signing key.** 6.4 is signed with a key of its own (certificate SHA-256 `D60280CF…F452C234`, full value in `releases/SIGNING_CERT_SHA256.txt`); 6.0–6.3 used the key shared with Mikajy Spark. Android does not install it over 6.3: uninstall first. `release.yml` can now be started from the Actions tab, and publishes a locally signed APK committed under `releases/` when the `release` environment has no signing secrets.

### Licensing documentation
- The `Required Notice:` line in `LICENSE` names the repository by its current URL (`Heritiana-Ankatso/Mikajy-Atlas`, was the pre-rename `Mikajy-Free`). Same copyright holder, same PolyForm Noncommercial 1.0.0 terms; nothing else in the licence changes. The security-advisory links in `SECURITY.md` and the issue chooser point there too.

## [6.3] - 2026-11-09 — Mikajy Atlas


### Added
- **Inequalities.** `<`, `>`, `≤`, `≥` are solved exactly by sign analysis: polynomials, rational functions (poles stay open), and `2^x`, `|x−1|`, `ln x`, `√x`. The answer is a set with exact endpoints: `S=]−∞ ; −2] ∪ [2 ; +∞[` in French, `S=(−∞, −2] ∪ [2, ∞)` in English; `S=ℝ`, `S=∅`, or `{1}` when it applies. Between constants it says True / False. Periodic ones (`sin x > 0`) and functions whose domain edge has no exact value are refused ("unsupported") rather than guessed. The inequality sign is itself the request, so it answers in *On demand* mode without a trailing `=`, and in *complex* mode (an order exists on the reals only).

### Fixed
- **No more automatic zoom-out after writing.** The view only slides to keep the answer in sight, never leaving the start of the line off screen. The zoom pill now brings you back to what you wrote (all of it, centred) instead of the board's origin.
- **Exact answers are shown alone**, without an approximate decimal beside them (`√2`, `π/4`, `2√2`, `e^(−3)`); decimals appear when the result is irrational and you chose decimals, marked `≈`.
- **`f(x) = x² + 1` followed by `f(3) =` now answers.** Tall handwritten brackets are read as the fused `\left(` / `\right)` tokens, which the board's memory did not recognise, so the definition and the call were never matched.
- **Exponents are written like on paper:** `e^(x²/2)` shows `x²` with a raised power inside the exponent and a plain slash (no `÷`, no brackets unless the parts are sums), instead of `(x2)÷(2)`.
- **A single arbitrary constant is `C`, not `C1`** in differential-equation answers (two constants keep their numbers).
- **`\left(` and `\right)` no longer appear as the words "left(" and "right)".** The recogniser emits them as single tokens; the board, the calculator and the matrix/modular evaluator now treat them as plain brackets (so `(4/3)³ ÷ 1/3` also gets its answer).
- **The root sign spans its whole radicand.** Over a stacked fraction (or a power) the bar clears the numerator and the hook reaches the denominator.
- **Scribble erase is more forgiving.** Over writing, any zigzag with two sharp turns (up-down-up) erases it instead of being read as a letter, and a scribble also erases what its box fully encloses.

### Branding
- Update the release checker and URL allowlist to the renamed `Heritiana-Ankatso/Mikajy-Atlas` repository. Existing signed APKs retain their historical update code; only future builds incorporate this correction.
- Rename the full edition to **Mikajy Atlas** (formerly Mikajy Free) in launcher labels, web UI, localization, and future release names. Keep the `com.mikajy.app.free` Android package ID, GitHub update channel, signing identity, and old release artifacts unchanged.
- New launcher icon / logo for Atlas (`branding/logo-atlas.svg`): a heavy black M cut out of a white disc inside a red ring, on a black tile, still black / red / white. It replaces the former Free emblem; sources and renderer are in `branding/`.

### Licensing documentation (2026-11-09)
- Clarified that this edition uses PolyForm Noncommercial 1.0.0 for first-party code, CC BY-NC-SA 4.0 for research model weights, plus the separately licensed bundled Nerdamer, decimal.js and Caveat font.
- Corrected obsolete commercial-use claims in `docs/LICENSING.md`. The sibling Mikajy code on `main` is now MIT, while its tagged `v5.0` release remains GPL-3.0-or-later; no old APK was relicensed.

## [6.2] - 2026-11-09

### Fixed
- **Updates happen inside the app.** Tapping *Get Mikajy Free x.y* used to open the browser and download the APK there. The app now downloads it itself (progress shown on the button), checks it against the release's `SHA256SUMS.txt`, and hands it to Android's installer, which asks once and replaces the app in place; your history and settings stay. If Android has not yet allowed Mikajy Free to install apps, the button opens that one settings screen and asks you to tap again. Only GitHub hosts are ever contacted; Android refuses anything not signed with the same key. New permission: `REQUEST_INSTALL_PACKAGES` (used only for this). `android/src/com/mikajy/app/UpdateInstaller.java`.
- Updating *to* 6.2 still needs one manual download for anyone on 6.1 or older, because the old versions cannot update themselves in place.

## [6.1] - 2026-11-09

### Added
- **Answers are typeset like paper:** fractions stacked, roots with the bar over the whole radicand, raised exponents, constants first (`1 − √6`); `arg` answers too.
- **Your handwriting is replaced by the reading, in place** (as in 5.0); the ink fades and the view follows the answer.
- **Scribble to erase** works over finished readings. **Tap a symbol to correct it**: the model's runner-up readings are offered one tap at a time.
- **Retrained recogniser** (MathWriting human ink + synthetic strokes from 57 OFL fonts + habits: a 1 with a long flag, crossed 7, open 4, a 9 from the top, x as `)(`; stroke-order augmentation). On 29 finger-written samples: **31.0 % read exactly right** (token error 32.1 %), up from 27.6 % (43.8 %) in 6.0 and 3.4 % for the shipped Mikajy 5.1 model. On MathWriting test ink: 53.3 % exact (token error 9.9 %) on the expanded set that includes the new domains.
- **Functions:** `f(x) = x² + 1`, then `f(3)`, `f(1/2)`, `f(g(2))`; a line sees the definitions above it. **Probability:** `X ~ B(n, p)` / `N` / `P` / `G` / `U` / `E`, then `P(X = k)`, `P(X ≤ k)`, `P(a ≤ X ≤ b)`, `E(X)`, `V(X)`, `C(n, k)` — exact (binomial, geometric, uniform, and Poisson / exponential as `q + c·e^(−λ)`), the normal distribution marked `≈`. `web/board-core.js`, `web/prob-core.js`.
- **Differential equations:** first-order linear and separable, second-order with constant coefficients and forcing, initial conditions, `y'`, `y''`, `dy/dx`; every solution is substituted back before it is shown. `web/ode-core.js`.
- **Complex numbers:** conjugate (`\overline z`), argument (a multiple of π when it is one), exact `e^(iπk/2)`; `e^(iπ)` is now exactly `−1`.
- **Answers are typeset:** integer fractions are stacked, exponents raised, and `√2/2` no longer shows a `÷`. The board draws `~ ≤ ≥ ≠`, the prime and a bar over a conjugate.
- **Recogniser training data:** new notation, a 9 written from the top and an x written as `)(`.
- **Matrices** (exact): `det`, `|A|`, `A⁻¹`, `Aᵀ`, `Aⁿ`, `A+B`, `AB`, `kA`; singular or mismatched matrices are refused. **Modular arithmetic**: `a mod m`, `aᵇ mod m` without forming `aᵇ`, `gcd`, `lcm`; **congruences**: `a ≡ b (mod m)` → True/False, `ax ≡ b (mod m)` → `x ≡ r (mod m')`, or `S=∅`. `web/linalg-core.js`, `web/modular-core.js`, `web/latex-eval.js`, `tests/latex-eval.test.cjs`.
- **Matrices look like they do on paper:** a bracketed grid (square, round or bars) whose brackets grow with the entries, entries aligned in columns and rows, stacked fractions allowed inside entries; answers are drawn the same way. Matrix readings no longer print their environment name (`bmatrix`) on the board.

## [6.0] - 2026-11-08 — Mikajy Free

### Recogniser (retrained)
- The stroke-sequence model was retrained on synthetic font strokes plus **MathWriting** human ink (CC BY-NC-SA 4.0; 45k expressions filtered to what the calculator understands; weights `web/model/seq1-research.json`, CC BY-NC-SA 4.0).
  Measured on 1,037 held-out MathWriting expressions (tablet / stylus ink): **60.0 % read exactly right** (token error 8.2 %), up from 49.3 % for the first MathWriting run on the same set; fractions 62.7 %, fractions inside fractions 53.3 %.
- **Honest limit:** on 29 of the owner's own finger-written samples only **27.6 % are read exactly right** (token error 43.8 %). The model reads stylus ink much better than finger ink; a 30-minute finger-style fine-tune was tried and did not clearly help (31.0 % on those 29, but worse on MathWriting), so it is not shipped. Expect misreads with finger writing; tap a symbol to correct it.

### Mikajy Free is now its own project
- **Moved and renamed.** What was *Mikajy Max* (branch `max-edition` of ARHeritiana/Mikajy, tags `max-vX.Y`) is now **Mikajy Free**, repository Heritiana-Ankatso/Mikajy-Free. New name, new logo (`branding/make_free_icon.py`, a FREE plaque), new application id `com.mikajy.app.free` (share authority `com.mikajy.app.free.share`); it still installs next to Mikajy and never replaces it. The licence (PolyForm Noncommercial 1.0.0; weights CC BY-NC-SA 4.0) and the whole history came along.
- **Updates** now follow this repository's *latest release* (plain `vX.Y` tags), as in Mikajy; the `max-v` pre-release channel is gone. Release notes start with the non-commercial notice and credits (`.github/release-notes-free.md`). Signed APKs may be committed under `releases/`.

### Added
- **Menu in three tabs** — *Actions* (history, copy, share, memory, clear), *Math* (results exact/decimal, angles, ℝ/ℂ, instant/on demand) and *App* (language, theme, updates) — instead of one long sheet. The rarely useful *Mixed* result format and the *Classic* recogniser are hidden unless they were already selected.
- **English / Français** (App → Language; follows the device language until chosen): the whole interface, toasts, the update texts and calculator words (`True/Vrai`, `unsupported/non géré`, `undefined/indéfini`). `web/i18n.js`, `tests/i18n.test.cjs`.
- Font: the Caveat subset in `web/fonts/hand.woff2` was regenerated (OFL, same weight, no Reserved Font Name) to include French accents; `tests/build_check.py` now fails if an interface string uses a character the font lacks.
- **Symbolic first:** irrational results show their closed form with the decimal second (`√8` → `2√2 ≈2.828…`, `sin(π/4)` → `√2/2`), and irrational equation roots show radicals (`x²=2` → `±√2`) when the CAS form matches the certified numeric roots. The default number format is now exact (`frac`); `dec` still gives decimals.
- **`4 = 2` is `False`** (and `4 = 4`, `1/3+1/6 = 1/2`, `√2·√2 = 2` are `True`): statements about constants are decided exactly, or symbolically, never by rounding.
- **Periodic equations:** `sin x = 0` → `x = nπ, n ∈ ℤ`; every family is verified by substituting several integers `n`.
- **Calculus engine** (`web/calculus.js`, bundled Nerdamer, Apache-2.0): derivatives, antiderivatives, definite integrals and limits, each audited against an independent numeric check of the original expression (finite differences, differentiating the answer back, Gauss–Legendre quadrature with a divergence guard, one-sided limits). The recogniser does not emit `∫`/`lim` yet, so this is an API (`Calculus.*`, `Calculator`) without handwriting input.
- `tests/calculus.test.cjs`.
- **Research licensing:** this project is under PolyForm Noncommercial 1.0.0 (code) and CC BY-NC-SA 4.0 (research weights) so it can be trained on non-commercial datasets and shared free of charge; see `docs/FREE.md`.
- **Stroke-sequence recogniser** (default; Settings → Recogniser, Classic still available): a transformer reads all the strokes of a line and emits LaTeX tokens — late additions, extended lines, multiple lines, exponents, denominators, matrices, complex numbers and `mod` are read without grouping rules. Ink stays on the board with the typeset reading and answer below it. `web/seq-core.js`, `web/model/seq1.json`, `training/{strokefeat,seqmodel,gen_corpus,train_seq,eval_seq,pack_seq,parity_seq}.py`, `tests/seq-core.test.cjs`, `tests/browser_seq.py`. Trained on synthetic strokes only.
- `training/eval_app.py --rec`, a recorded-clock replay and a viewport that contains all the ink.
- **ℝ / ℂ number domain** (Settings → Numbers): complex arithmetic with exact Gaussian rationals, all complex roots of polynomial and rational-function equations (`complexRoots` in `poly-core.js`), `tests/complex.test.cjs`.
- **Licence changed from GPL-3.0-or-later to MIT.**
- **Maths engine:** `web/poly-core.js` — exact polynomials and rational functions over ℚ and certified real-root finding
  (Sturm sequences, exact bisection). Equations in `x` now return *every* real root for polynomials up to degree 32
  and for fractions with `x` in the denominator (excluded points are removed). `|u|` and even powers invert to both branches.
- Exact trigonometric values at 30°/45°/60°/90° and their `π` multiples (`sin 30°=0.5`, `tan 45°=1`, no `≈`); decimal
  arithmetic uses the exact rational (`0.1+0.2=0.3`).
- Licensing documentation: `docs/LICENSING.md`, `THIRD_PARTY_NOTICES.md`, `licenses/OFL-Caveat.txt`.
- Synthetic handwriting generator (`training/synth/`, `training/generate.py`) and an offline data-collection page (`tools/collect/`).
- Trainer: `MIKAJY_ASSETS` directory, `--no-mnist`, `--cursive` (ligature-stroke augmentation) and `training/eval_model.py`.

### Changed
- Fixed: `×` inside an exponent was read as the variable x, and two roots closing on the same symbol lost a bracket.
- Synthetic generator: `+`, `×` and `x` are now drawn with two strokes most of the time (the font tracer drew them in one).
- `sin(30°)`, `sin(180°)` and similar now display exactly instead of `≈0.5` / `≈0`.
- `x⁴=16`, `|x|=2`, `x²/(x−1)=0` are solved instead of refused.

## [5.0] - 2026-11-07

### Added
- **Automatic update check.** The Android shell asks GitHub for the newest published release (at most once a day,
  only when online, switchable in Settings) and shows a dot on the menu button plus a *Get Mikajy x.y* entry.
  Nothing about the user or device is sent; the WebView itself stays offline. `INTERNET` is the only permission.
- **Exponentials and powers:** `e^x`, `e^(2x)`, `e^-1`, `10^-3`, exponents of brackets and of lower-case letters
  (the x-height `e` used to defeat the exponent detector), and a cursive `e` read as `c`/`o` before an exponent.
- **Cursive function names.** A word written in one pen-down (`sin`, `ln`, `cos`) is cut into letters at its
  ligatures by scoring every segmentation with the recogniser's own confidence; look-alike letters (`5`→`s`,
  `1`→`i`) are accepted inside words. New words: `exp`, `sqrt`, `cot`, `sec`, `csc`.
- **Maths engine:** `exp`, `sqrt`, `cot`, `sec`, `csc`; `sin2x`/`sin2π` read as `sin(2x)`/`sin(2π)`;
  exact rational powers (`8^(2/3)=4`, `4^(1/2)=2`); exact `e^0`, `ln 1`, `ln e`, `log 10`;
  equations with one `x` solved by exact inversion: `2^x=8`, `e^x=5`, `ln x=1`, `√(x+1)=3`, `5/x=2`, `x³=8`.
  Non-injective forms (`sin x=0`, `x⁴=16`, `|x|=2`) are still refused rather than answered with one "principal" value.
- Recogniser heuristics moved into a tested, DOM-free module (`web/recognizer.js`).
- Professional repository layout: docs, contribution and security policies, issue/PR templates, Dependabot,
  `package.json` scripts, wider CI (stroke-level end-to-end test, update-UI test, Java parser test).

### Changed
- Package metadata: `versionName` 5.0, `versionCode` 15.
- The multiplication-shaped glyph is now accepted as the first symbol of an exponent (`e^x`), which the old
  rule never allowed.

### Security
- The release-link guard exists twice (Java and JavaScript) and accepts only `https://github.com/Heritiana-Ankatso/Mikajy-Free/releases/…`.
- Update answers and the stored update record are re-validated field by field before use.

## [4.5] - 2026-11-07
Initial public release of the audited offline calculator. See [docs/AUDIT.md](docs/AUDIT.md).
