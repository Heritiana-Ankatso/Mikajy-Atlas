'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const Calculator = require('../web/calculator.js');
const Core = require('../web/math-core.js');
const SET = {mode: 'instant', angle: 'rad', fmt: 'frac', domain: 'real', lang: 'fr'};
const solve = (s, set = {}) => { const r = Calculator.compute(s.split(' '), {...SET, ...set}, false); return r && r.text; };

test('polynomial inequalities: exact endpoints, brackets by language', () => {
  assert.equal(solve('x ^ ( 2 ) - 4 < 0'), 'S=]-2 ; 2[');
  assert.equal(solve('x ^ ( 2 ) - 4 < 0', {lang: 'en'}), 'S=(-2, 2)');
  assert.equal(solve('x ^ ( 2 ) ≥ 4'), 'S=]-∞ ; -2] ∪ [2 ; +∞[');
  assert.equal(solve('3 * x + 1 ≤ 7'), 'S=]-∞ ; 2]');
  assert.equal(solve('( x - 1 ) ^ ( 2 ) ≤ 0'), 'S={1}');                  // a double root satisfies ≤ only at the root
  assert.equal(solve('x ^ ( 2 ) + 1 > 0'), 'S=ℝ');
  assert.equal(solve('x ^ ( 2 ) < 0'), 'S=∅');
  assert.equal(solve('x < = 3'), 'S=]-∞ ; 3]');                           // "<" then "=" strokes are read as ≤
});
test('irrational endpoints are exact, with no decimal beside them', () => {
  assert.equal(solve('x ^ ( 2 ) - 2 < 0'), 'S=]-√2 ; √2[');
  assert.ok(!solve('x ^ ( 2 ) - 2 < 0').includes('≈'));
  assert.ok(solve('x ^ ( 2 ) - 2 < 0', {fmt: 'dec'}).includes('≈-1.414'));  // decimals only when asked
});
test('rational inequalities: poles are open, roots follow the sign', () => {
  assert.equal(solve('( x - 1 ) / ( x + 2 ) ≥ 0'), 'S=]-∞ ; -2[ ∪ [1 ; +∞[');
  assert.equal(solve('1 / x > 0'), 'S=]0 ; +∞[');
  assert.equal(solve('1 / ( x ^ ( 2 ) - 2 ) > 0'), 'S=]-∞ ; -√2[ ∪ ]√2 ; +∞[');
});
test('exponential, logarithm, root and absolute value', () => {
  assert.equal(solve('2 ^ x > 8'), 'S=]3 ; +∞[');
  assert.equal(solve('abs ( x - 1 ) < 2'), 'S=]-1 ; 3[');
  assert.equal(solve('ln ( x ) < 1'), 'S=]0 ; e[');
  assert.equal(solve('sqrt ( x ) ≤ 2'), 'S=[0 ; 4]');
  assert.equal(solve('sqrt ( x - 3 ) ≥ 1'), 'S=[4 ; +∞[');
});
test('constants: True / False; periodic inequalities are refused, not guessed', () => {
  assert.equal(solve('3 < 5', {lang: 'en'}), 'True');
  assert.equal(solve('2 > 7', {lang: 'en'}), 'False');
  assert.equal(solve('sin ( x ) > 0'), null);
  assert.throws(() => Core.inequality(['sin', '(', 'x', ')'], '>', ['0']), e => e.code === 'unsupported');
});
test('on demand, an inequality waits for the "="', () => {
  assert.equal(Calculator.compute('x ^ ( 2 ) < 4'.split(' '), {...SET, mode: 'demand'}, false), null);
  assert.equal(Calculator.compute('x ^ ( 2 ) < 4'.split(' '), {...SET, mode: 'demand'}, true).text, 'S=]-2 ; 2[');
});
