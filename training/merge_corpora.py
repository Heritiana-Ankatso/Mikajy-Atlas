"""Concatenate gen_corpus-format npz files:  python3 merge_corpora.py OUT.npz A.npz[:repeat] B.npz[:repeat] ...  (repeat = integer upsampling factor)."""
import sys
import numpy as np


def main(out, specs):
    parts = []
    for s in specs:
        path, _, rep = s.partition(':'); z = np.load(path)
        P, T, lens, tok, beh, dom = (z[k] for k in ('P', 'T', 'lens', 'tok', 'beh', 'dom'))
        parts += [(P, T, lens, tok, beh, dom)] * int(rep or 1)
    cat = lambda i: np.concatenate([p[i] for p in parts])
    np.savez_compressed(out, P=cat(0), T=cat(1), lens=cat(2), tok=cat(3), beh=cat(4), dom=cat(5))
    print('wrote', out, len(cat(2)), 'samples')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2:])
