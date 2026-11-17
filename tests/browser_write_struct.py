#!/usr/bin/env python3
"""Writing into roots, powers and fractions, striking out, and writing on a line reopened from history (sequence recogniser).

Each case once failed: an = written after a root went under it (the answer lost its =), +7 written past a root's bar went inside it (as 127+),
a 3 written in front of a root went under it, an exponent written later was read as a digit on the line, a dash under a number was read as a
minus, a straight line through a calculation was read as a minus, and writing on a reopened history line replaced the whole line."""
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
    "4": [line((.45, 0), (0, .68), 7) + line((0, .68), (.6, .68), 6)[1:], line((.45, 0), (.45, 1), 8)],
    "5": [line((.55, 0), (.1, 0), 5) + line((.1, 0), (.05, .45), 5)[1:] + arc(.3, .68, .3, 230, 480, 12)[1:]],
    "7": [line((0, 0), (.6, 0), 6) + line((.6, 0), (.2, 1), 8)[1:]],
    "+": [line((0, .55), (.6, .55), 6), line((.3, .25), (.3, .85), 6)],
    "=": [line((0, .38), (.6, .38), 6), line((0, .68), (.6, .68), 6)],
}


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        pg = await browser.new_page(viewport={"width": 1000, "height": 700})
        errors = []
        pg.on("pageerror", lambda e: errors.append(str(e)))
        await pg.add_init_script("localStorage.setItem('inkset', JSON.stringify({recogniser: 'seq', fmt: 'frac'}))")
        await pg.goto(PAGE); await pg.locator("#pad").wait_for()

        async def stroke(pts):
            await pg.mouse.move(*pts[0]); await pg.mouse.down()
            for q in pts[1:]:
                await pg.mouse.move(*q)
            await pg.mouse.up(); await pg.wait_for_timeout(30)

        async def char(c, x, y, h=70):
            for s in SHAPES[c]:
                await stroke([(x + px * h, y - h + py * h) for px, py in s])

        async def text(t, x=120, y=250):
            for i, c in enumerate(t):
                await char(c, x + i * 50, y)

        async def root(x0, x1, ytop, ybot):
            h = ybot - ytop
            hook = line((x0, ytop + .6 * h), (x0 + .15 * h, ytop + .52 * h), 3) + line((x0 + .15 * h, ytop + .52 * h), (x0 + .3 * h, ybot), 5)[1:] + line((x0 + .3 * h, ybot), (x0 + .55 * h, ytop), 8)[1:]
            await stroke(hook + line((x0 + .55 * h, ytop), (x1, ytop), 10)[1:])

        async def settle():
            await pg.wait_for_timeout(900)
            await pg.wait_for_function("() => !recBusy && hold.length==0 && lines.every(L=>!L.ink.some(t=>!t.read)) && lines.every(L=>L.sk||!L.ink.length)", timeout=60000)
            await pg.wait_for_timeout(600)

        async def clear():
            await pg.evaluate("() => { lines.length = 0; setView(0, 0, 1); kick() }")

        async def box(c, nth=0, li=0):
            return await pg.evaluate("""([c, nth, li]) => { const L = lines.filter(L => !L.kidOf)[li];
                const bs = c === 'all' ? L.syms.map(gbox) : [gbox(L.syms.filter(g => ch(g) == c)[nth])];
                return {x0: Math.min(...bs.map(b => b.x0)) * V.k + V.x, x1: Math.max(...bs.map(b => b.x1)) * V.k + V.x,
                        y0: Math.min(...bs.map(b => b.y0)) * V.k + V.y, y1: Math.max(...bs.map(b => b.y1)) * V.k + V.y} }""", [c, nth, li])

        async def bar_end():
            return await pg.evaluate("() => { const g = lines[0].syms[0]; return [g.vtx * V.k + V.x, (g.ty - (g.ru || .8) * g.tsz) * V.k + V.y] }")

        async def check(name, want, answer=None, li=-1):
            got = await pg.evaluate("li => { const L = lines.filter(L => !L.kidOf).at(li); return [L.toks.join(' '), L.at] }", li)
            assert got[0] == want, (name, got, want)
            if answer is not None:
                assert got[1] == answer, (name, got, answer)
            print(f"{name}: PASS")

        await root(100, 420, 170, 260); await text("12+35", x=150, y=255); await settle()
        await check("A root over 12+35", r"\sqrt { 1 2 + 3 5 }", "=√47")
        q = await box("all"); await char("=", q["x1"] + 25, q["y1"] - 5, 45); await settle()
        await check("An = written after the root's bar is outside it", r"\sqrt { 1 2 + 3 5 } =", "√47")

        await clear(); await root(100, 260, 170, 260); await text("12", x=150, y=255); await settle()
        x, _ = await bar_end()
        await char("+", x + 25, 250, 60); await char("7", x + 85, 250); await settle()
        await check("+7 written past the bar is after the root", r"\sqrt { 1 2 } + 7", "=2√3+7")
        q = await box("√"); await char("3", q["x0"] - 60, 250); await settle()
        await check("A 3 written in front of the root multiplies it", r"3 \sqrt { 1 2 } + 7", "=6√3+7")

        await clear(); await root(100, 260, 170, 260); await text("12", x=150, y=255); await settle()
        x, y = await bar_end()
        await char("+", x + 25, 250, 60); await char("4", x + 85, 255); await settle()
        await stroke(line((x - 5, y), (x + 150, y), 12)); await settle()
        await check("The root's bar drawn further takes +4 under it", r"\sqrt { 1 2 + 4 }", "=4")

        await clear(); await text("12+5"); await settle()
        q = await box("5"); await char("2", q["x1"] + 4, q["y0"] + 20, 32); await settle()
        await check("A small 2 written up after the 5 is its exponent", "1 2 + 5 ^ { 2 }", "=37")

        await clear(); await text("12"); await settle()
        q = await box("all")
        await stroke(line((q["x0"] - 8, q["y1"] + 14), (q["x1"] + 8, q["y1"] + 14), 12)); await char("4", (q["x0"] + q["x1"]) / 2 - 20, q["y1"] + 90); await settle()
        await check("A bar under 12 with a 4 under it makes 12/4", r"\frac { 1 2 } { 4 }", "=3")

        await clear(); await text("12+35"); await settle()
        a = await box("2"); b = await box("3"); y = a["y0"] * .45 + a["y1"] * .55
        await stroke(line((a["x0"] - 5, y), (b["x1"] + 5, y), 20)); await settle()
        await check("A straight line through 2+3 strikes them out", "1 5")

        await clear()
        await pg.evaluate("() => openHist({id: 'h1', F: 70, syms: [{c: '√', sup: 0, cover: 2}, {c: '1', sup: 0}, {c: '6', sup: 0}, {c: '+', sup: 0}, {c: '1', sup: 0}]})")
        await pg.wait_for_timeout(800)
        q = await box("all"); await char("=", q["x1"] + 12, q["y1"] - 10, 40); await settle()
        await check("Writing on a line reopened from history edits it (nothing is lost)", r"\sqrt { 1 6 } + 1 =", "5")

        assert not errors, errors
        await browser.close()


asyncio.run(main())
