#!/usr/bin/env python3
"""Writing into a structured reading (a fraction with a root under it), sequence recogniser.

2/sqrt(3) is written and read; then, aiming at the symbols on screen as a finger would: a 1 before the 2, a 1 after it, a 4 over it,
a 1 after the 3 under the root, and a scribble over the 2 of 21. Each edit must land in that row of the fraction (or the root), not after
the whole fraction, and must leave the rest of the reading as it was."""
import asyncio, math
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[1]
PAGE = (ROOT / "android/assets/index.html").as_uri()


def arc(cx, cy, r, a0, a1, n=10):
    return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)), cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]


def line(a, b, n=8):
    return [(a[0] + (b[0] - a[0]) * i / n, a[1] + (b[1] - a[1]) * i / n) for i in range(n + 1)]


# Each character: strokes in a box 0..0.6 wide and 0..1 tall (y down), drawn at height h with its bottom-left at (x, y).
SHAPES = {
    "1": [line((.15, .25), (.4, 0), 4) + line((.4, 0), (.4, 1), 8)[1:]],
    "2": [arc(.3, .27, .25, 200, 380, 10) + line((.55, .3), (.02, 1), 8)[1:] + line((.02, 1), (.6, 1), 6)[1:]],
    "3": [arc(.28, .25, .24, 210, 450, 10) + arc(.28, .73, .26, 270, 500, 10)[1:]],
    "4": [line((.45, 0), (0, .68), 7) + line((0, .68), (.6, .68), 6)[1:], line((.45, 0), (.45, 1), 8)],
    "=": [line((0, .38), (.6, .38), 6), line((0, .68), (.6, .68), 6)],
}


async def stroke(pg, pts):
    await pg.mouse.move(*pts[0]); await pg.mouse.down()
    for p in pts[1:]:
        await pg.mouse.move(*p)
    await pg.mouse.up(); await pg.wait_for_timeout(30)


async def char(pg, c, x, y, h):
    for s in SHAPES[c]:
        await stroke(pg, [(x + px * h, y - h + py * h) for px, py in s])


async def settle(pg):
    await pg.wait_for_timeout(900)
    await pg.wait_for_function("() => !recBusy && hold.length==0 && lines.every(L=>!L.ink.some(t=>!t.read)) && lines.every(L=>L.sk||!L.ink.length)", timeout=60000)
    await pg.wait_for_timeout(1200)   # the view may slide to keep the answer in sight


async def fraction(pg, num):
    """num over sqrt(3), then =, read in one go."""
    await pg.evaluate("() => { lines.length = 0; setView(0, 0, 1); kick() }")
    for i, c in enumerate(num):
        await char(pg, c, 150 + i * 50, 262, 70)
    await stroke(pg, line((120, 290), (160 + len(num) * 50, 290), 12))
    hook = line((130, 364), (141, 357), 3) + line((141, 357), (157, 400), 5)[1:] + line((157, 400), (180, 310), 8)[1:]
    await stroke(pg, hook + line((180, 310), (275, 310), 8)[1:])
    await char(pg, "3", 195, 397, 70)
    await char(pg, "=", 330, 318, 45)
    await settle(pg)


async def on_screen(pg, c):
    """Box of the glyph c of the first line, in screen pixels."""
    return await pg.evaluate("""c => { const g = lines[0].syms.find(g => ch(g) == c), b = gbox(g);
        return {x0: b.x0 * V.k + V.x, x1: b.x1 * V.k + V.x, y0: b.y0 * V.k + V.y, y1: b.y1 * V.k + V.y} }""", c)


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        pg = await browser.new_page(viewport={"width": 800, "height": 700})
        errors = []
        pg.on("pageerror", lambda e: errors.append(str(e)))
        await pg.add_init_script("localStorage.setItem('inkset', JSON.stringify({recogniser: 'seq', fmt: 'dec'}))")
        await pg.goto(PAGE); await pg.locator("#pad").wait_for()
        await fraction(pg, "2")
        RT = "() => lines.map(L => L.rt.replace(/ =$/, '')).join(' | ')"   # the reading, without the = that asks for the answer
        assert await pg.evaluate(RT) == r"\frac { 2 } { \sqrt { 3 } }", await pg.evaluate(RT)
        h = lambda q: q["y1"] - q["y0"]

        async def before(q): await char(pg, "1", q["x0"] - 8 - .6 * h(q), q["y1"], h(q))
        async def after(q): await char(pg, "1", q["x1"] + 8, q["y1"], h(q))
        async def over(q): await char(pg, "4", q["x0"] + .1 * h(q), q["y1"], .9 * h(q))
        async def scribble(q):
            await stroke(pg, [(q["x0"] - 3 + (q["x1"] - q["x0"] + 6) * i / 8, q["y0"] - 4 if i % 2 == 0 else q["y1"] + 4) for i in range(9)])
            await pg.wait_for_timeout(700)

        for name, num, at, act, want in [
                ("a 1 written before the 2 goes into the numerator, first", "2", "2", before, r"\frac { 1 2 } { \sqrt { 3 } }"),
                ("a 1 written after the 2 goes into the numerator, last", "2", "2", after, r"\frac { 2 1 } { \sqrt { 3 } }"),
                ("a 4 written over the 2 replaces it", "2", "2", over, r"\frac { 4 } { \sqrt { 3 } }"),
                ("a 1 written after the 3 goes under the root", "2", "3", after, r"\frac { 2 } { \sqrt { 3 1 } }"),
                ("a scribble over the 2 of 21 erases only the 2", "21", "2", scribble, r"\frac { 1 } { \sqrt { 3 } }")]:
            await fraction(pg, num)
            await act(await on_screen(pg, at))
            await settle(pg)
            got = await pg.evaluate(RT)
            assert got == want, (name, got, want)
            assert await pg.evaluate("() => lines[0].at") not in (None, ""), (name, "no answer")
            print(f"Fraction: {name}: PASS")
        assert not errors, errors
        await browser.close()


asyncio.run(main())
