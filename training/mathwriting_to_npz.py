"""MathWriting InkML -> the npz format of gen_corpus.py (research branch only: MathWriting is CC BY-NC-SA 4.0).
python3 -I training/mathwriting_to_npz.py --src DIR/mathwriting-2024 --out DIR --workers 12 [--splits train,valid,test]
Keeps only expressions made of symbols the calculator understands and rewrites their LaTeX to the synthetic corpus' conventions
({x}^{2} for powers, \\left( ... \\right) for brackets) so both corpora share one vocabulary."""
import argparse, os, re, sys, time
import xml.etree.ElementTree as ET
from multiprocessing import Pool
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from strokefeat import featurise, tokenize, TOKEN_RE

NS = '{http://www.w3.org/2003/InkML}'
SINGLE = set('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+-=.,!%/<>')
WORDS = {r'\times', r'\div', r'\pi', r'\sin', r'\cos', r'\tan', r'\ln', r'\log', r'\exp', r'\sim', r'\le', r'\ge', r'\prime'}
SCRIPT1 = set('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
OPEN = {'(': ')', '[': ']'}
CLOSE = {v: k for k, v in OPEN.items()}
MAXS, MAXTOK = 160, 120


class Skip(Exception):
    pass


def parse_group(tk, i):
    """tk[i] == '{' -> (tokens, index after the closing brace)"""
    if i >= len(tk) or tk[i] != '{': raise Skip('group')
    out, i = parse_seq(tk, i + 1, '}')
    return out, i + 1


def parse_seq(tk, i, stop):
    """Parses atoms up to the token `stop` (None = end of input); returns (tokens, index of stop)."""
    out = []
    while True:
        if i >= len(tk):
            if stop is None: return out, i
            raise Skip('unbalanced')
        if tk[i] == stop: return out, i
        atom, i = parse_atom(tk, i)
        while i < len(tk) and tk[i] in ('^', '_'):
            kind = tk[i]
            if tk[i + 1:i + 2] == ['{']: arg, i = parse_group(tk, i + 1)
            elif i + 1 < len(tk) and tk[i + 1] in SCRIPT1: arg, i = [tk[i + 1]], i + 2
            else: raise Skip('script')
            atom = ['{'] + atom + ['}', kind, '{'] + arg + ['}']
        out += atom


def parse_atom(tk, i):
    t = tk[i]
    if t in SINGLE or t in WORDS: return [t], i + 1
    if t == r'\frac':
        a, j = parse_group(tk, i + 1); b, j = parse_group(tk, j)
        return [r'\frac', '{'] + a + ['}', '{'] + b + ['}'], j
    if t == r'\overline':
        a, j = parse_group(tk, i + 1)
        return [r'\overline', '{'] + a + ['}'], j
    if t == r'\sqrt':
        a, j = parse_group(tk, i + 1)
        return [r'\sqrt', '{'] + a + ['}'], j
    if t == '{':
        a, j = parse_group(tk, i)
        return ['{'] + a + ['}'], j
    if t in OPEN:
        a, j = parse_seq(tk, i + 1, OPEN[t])
        return [r'\left' + t] + a + [r'\right' + OPEN[t]], j + 1
    raise Skip(t)


FUNC_WORDS = ('sin', 'cos', 'tan', 'cot', 'sec', 'csc', 'log', 'exp', 'ln')
DROP_RUNS = ('sqrt', 'min', 'max', 'arrow', 'lim', 'det', 'mod')   # spelled-out words whose structure differs from the corpus' conventions


def fix_words(out):
    """MathWriting often spells functions as plain letters (l o g x): rewrite them as \\log x like the synthetic corpus; drop labels with other spelled-out words."""
    res, i = [], 0
    while i < len(out):
        if len(out[i]) == 1 and out[i].isalpha() and out[i].islower():
            j = i
            while j < len(out) and len(out[j]) == 1 and out[j].isalpha() and out[j].islower(): j += 1
            run = ''.join(out[i:j])
            if any(w in run for w in DROP_RUNS): raise Skip('word')
            k = 0
            while k < len(run):
                w = next((w for w in FUNC_WORDS if run.startswith(w, k)), None)
                if w: res.append('\\' + w); k += len(w)
                else: res.append(run[k]); k += 1
            i = j
        else:
            res.append(out[i]); i += 1
    return res


def convert(label):
    """-> LaTeX tokens in the synthetic corpus' conventions, or raises Skip"""
    tk = TOKEN_RE.findall(label.replace(r'\left', '').replace(r'\right', ''))
    out, _ = parse_seq(tk, 0, None)
    return fix_words(out)


def read_inkml(path):
    root = ET.parse(path).getroot()
    label = norm = None
    for an in root.iter(NS + 'annotation'):
        if an.get('type') == 'normalizedLabel': norm = an.text
        elif an.get('type') == 'label': label = an.text
    strokes = []
    for tr in root.iter(NS + 'trace'):
        pts = [[float(v) for v in p.split()] for p in tr.text.strip().split(',')]
        if pts and all(len(p) == 3 for p in pts): strokes.append(pts)
    return (norm or label), strokes


def work(path):
    try:
        label, strokes = read_inkml(path)
        if not label or not strokes or len(strokes) > MAXS: return None
        toks = convert(label)
        if not toks or len(toks) > MAXTOK: return None
        P, T = featurise(strokes)
        if not np.isfinite(P).all() or not np.isfinite(T).all(): return None
        return P.astype(np.float16), T.astype(np.float16), ' '.join(toks), 'human', 'mathwriting'
    except (Skip, ET.ParseError, IndexError, ValueError, KeyError):
        return None


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--src', required=True); ap.add_argument('--out', required=True)
    ap.add_argument('--splits', default='train,valid,test'); ap.add_argument('--workers', type=int, default=12); ap.add_argument('--limit', type=int, default=0)
    a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
    names = {'train': 'train', 'valid': 'val', 'test': 'held'}
    for sp in a.splits.split(','):
        t0 = time.time(); d = os.path.join(a.src, sp)
        files = sorted(os.path.join(d, f) for f in os.listdir(d) if f.endswith('.inkml'))
        if a.limit: files = files[:a.limit]
        with Pool(a.workers) as pool: rows = [r for r in pool.imap(work, files, chunksize=64) if r]
        lens = np.array([len(r[0]) for r in rows])
        np.savez_compressed(os.path.join(a.out, names[sp] + '.npz'), P=np.concatenate([r[0] for r in rows]), T=np.concatenate([r[1] for r in rows]), lens=lens,
                            tok=np.array([r[2] for r in rows]), beh=np.array([r[3] for r in rows]), dom=np.array([r[4] for r in rows]))
        print(sp, 'kept', len(rows), 'of', len(files), f'({int(time.time() - t0)}s)', flush=True)
