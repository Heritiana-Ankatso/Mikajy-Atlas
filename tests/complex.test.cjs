'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const Poly = require('../web/poly-core.js');
const MathCore = require('../web/math-core.js');
const Calculator = require('../web/calculator.js');
const T = s => s.split(' ');
const C = {domain: 'complex', mode: 'instant', angle: 'rad', fmt: 'dec'};
const calc = (t, set = {}) => Calculator.compute(T(t), {...C, ...set}, true);
const within = (a, b, tol = 1e-12) => assert.ok(Math.abs(a - b) <= tol, `${a} ≠ ${b}`);

test('complex arithmetic is exact in the Gaussian rationals', () => {
  assert.equal(calc('( 1 + 2 i ) ( 3 - i )').text, '5+5i');
  assert.equal(calc('i ^ ( 2 )').text, '-1');
  assert.equal(calc('i ^ ( 7 )').text, '-i');
  assert.equal(calc('sqrt ( - 4 )').text, '2i');
  assert.equal(calc('( 3 + 4 i ) / ( 1 - 2 i )').text, '-1+2i');
  assert.equal(calc('1 / ( 1 + i )').text, '0.5-0.5i');
  assert.equal(calc('abs ( 3 + 4 i )').text, '5');
  assert.equal(calc('2 i ^ ( 2 ) + 3').text, '1');
  assert.equal(calc('( 1 + i ) ^ ( 8 )').text, '16');
});

test('irrational complex results are exact when a closed form exists, approximate otherwise', () => {
  assert.equal(calc('sqrt ( - 2 )').text, '√2·i');
  assert.equal(calc('ln ( - 1 )').text, 'π·i');                            // principal branch: +pi i
  assert.equal(calc('( - 8 ) ^ ( 1 / 3 )').text, '1+√3·i');
  const eipi = MathCore.evaluateComplex(T('e ^ ( i π )'), C);
  within(eipi.re, -1); within(eipi.im, 0, 1e-15); assert.ok(eipi.exact && eipi.exact.re.n === -1n && eipi.exact.im.n === 0n);   // exact: e^(iπ) = -1
  assert.equal(calc('e ^ ( i π )').text, '-1');
  const s = MathCore.evaluateComplex(T('sin ( i )'), C);
  within(s.im, Math.sinh(1)); within(s.re, 0);
});

test('real mode still refuses i and negative square roots', () => {
  const real = {...C, domain: 'real'};
  assert.equal(Calculator.compute(T('sqrt ( - 4 )'), real, true).text, '= undefined');
  assert.equal(Calculator.compute(T('i ^ ( 2 )'), real, true).text, '= unsupported');
  assert.equal(Calculator.compute(T('x ^ ( 2 ) + 1 = 0'), real, true).text, 'S=∅');
});

test('equations: every complex root, exact when the polynomial allows', () => {
  assert.equal(calc('x ^ ( 2 ) + 1 = 0').text, 'x=-i, i');
  assert.equal(calc('x ^ ( 2 ) + 4 x + 5 = 0').text, 'x=-2-i, -2+i');
  assert.equal(calc('x ^ ( 3 ) = 1').text, 'x=-1/2-√3/2·i, -1/2+√3/2·i, 1');
  assert.equal(calc('x ^ ( 3 ) - 6 x ^ ( 2 ) + 11 x = 6').text, 'x=1, 2, 3');         // all-real roots print as before
  assert.equal(calc('( x ^ ( 2 ) + 1 ) / ( x - 1 ) = 0').text, 'x=-i, i');
  assert.equal(calc('( x ^ ( 2 ) + 1 ) / ( x ^ ( 2 ) + 1 ) = 0').text, 'S=∅');
  assert.equal(calc('x ^ ( 2 ) + 2 = 0').text, 'x=-√2·i, √2·i');
  assert.equal(calc('x ^ ( 4 ) = - 1').text.split(', ').length, 4);
  assert.equal(calc('2 ^ ( x ) = 8').text, '= unsupported');                           // infinitely many complex solutions
});

