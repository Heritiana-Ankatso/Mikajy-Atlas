# Roadmap

## 6.0 (Mikajy Free, current; first published as Mikajy Max)
Own app id and update channel, three-tab menu, English / Français, symbolic-first results, `True`/`False` for constant statements,
periodic equations, audited calculus engine (API only), stacked nested fractions, recogniser retrained on MathWriting.

## 6.1 — requested by the owner (2026-11-08): engines done, recogniser retraining in progress
Everything below is implemented in `web/`, tested, and drawn on the board; the recogniser was retrained on the new notation (capital letters, `~`,
`≤ ≥ < >`, the prime, `\overline`, function calls) plus two handwriting habits the old data lacked: a **9 written from the top** and an **x written as two
back-to-back arcs `)(`** (never confused with `×`). Exact arithmetic wherever the result is exact; a decimal is always marked `≈`; unsupported beats a plausible wrong answer.

1. **Probability — done.** `X ~ B(n, p)`, `N(mean, deviation)`, `P(λ)` (Poisson), `G(p)`, `U(a, b)`, `E(λ)`, then `P(X = k)`, `P(X ≤ k)`, `<`, `≥`, `>`, `P(a ≤ X ≤ b)`, `E(X)`, `V(X)`
   and `C(n, k)`. Binomial, geometric and uniform answers are exact fractions; Poisson and exponential answers are exact `q + c·e^(−λ)`; the normal distribution is numeric (`≈`).
   The declared variable is remembered by the board (`web/board-core.js`, `web/prob-core.js`). Not done: `P(n, k)` (permutations), `\mu`/`\sigma` as symbols.
2. **Functions — done.** `f(x) = x² + 1`, then `f(3)`, `f(1/2)`, `f(g(2))` on later lines; a redefinition replaces; a line sees what is written above it (or, failing that, below it).
   Names: any lowercase letter except `e`, `i`, `x`, `y`; one variable, `x`.
3. **Matrices — done** (exact; drawn as bracketed grids). Still to do: linear systems, rank, eigenvalues.
4. **Modular arithmetic — done** (`mod`, `aᵇ mod m`, `gcd`, `lcm`, congruences). Still to do: systems of congruences (CRT).
5. **Complex numbers — done:** `\overline z` (conjugate, exact), `\arg z` (as a multiple of π when it is one), exact `e^(iπk/2)`. Not done: polar-form output, roots of unity written as `\sqrt[n]{1}`.
6. **Differential equations — done:** first order linear (also `x y' + y = 1`) and separable (`y' = x y`), second order with constant coefficients and forcing, initial conditions after the
   equation, `y'`, `y''` and `dy/dx` notation (`web/ode-core.js`). Every solution is substituted back into the equation and the conditions before it is shown. Refused, never guessed:
   nonlinear, variable-coefficient second order, forcing the bundled CAS cannot integrate (`y' + y = sin x`), conditions on a second line.

Not yet scheduled: handwriting input for `∫`, `d/dx` and `lim` (the calculus API exists; the recogniser cannot read them).
