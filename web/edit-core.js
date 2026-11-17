/* Editing a reading: where a character written into a finished line belongs.
 * A reading is the recogniser's LaTeX-like token list; on screen it is a set of glyphs. The two only roughly line up with the handwriting they
 * came from, so an edit is decided from what the user sees: the structure of the reading (rows, fractions, roots, exponents) and the boxes of its
 * glyphs. Pure functions on plain data, no DOM: the board (app.js) passes the tokens and the glyph boxes, and applies the edits it gets back.
 *
 * Glyph box: {k: index of the token the glyph came from, x0, x1, y0, y1, c: its character,
 *             sign glyphs only (√ ‾ §): sx1 = where the radicand starts, vx = where the bar ends}. */
const EditCore = (() => {
  'use strict';
  const ARGS = {'^': 1, '_': 1, '\\sqrt': 1, '\\overline': 1, '\\frac': 2};
  const OPERATOR = /^([+\-=<>,.(!|]|\\times|\\div|\\le|\\leq|\\ge|\\geq|\\ne|\\neq|\\equiv|\\sim|\\left|\\left\(|\\left\[)$/;
  const STRUCTURE = new Set(['{', '}', '^', '_', '\\frac', '\\sqrt', '\\overline', '\\left', '\\right']);

  /** index just after the matrix that starts at tokens[i] === '\begin' */
  function matrixEnd(tokens, i) {
    let e = i + 1;
    while (e < tokens.length && tokens[e] !== '\\end') e++;
    if (e >= tokens.length) return tokens.length;
    e++;
    if (tokens[e] === '{') { while (e < tokens.length && tokens[e] !== '}') e++; e++; }
    return Math.min(e, tokens.length);
  }

  /** One spelling for every reading, so that an edit is a plain splice: every argument of ^ _ \sqrt \overline \frac is a {group}, braces that
   *  group nothing are dropped (the board draws them as nothing and the engine reads through them), an exponent of nothing is dropped, and an x
   *  written between two numbers is the multiplication sign (2 x 3 is never algebra). `alts` (per-token alternatives) is kept in step.
   *  -> {toks, alts} */
  function normalise(tokens, alts) {
    const out = [], oa = [];
    let i = 0;
    const src = k => (alts && alts[k]) || [];
    const push = (t, a) => { out.push(t); oa.push(a || []); };
    function arg() {
      if (tokens[i] === '{') {
        push('{', src(i)); i++;
        seq(true);
        if (tokens[i] === '}') { push('}', src(i)); i++; } else push('}');
      } else {
        push('{');
        if (i < tokens.length && tokens[i] !== '}' && tokens[i] !== '<nl>') one();
        push('}');
      }
    }
    function one() {
      const t = tokens[i];
      if (t === '{') {
        let close = i;
        for (let d = 0; close < tokens.length; close++) { if (tokens[close] === '{') d++; else if (tokens[close] === '}' && --d === 0) break; }
        if (close - i > 2 && (tokens[close + 1] === '^' || tokens[close + 1] === '_')) {   // {2+1}^2: the braces say what is raised, they stay
          push('{', src(i)); i++; seq(true); if (tokens[i] === '}') { push('}', src(i)); i++; } else push('}');
          return;
        }
        i++; seq(true); if (tokens[i] === '}') i++; return;
      }
      if (t === '\\begin') { const e = matrixEnd(tokens, i); for (; i < e; i++) push(tokens[i], src(i)); return; }
      const at = out.length;
      push(t, src(i)); i++;
      for (let k = 0; k < (ARGS[t] || 0); k++) arg();
      if ((t === '^' || t === '_') && out.length === at + 3) { out.length = at; oa.length = at; }   // ^ { } raises nothing
    }
    function seq(inGroup) {
      while (i < tokens.length && !(inGroup && tokens[i] === '}')) {
        if (tokens[i] === '}') { i++; continue; }                    // a stray closing brace
        one();
      }
    }
    seq(false);
    for (let j = 1; j + 1 < out.length; j++) {
      if ((out[j] === 'x' || out[j] === 'X') && /^([0-9)}]|\\right[)\]])$/.test(out[j - 1]) && /^[0-9.]$/.test(out[j + 1])) out[j] = '\\times';
    }
    return {toks: out, alts: oa};
  }

  /* ---- Structure ------------------------------------------------------------------------------
   * A sequence {a, b, kind, items} is a run of items written side by side; a..b are the token positions something can be inserted at.
   * An item {s, e, kind, seqs} covers tokens s..e-1: a symbol, a word (\sin), or a container with its own sequences
   * (frac: numerator, denominator; sqrt / over: what is under the bar; sup / sub: the exponent or index). */
  function tree(tokens) {
    let i = 0;
    const rows = [];
    function group(kind) {
      if (tokens[i] !== '{') return {a: i, b: i, kind, items: []};
      i++;
      const s = seq(kind, true);
      if (tokens[i] === '}') i++;
      return s;
    }
    function item() {
      const s = i, t = tokens[i];
      if (t === '\\frac') { i++; const n = group('num'), d = group('den'); return {s, e: i, kind: 'frac', seqs: [n, d]}; }
      if (t === '\\sqrt' || t === '\\overline') { i++; return {s, kind: t === '\\sqrt' ? 'sqrt' : 'over', seqs: [group('rad')], e: i}; }
      if (t === '^' || t === '_') { i++; return {s, kind: t === '^' ? 'sup' : 'sub', seqs: [group(t === '^' ? 'sup' : 'sub')], e: i}; }
      if (t === '\\begin') { i = matrixEnd(tokens, i); return {s, e: i, kind: 'opaque', seqs: []}; }
      if (t === '{') { return {s, kind: 'grp', seqs: [group('grp')], e: i}; }
      if (t === '\\left' || t === '\\right') { i++; if (i < tokens.length && /^[()|]$/.test(tokens[i])) i++; return {s, e: i, kind: 'sym', seqs: []}; }
      i++;
      return {s, e: i, kind: 'sym', seqs: []};
    }
    function seq(kind, inGroup) {
      const q = {a: i, b: i, kind, items: []};
      while (i < tokens.length && tokens[i] !== '<nl>' && !(inGroup && tokens[i] === '}')) {
        if (tokens[i] === '}') { i++; continue; }
        q.items.push(item());
      }
      q.b = i;
      return q;
    }
    for (;;) {
      rows.push(seq('row', false));
      if (tokens[i] === '<nl>') i++; else break;
    }
    return rows;
  }

  const union = (a, b) => !a ? b : !b ? a : {x0: Math.min(a.x0, b.x0), y0: Math.min(a.y0, b.y0), x1: Math.max(a.x1, b.x1), y1: Math.max(a.y1, b.y1)};
  /** give every item its box on screen (union of its glyphs; a root reaches to the end of its bar) and its sign glyph */
  function measure(q, G) {
    for (const it of q.items) {
      it.box = null; it.sign = null;
      for (const g of G) {
        if (g.k < it.s || g.k >= it.e) continue;
        it.box = union(it.box, {x0: g.x0, y0: g.y0, x1: Math.max(g.x1, g.vx === undefined ? g.x1 : g.vx), y1: g.y1});
        if (g.k === it.s && (g.c === '√' || g.c === '§' || g.c === '‾')) it.sign = g;
      }
      it.seqs.forEach(s => measure(s, G));
    }
  }
  /** the items of a sequence that can be seen, in writing order; groups and indices are read through */
  function visible(q) {
    const out = [];
    for (const it of q.items) {
      if (it.kind === 'grp' || it.kind === 'sub') it.seqs.forEach(s => out.push(...visible(s)));
      else if (it.box) out.push(it);
    }
    return out;
  }
  const extent = q => visible(q).reduce((b, it) => union(b, it.box), null);
  const mid = b => (b.x0 + b.x1) / 2;

  /** Where a character written in box b goes: {at, del, over?, sup?}. `at` is a token position, `del` how many tokens it replaces (written over a
   *  symbol), `sup` says it is a new exponent of what stands before `at`. null: not clearly anywhere in this reading. */
  function slot(tokens, G, b) {
    const rows = tree(tokens);
    rows.forEach(r => measure(r, G));
    const cx = mid(b), cy = (b.y0 + b.y1) / 2, w = Math.max(8, b.x1 - b.x0), h = Math.max(8, b.y1 - b.y0);
    let row = null, rd = Infinity, re = null;
    for (const r of rows) {
      const e = extent(r);
      if (!e) continue;
      const d = cy < e.y0 ? e.y0 - cy : cy > e.y1 ? cy - e.y1 : 0;
      if (d < rd) { rd = d; row = r; re = e; }
    }
    if (!row) return rows.length ? {at: rows[0].a, del: 0} : null;
    if (rd > .75 * Math.max(h, .5 * (re.y1 - re.y0))) return null;      // well above or below every row

    function inSeq(q) {
      const its = visible(q);
      if (!its.length) return {at: q.a, del: 0};
      for (let n = 0; n < its.length; n++) {
        const it = its[n];
        if (it.kind === 'frac' && it.sign) {
          // above the bar is the numerator, below it the denominator; level with the bar is beside the fraction
          const bar = it.sign, by = (bar.y0 + bar.y1) / 2, nb = extent(it.seqs[0]), db = extent(it.seqs[1]), pad = .6 * w + 4;
          if (cx < bar.x0 - pad || cx > bar.x1 + pad) continue;
          if (cy < (nb ? nb.y0 : by - 1.2 * h) - .5 * h || cy > (db ? db.y1 : by + 1.2 * h) + .5 * h) continue;
          if (b.y1 <= by + .2 * h && cy < by - .15 * h) return inSeq(it.seqs[0]);
          if (b.y0 >= by - .2 * h && cy > by + .15 * h) return inSeq(it.seqs[1]);
          if (cx > bar.x0 && cx < bar.x1) return null;                  // right across the bar: unclear
        } else if ((it.kind === 'sqrt' || it.kind === 'over') && it.sign) {
          // under the bar is inside, past its end is outside: the bar on screen says how far the root reaches
          const sg = it.sign, empty = !extent(it.seqs[0]), end = sg.vx === undefined ? sg.x1 : sg.vx;
          const start = sg.x0 + .5 * ((sg.sx1 === undefined ? sg.x0 : sg.sx1) - sg.x0);
          // a character written just past the end of the bar, close to the last one under it, carries on the radicand (as on paper, the bar is
          // drawn on afterwards); one written a gap further is after the root
          if (cx > start && cx <= end + (empty ? 1.2 * Math.max(w, h) : .6 * Math.max(w, h)) && cy >= sg.y0 - .35 * h && cy <= sg.y1 + .35 * h) return inSeq(it.seqs[0]);
        } else if (it.kind === 'sup') {
          // on to an exponent: next to it, at its height, clear of the line the base stands on
          const B = it.box, bh = B.y1 - B.y0, prev = its[n - 1];
          const raised = !prev || b.y1 <= prev.box.y1 - .3 * (prev.box.y1 - prev.box.y0);
          if (raised && cx >= B.x0 - .3 * w && cx <= B.x1 + Math.max(w, bh) && cy >= B.y0 - .6 * bh && cy <= B.y1 + .35 * bh) return inSeq(it.seqs[0]);
        }
      }
      for (const it of its) {
        if (it.kind !== 'sym' || it.e !== it.s + 1) continue;
        const q2 = it.box, gw = q2.x1 - q2.x0, ov = Math.min(b.x1, q2.x1) - Math.max(b.x0, q2.x0), vo = Math.min(b.y1, q2.y1) - Math.max(b.y0, q2.y0);
        if (cx >= q2.x0 + .2 * gw && cx <= q2.x1 - .2 * gw && ov >= .5 * Math.min(w, gw) && vo >= .4 * Math.min(h, q2.y1 - q2.y0)) return {at: it.s, del: 1, over: true};
      }
      let j = 0;
      while (j < its.length && mid(its[j].box) < cx) j++;
      const left = its[j - 1];
      if (left && q.kind !== 'sup' && left.kind !== 'sup' && !(left.kind === 'sym' && OPERATOR.test(tokens[left.s])) && !(its[j] && its[j].kind === 'sup')) {
        // small and raised right after something: a new exponent
        const lb = left.box, lh = lb.y1 - lb.y0;
        if (h <= .8 * lh && b.y1 <= lb.y0 + .5 * lh && cy <= lb.y0 + .25 * lh && b.x0 - lb.x1 <= .9 * lh && b.x0 >= lb.x1 - .35 * w) return {at: left.e, del: 0, sup: true};
      }
      return {at: j < its.length ? its[j].s : q.b, del: 0};
    }
    return inSeq(row);
  }

  /** What a horizontal stroke (box b) drawn on a reading is, when it is not a minus sign:
   *  {kind: 'extend', root, from, to, x}: the bar of the root at token `root` drawn further, to x; its closing brace moves from `from` to before `to`;
   *  {kind: 'frac', s, e, part}: a fraction bar under (part 'n') or over (part 'd') the items of tokens s..e-1. null: neither. */
  function barOp(tokens, G, b) {
    const rows = tree(tokens);
    rows.forEach(r => measure(r, G));
    const cy = (b.y0 + b.y1) / 2;
    let ext = null;
    const roots = q => {
      q.items.forEach((it, n) => {
        if (it.kind === 'sqrt' && it.sign && !ext) {
          const sg = it.sign, sz = sg.y1 - sg.y0, end = sg.vx === undefined ? sg.x1 : sg.vx;
          if (Math.abs(cy - sg.y0) <= .3 * sz && b.x0 >= sg.x0 && b.x0 <= end + .5 * sz && b.x1 > end + .1 * sz) {
            let to = it.e;
            for (let k = n + 1; k < q.items.length; k++) { const nx = q.items[k]; if (nx.box && mid(nx.box) < b.x1) to = nx.e; else if (nx.box) break; }
            ext = {kind: 'extend', root: it.s, from: it.e - 1, to, x: b.x1};
          }
        }
        it.seqs.forEach(roots);
      });
    };
    rows.forEach(roots);
    if (ext) return ext;
    for (const r of rows) {
      const run = r.items.filter(it => it.box && mid(it.box) >= b.x0 && mid(it.box) <= b.x1);
      if (!run.length) continue;
      const box = run.reduce((u, it) => union(u, it.box), null), rh = box.y1 - box.y0;
      if (cy >= box.y1 - .12 * rh && cy <= box.y1 + rh) return {kind: 'frac', s: run[0].s, e: run[run.length - 1].e, part: 'n'};
      if (cy <= box.y0 + .1 * rh && cy >= box.y0 - rh) return {kind: 'frac', s: run[0].s, e: run[run.length - 1].e, part: 'd'};
    }
    return null;
  }

  /** The items of the first row whose middle lies between x0 and x1 (what a root sign drawn around existing writing covers): {s, e} or null. */
  function span(tokens, G, x0, x1) {
    const rows = tree(tokens);
    rows.forEach(r => measure(r, G));
    const run = rows[0].items.filter(it => it.box && mid(it.box) >= x0 && mid(it.box) <= x1);
    return run.length ? {s: run[0].s, e: run[run.length - 1].e} : null;
  }

  /** Apply edits [{at, del, toks, alts?, x}] (positions in the tokens as they are now): right to left so earlier positions hold; at one position a
   *  replacement goes first and insertions land before it, in the order they were written (by x). -> {toks, alts} */
  function apply(tokens, alts, edits) {
    const toks = tokens.slice(), al = tokens.map((_, k) => (alts && alts[k]) || []);
    const order = edits.slice().sort((p, q) => q.at - p.at || (q.del || 0) - (p.del || 0) || (q.x || 0) - (p.x || 0));
    for (const e of order) {
      toks.splice(e.at, e.del || 0, ...e.toks);
      al.splice(e.at, e.del || 0, ...e.toks.map((_, k) => (e.alts && e.alts[k]) || []));
    }
    return {toks, alts: al};
  }

  /** Did a re-reading of the whole line (after new strokes) keep what was there? Every digit and letter of the old reading must still be there, in
   *  order, and at most `added` new ones may have appeared. Signs and structure may change: a bar read as a minus becomes a fraction bar. */
  function keeps(oldTokens, newTokens, added) {
    const alnum = t => /^([0-9a-zA-Z]|\\pi)$/.test(t);
    const a = oldTokens.filter(alnum), b = newTokens.filter(alnum);
    let k = 0;
    for (const t of b) if (k < a.length && t === a[k]) k++;
    return k === a.length && b.length - a.length <= added;
  }

  /** How many top-level roots the first row has, in order: the token index of each. */
  function rootsOf(tokens) { return tree(tokens)[0].items.filter(it => it.kind === 'sqrt').map(it => it.s); }

  return Object.freeze({normalise, tree, slot, barOp, span, apply, keeps, rootsOf, STRUCTURE});
})();
if (typeof module !== 'undefined' && module.exports) module.exports = EditCore;
