#!/usr/bin/env python3
"""Erasing in a finished reading (sequence recogniser): what you scribble over goes, and nothing erased comes back or appears from nowhere.

Each case once failed: an erased character came back when the line was next read from its (hidden) handwriting; a scribble over a fraction bar or a
root sign was read as handwriting (the line became 2/1 - 1/3, or a W appeared under the root); a scribble over an answer did nothing; a row of a
two-row reading was erased on screen only."""
import asyncio, math
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[1]
PAGE = (ROOT / "android/assets/index.html").as_uri()


def arc(cx, cy, r, a0, a1, n=10):
    return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)), cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]


def line(a, b, n=8):
    return [(a[0] + (b[0] - a[0]) * i / n, a[1] + (b[1] - a[1]) * i / n) for i in range(n + 1)]


SHAPES = {   # strokes in a box 0..0.6 wide and 0..1 tall (y down)
    "1": [line((.15, .25), (.4, 0), 4) + line((.4, 0), (.4, 1), 8)[1:]],
    "2": [arc(.3, .27, .25, 200, 380, 10) + line((.55, .3), (.02, 1), 8)[1:] + line((.02, 1), (.6, 1), 6)[1:]],
    "3": [arc(.28, .25, .24, 210, 450, 10) + arc(.28, .73, .26, 270, 500, 10)[1:]],
    "5": [line((.55, 0), (.1, 0), 5) + line((.1, 0), (.05, .45), 5)[1:] + arc(.3, .68, .3, 230, 480, 12)[1:]],
    "7": [line((0, 0), (.6, 0), 6) + line((.6, 0), (.2, 1), 8)[1:]],
    "+": [line((0, .55), (.6, .55), 6), line((.3, .25), (.3, .85), 6)],
    "=": [line((0, .38), (.6, .38), 6), line((0, .68), (.6, .68), 6)],
}


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        pg = await browser.new_page(viewport={"width": 900, "height": 700})
        errors = []
        pg.on("pageerror", lambda e: errors.append(str(e)))
        await pg.add_init_script("localStorage.setItem('inkset', JSON.stringify({recogniser: 'seq', fmt: 'dec'}))")
        await pg.goto(PAGE); await pg.locator("#pad").wait_for()

        async def stroke(pts):
            await pg.mouse.move(*pts[0]); await pg.mouse.down()
            for q in pts[1:]:
                await pg.mouse.move(*q)
            await pg.mouse.up(); await pg.wait_for_timeout(30)

        async def char(c, x, y, h=70):
            for s in SHAPES[c]:
                await stroke([(x + px * h, y - h + py * h) for px, py in s])

        async def settle():
            await pg.wait_for_timeout(900)
            await pg.wait_for_function("() => !recBusy && hold.length==0 && lines.every(L=>!L.ink.some(t=>!t.read)) && lines.every(L=>L.sk||!L.ink.length)", timeout=60000)
            await pg.wait_for_timeout(600)

        async def clear():
            await pg.evaluate("() => { lines.length = 0; setView(0, 0, 1); kick() }")

        async def fraction(num):
            """num over sqrt(3), then =, read in one go."""
            await clear()
            for i, c in enumerate(num):
                await char(c, 150 + i * 50, 262)
            await stroke(line((120, 290), (160 + len(num) * 50, 290), 12))
            hook = line((130, 364), (141, 357), 3) + line((141, 357), (157, 400), 5)[1:] + line((157, 400), (180, 310), 8)[1:]
            await stroke(hook + line((180, 310), (275, 310), 8)[1:])
            await char("3", 195, 397); await char("=", 330, 318, 45)
            await settle()
            assert await reading() == r"\frac { 2 1 } { \sqrt { 3 } } =", await reading()

        async def plain(text):
            await clear()
            for i, c in enumerate(text):
                await char(c, 120 + i * 50, 250)
            await settle()

        async def box(c, nth=0, row=None):
            """Screen box of a glyph c (row: index of a reading's extra row), or of the answer (c = 'ans')."""
            return await pg.evaluate("""([c, nth, row]) => { const L = lines.find(L => !L.kidOf), R = row === null ? L : L.kids[row];
                const bs = c === 'ans' ? R.ans.map(gbox) : [gbox(R.syms.filter(g => ch(g) == c)[nth])];
                return {x0: Math.min(...bs.map(b => b.x0)) * V.k + V.x, x1: Math.max(...bs.map(b => b.x1)) * V.k + V.x,
                        y0: Math.min(...bs.map(b => b.y0)) * V.k + V.y, y1: Math.max(...bs.map(b => b.y1)) * V.k + V.y} }""", [c, nth, row])

        async def scribble(q):
            await stroke([(q["x0"] - 3 + (q["x1"] - q["x0"] + 6) * i / 8, q["y0"] - 4 if i % 2 == 0 else q["y1"] + 4) for i in range(9)])
            await settle()

        async def reading():
            return await pg.evaluate("() => lines.filter(L => !L.kidOf).map(L => L.toks.join(' ')).join(' | ')")

        async def check(name, want):
            got = await reading()
            assert got == want, (name, got, want)
            print(f"{name}: PASS")

        await fraction("21")
        await scribble(await box("2"))
        await check("Erasing the 2 of 21 in a fraction", r"\frac { 1 } { \sqrt { 3 } } =")
        q = await box("=")
        await char("7", q["x1"] + 160, q["y1"] + 10); await settle()
        await check("Writing after it does not bring the erased 2 back", r"\frac { 1 } { \sqrt { 3 } } = 7")

        await fraction("21")
        await scribble(await box("§"))
        await check("A scribble over a fraction bar erases the fraction (and is not read as writing)", "=")

        await fraction("21")
        await scribble(await box("√"))
        await check("A scribble over a root sign erases the sign only (no W appears)", r"\frac { 2 1 } { 3 } =")

        await plain("12+35=")
        assert await reading() == "1 2 + 3 5 =", await reading()
        await scribble(await box("ans"))
        assert await pg.evaluate("() => lines.length") == 0, await reading()
        print("A scribble over the answer erases the calculation: PASS")

        await plain("12+35=")
        await scribble(await box("3"))
        await check("Erasing the 3 of 12+35=", "1 2 + 5 =")
        q = await box("=")
        await char("7", q["x1"] + 20, q["y1"]); await settle()
        await check("Writing after it does not bring the 3 back", "1 2 + 5 = 7")

        await plain("12+3")
        await pg.evaluate("() => { const L = lines[0]; applyReading(L, ['1', '2', '<nl>', '5', '7']); L.sk = inkKey(L.ink); kick() }")
        await pg.wait_for_timeout(400)
        await scribble(await box("5", 0, 0))
        await check("Erasing on the second row of a two-row reading changes the reading itself", "1 2 <nl> 7")
        q = await box("2")
        await char("1", q["x1"] + 30, q["y1"]); await settle()
        await check("Writing after it goes into its own row and does not bring the erased symbol back", "1 2 1 <nl> 7")

        assert not errors, errors
        await browser.close()


asyncio.run(main())
