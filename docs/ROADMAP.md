# Roadmap

## 6.0 (Mikajy Free, current; first published as Mikajy Max)
Own app id and update channel, three-tab menu, English / Français, symbolic-first results, `True`/`False` for constant statements,
periodic equations, audited calculus engine (API only), stacked nested fractions, recogniser retrained on MathWriting.

## 6.1 — requested by the owner (2026-11-08)
All of these need the recogniser to learn new symbols (retrain: extend `training/mathwriting_to_npz.py`'s whitelist and the
`training/synth/` generator), engine support in `web/`, and tests. Exact arithmetic wherever the result is exact; a decimal is
always marked `≈`; unsupported beats a plausible wrong answer.

1. **Probability.** Declare `X ~ B(n, p)` (binomial) or `X ~ N(μ, σ)` (normal) on one line, then `P(X = 2)`, `P(X ≤ 9)`, `P(X < 3)`,
   `P(X ≥ 4)`, `P(a ≤ X ≤ b)`, `E(X)`, `V(X)` on later lines. The board remembers the declared variable. Binomial answers are exact
   rationals when p is rational; normal answers are numeric (marked `≈`). Expand to Poisson, geometric, uniform, exponential.
   Also `C(n,k)` / `P(n,k)` (nCr, nPr) notation. Needs: uppercase `X B N P`, `~`, `≤ ≥ < >`, `μ σ`.
2. **Defining and evaluating functions.** `f(x) = x² + 1` on one line, then `f(3)`, `f(1/2)`, `f(g(2))` on others; redefinition replaces.
   Shares the board's variable store with probability.
3. **Matrices:** determinant, inverse, transpose, products, powers, solving linear systems (exact rationals). The recogniser already
   reads matrix layout; the engine does not evaluate them yet.
4. **Modular arithmetic:** `a mod m`, `a ≡ b (mod m)`, modular inverse, powers mod m (BigInt), gcd / lcm. The recogniser already emits `mod`.
5. **Complex numbers:** extend the existing ℂ mode (exact Gaussian rationals): polar form, conjugate, modulus, argument, roots of unity.
6. **Differential equations:** first-order separable / linear, second-order linear with constant coefficients, with initial conditions
   (`y' + 2y = e^x, y(0) = 1`), using the bundled Nerdamer plus `web/calculus.js`'s rule: a solution is shown only after substituting it
   back into the equation numerically at several points. Needs `y'`, `y''`, `dy/dx` in the recogniser.

Not yet scheduled: handwriting input for `∫`, `d/dx` and `lim` (the calculus API exists; the recogniser cannot read them).