test('property: complexRoots really are roots (residual) and conjugate-symmetric', () => {
  let seed = 99;
  const rnd = n => (seed = (seed * 1103515245 + 12345) & 0x7fffffff) % n;
  for (let t = 0; t < 40; t++) {
    const deg = 2 + rnd(5), c = Array.from({length: deg + 1}, () => rnd(11) - 5);
    if (!c[deg]) c[deg] = 1;
    const roots = Poly.complexRoots(c.map(x => Poly.q(BigInt(x))));
    for (const r of roots) {
      let re = 0, im = 0, pr = 1, pi = 0;
      for (let i = 0; i <= deg; i++) { re += c[i] * pr; im += c[i] * pi; [pr, pi] = [pr * r.re - pi * r.im, pr * r.im + pi * r.re]; }
      assert.ok(Math.hypot(re, im) < 1e-7 * Math.max(1, ...c.map(Math.abs)) * Math.max(1, Math.hypot(r.re, r.im)) ** deg, `${c} root ${r.re}+${r.im}i`);
      if (r.im !== 0) assert.ok(roots.some(u => Math.abs(u.re - r.re) < 1e-9 && Math.abs(u.im + r.im) < 1e-9), 'conjugate missing');
    }
  }
});

test('conjugate, argument and e^(i q π)', () => {
  assert.equal(calc('conj ( 3 + 4 i )').text, '3-4i');                                  // exact
  assert.equal(calc('conj ( ( 1 + 2 i ) * ( 3 - i ) )').text, '5-5i');
  assert.equal(calc('e ^ ( i π / 2 )').text, 'i');
  assert.equal(calc('e ^ ( - i π / 2 )').text, '-i');
  assert.equal(calc('e ^ ( 3 i π )').text, '-1');
  assert.equal(calc('e ^ ( i π ) + 1').text, '0');
  assert.equal(calc('arg ( 1 + 2 i )').text, '≈1.107148718');                           // not a multiple of π: numeric, marked
  assert.equal(calc('arg ( - 1 )').text, 'π');
  assert.equal(calc('arg ( 1 + i )').text, 'π/4');
  assert.equal(calc('arg ( - 1 - i )').text, '-3π/4');
  assert.equal(calc('arg ( i )').text, 'π/2');
  assert.throws(() => MathCore.evaluateComplex(T('arg ( 0 )'), C), e => e.code === 'undefined');
});

test('complex results with radicals are exact in the closed-form formats, approximate in decimal', () => {
  const f = t => calc(t, {fmt: 'frac'}).text;
  assert.equal(f('sqrt ( - 8 )'), '2√2·i');
  assert.equal(f('sqrt ( 2 ) + i'), '√2+i');
  assert.equal(f('( 1 + i ) / sqrt ( 2 )'), '√2/2+√2/2·i');
  assert.equal(f('e ^ ( i π / 3 )'), '1/2+√3/2·i');
  assert.equal(f('( - 8 ) ^ ( 1 / 3 )'), '1+√3·i');
  assert.equal(f('sqrt ( 2 ) - sqrt ( 3 ) i'), '√2-√3·i');
  assert.equal(f('sqrt ( 2 )'), '√2');
  assert.equal(calc('sqrt ( - 8 )', {fmt: 'dec'}).text, '2√2·i');   // the ℂ mode is exact whatever the decimal setting
  assert.equal(f('( 1 + 2 i ) ( 3 - i )'), '5+5i');                           // Gaussian rationals are unchanged
});

test('complex roots with radicals are exact', () => {
  for (const fmt of ['frac', 'dec']) {
    assert.equal(calc('x ^ ( 2 ) + x + 1 = 0', {fmt}).text, 'x=-1/2-√3/2·i, -1/2+√3/2·i');
    assert.equal(calc('( 2 x - 5 ) / x ^ ( 2 ) = 9', {fmt}).text, 'x=1/9-2√11/9·i, 1/9+2√11/9·i');
    assert.equal(calc('x ^ ( 2 ) + 3 = 0', {fmt}).text, 'x=-√3·i, √3·i');
  }
  assert.equal(calc('x ^ ( 2 ) - 2 = 0', {fmt: 'frac'}).text, 'x=-√2, √2');
});
