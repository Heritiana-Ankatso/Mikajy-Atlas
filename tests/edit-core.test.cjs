'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const E = require('../web/edit-core.js');
const T = s => s.split(' ');
const N = s => E.normalise(T(s)).toks.join(' ');

test('normalise: one spelling for every reading', () => {
  assert.equal(N('{ 2 } ^ { 3 } + 1'), '2 ^ { 3 } + 1');
  assert.equal(N('2 ^ 3 4'), '2 ^ { 3 } 4');                                  // an exponent of one token is braced
  assert.equal(N('\\sqrt 9 + \\frac 1 2'), '\\sqrt { 9 } + \\frac { 1 } { 2 }');
  assert.equal(N('{ 2 + 1 } ^ { 2 }'), '{ 2 + 1 } ^ { 2 }');                    // the braces of a power's base say what is raised: kept
  assert.equal(N('2 x 3 ='), '2 \\times 3 =');                                  // x between two numbers is the multiplication sign
  assert.equal(N('2 x + 3'), '2 x + 3');
  assert.equal(N('x ^ { }'), 'x');
  assert.deepEqual(E.normalise(T('{ 2 } ^ 3'), [[{t: 'Z'}], [], [], [], [{t: '8'}]]).alts, [[], [], [], [{t: '8'}], []]);   // alternatives follow their token
});

// glyph boxes as the board lays out "√(12) + 4": the sign, 1, 2 under the bar (ending at 150), then + and 4
const ROOT = T('\\sqrt { 1 2 } + 4');
const ROOT_G = [{k: 0, c: '√', x0: 0, x1: 40, y0: 0, y1: 110, sx1: 45, vx: 150}, {k: 2, c: '1', x0: 55, x1: 95, y0: 40, y1: 100}, {k: 3, c: '2', x0: 100, x1: 145, y0: 40, y1: 100},
  {k: 5, c: '+', x0: 170, x1: 210, y0: 50, y1: 95}, {k: 6, c: '4', x0: 220, x1: 260, y0: 40, y1: 100}];
const box = (x0, x1, y0 = 40, y1 = 100) => ({x0, x1, y0, y1});

test('slot: under a root bar, past its end, before the sign', () => {
  assert.deepEqual(E.slot(ROOT, ROOT_G, box(150, 168)), {at: 4, del: 0});       // just past the last digit under the bar: carries on the radicand
  assert.deepEqual(E.slot(ROOT, ROOT_G, box(265, 300)), {at: 7, del: 0});       // after the 4
  assert.deepEqual(E.slot(ROOT, ROOT_G, box(-50, -10)), {at: 0, del: 0});       // in front of the root sign, not under it
  assert.deepEqual(E.slot(ROOT, ROOT_G, box(104, 141)), {at: 3, del: 1, over: true});
  assert.equal(E.slot(ROOT, ROOT_G, box(100, 140, 400, 460)), null);              // far below the line
});
test('slot: exponents', () => {
  const t = T('1 2 + 5'), G = [{k: 0, c: '1', x0: 0, x1: 40, y0: 40, y1: 100}, {k: 1, c: '2', x0: 45, x1: 85, y0: 40, y1: 100}, {k: 2, c: '+', x0: 95, x1: 135, y0: 50, y1: 95}, {k: 3, c: '5', x0: 145, x1: 185, y0: 40, y1: 100}];
  assert.deepEqual(E.slot(t, G, box(188, 205, 20, 55)), {at: 4, del: 0, sup: true});   // small and raised after the 5: its exponent
  assert.deepEqual(E.slot(t, G, box(190, 230)), {at: 4, del: 0});                      // level with the line: after it
  const p = T('5 ^ { 2 } + 1'), PG = [{k: 0, c: '5', x0: 0, x1: 40, y0: 40, y1: 100}, {k: 2, c: '2', x0: 42, x1: 62, y0: 20, y1: 55}, {k: 4, c: '+', x0: 80, x1: 120, y0: 50, y1: 95}, {k: 5, c: '1', x0: 130, x1: 170, y0: 40, y1: 100}];
  assert.deepEqual(E.slot(p, PG, box(64, 82, 20, 55)), {at: 3, del: 0});              // on into the exponent
  assert.deepEqual(E.slot(p, PG, box(-40, -5)), {at: 0, del: 0});
});
test('slot: numerator and denominator', () => {
  const t = T('\\frac { 2 } { 3 } + 1'), G = [{k: 0, c: '§', x0: 0, x1: 80, y0: 95, y1: 105}, {k: 2, c: '2', x0: 20, x1: 60, y0: 40, y1: 90}, {k: 5, c: '3', x0: 20, x1: 60, y0: 110, y1: 160}, {k: 7, c: '+', x0: 100, x1: 140, y0: 75, y1: 120}];
  assert.deepEqual(E.slot(t, G, box(64, 84, 40, 90)), {at: 3, del: 0});            // after the 2, above the bar
  assert.deepEqual(E.slot(t, G, box(64, 84, 110, 160)), {at: 6, del: 0});          // after the 3, below it
});
test('barOp: a root bar drawn further, a fraction bar under symbols', () => {
  assert.deepEqual(E.barOp(ROOT, ROOT_G, box(140, 270, -2, 2)), {kind: 'extend', root: 0, from: 4, to: 7, x: 270});
  const t = T('1 2'), G = [{k: 0, c: '1', x0: 0, x1: 40, y0: 40, y1: 100}, {k: 1, c: '2', x0: 45, x1: 85, y0: 40, y1: 100}];
  assert.deepEqual(E.barOp(t, G, box(-5, 90, 110, 114)), {kind: 'frac', s: 0, e: 2, part: 'n'});
  assert.equal(E.barOp(t, G, box(90, 130, 68, 72)), null);                         // a minus after the 2
});
test('apply: right to left, insertions in writing order', () => {
  const r = E.apply(T('1 2 + 3'), null, [{at: 1, toks: ['8'], x: 10}, {at: 1, toks: ['9'], x: 20}, {at: 2, del: 1, toks: ['-']}]);
  assert.equal(r.toks.join(' '), '1 8 9 2 - 3');
  assert.equal(r.alts.length, r.toks.length);
});
test('keeps: a re-reading that changed what was there is refused', () => {
  assert.equal(E.keeps(T('\\sqrt { 1 2 }'), T('\\sqrt { 1 2 } + 7'), 1), true);
  assert.equal(E.keeps(T('1 2 + 3 5'), T('1 2 + 3 5 = \\frac { a } { b }'), 1), false);
  assert.equal(E.keeps(T('1 2 + 3 5'), T('1 7 + 3 5 4'), 1), false);
});
