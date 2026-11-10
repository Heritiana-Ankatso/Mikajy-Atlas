#!/usr/bin/env python3
"""A zigzag scribbled over a finished reading (sequence recogniser) erases the line."""
import asyncio, json
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parents[1]
FIX=json.loads((ROOT/'tests/fixtures/seq_strokes.json').read_text())
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(headless=True); pg=await b.new_page(viewport={"width":800,"height":700})
        await pg.add_init_script("(() => { const r = performance.now.bind(performance); window.__ck = null; performance.now = () => window.__ck === null ? r() : window.__ck; localStorage.setItem('inkset', JSON.stringify({recogniser:'seq', fmt:'dec'})) })()")
        await pg.goto((ROOT/'android/assets/index.html').as_uri()); await pg.locator('#pad').wait_for()
        async def stroke(pts):
            await pg.mouse.move(*pts[0]); await pg.mouse.down()
            for q in pts[1:]: await pg.mouse.move(*q, steps=6)
            await pg.mouse.up(); await pg.wait_for_timeout(40)
        for s in FIX['strokes']: await stroke([(x,y) for x,y,_ in s])
        await pg.wait_for_function("() => lines.length && lines.every(L=>L.sk||!L.ink.length)&&!recBusy",timeout=40000)
        bb=await pg.evaluate("()=>{const q=lines[0].ink.map(bb);return [Math.min(...q.map(a=>a.x0)),Math.min(...q.map(a=>a.y0)),Math.max(...q.map(a=>a.x1)),Math.max(...q.map(a=>a.y1))]}")
        x0,y0,x1,y1=bb
        n=16; pts=[(x0+(x1-x0)*i/n, y0-6 if i%2==0 else y1+6) for i in range(n+1)]
        await stroke(pts); await pg.wait_for_timeout(600)
        left = await pg.evaluate("() => lines.length"); assert left == 0, left
        print('Scribble over a finished reading erases the line: PASS')
        # Erasing is exact: a zigzag over one glyph of the reading removes that character and nothing else (no neighbour, no leftover read as a new character)
        TOK = FIX['tokens'].split()                      # '2 4 \\div 9 7 + 1 9 - 8 - 6'
        async def fresh():
            await pg.evaluate("() => { lines.length = 0; kick() }")
            for s in FIX['strokes']:                       # the recorded pen times, which the model reads
                await pg.evaluate("t => window.__ck = t", s[0][2]); await pg.mouse.move(s[0][0], s[0][1]); await pg.mouse.down()
                for x,y,_ in s[1:]: await pg.mouse.move(x, y)
                await pg.evaluate("t => window.__ck = t", s[-1][2]); await pg.mouse.up(); await pg.wait_for_timeout(40)
            await pg.evaluate("() => window.__ck = null")
            await pg.wait_for_function("() => lines.length && lines.every(L=>L.sk||!L.ink.length)&&!recBusy",timeout=40000); await pg.wait_for_timeout(800)
        for name, k in [('first character', 0), ('division sign', 2), ('plus sign', 5), ('last character', 11), ('up-down-up over the second nine', 7)]:
            await fresh()
            bx = await pg.evaluate("k => gbox(lines[0].syms[k])", k)        # what is on screen: the glyph, which the handwriting under it only roughly matches
            if name.startswith('up-down-up'):     # two turns only: still an erasure, not a letter
                w = bx['x1']-bx['x0']; await stroke([(bx['x0']-2, bx['y1']+4), (bx['x0']+w/3, bx['y0']-4), (bx['x0']+2*w/3, bx['y1']+4), (bx['x1']+2, bx['y0']-4)])
            else:                                  # a hand: eight turns, overshooting the glyph by a few pixels each side
                await stroke([(bx['x0']-3+(bx['x1']-bx['x0']+6)*i/8, bx['y0']-4 if i%2==0 else bx['y1']+4) for i in range(9)])
            await pg.wait_for_timeout(600)
            await pg.wait_for_function("() => lines.length && lines.every(L=>L.sk||!L.ink.length)&&!recBusy",timeout=40000)
            rt = await pg.evaluate("() => lines.map(L=>L.rt).join('|')")
            want = ' '.join(TOK[:k] + TOK[k+1:])
            assert rt == want, (name, rt, want)
            print('Scribble over only the %s erases only it: PASS' % name.replace('up-down-up over the second nine', 'second nine (up-down-up)'))
        await b.close()
asyncio.run(main())
