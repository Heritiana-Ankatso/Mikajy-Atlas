#!/usr/bin/env python3
"""Thickens a TrueType font's outlines and writes the result (the app's hand.woff2 is this, then subset to the characters in use).

    python3 tools/embolden_font.py PatrickHand-Regular.ttf out.ttf 30

The third argument is the stroke width in font units (1000 per em) added around every outline, half on each side; 30 gives the
shipped weight. Advance widths are untouched, so the layout stays identical to the regular face.
Needs fontTools and skia-pathops (both permissively licensed; used at build time only, nothing is bundled)."""
import sys
import pathops
from fontTools.ttLib import TTFont
from fontTools.pens.ttGlyphPen import TTGlyphPen
from pathops import Path, LineCap, LineJoin

src, dst, width = sys.argv[1], sys.argv[2], float(sys.argv[3])
font = TTFont(src)
glyphs, glyf = font.getGlyphSet(), font['glyf']
for name in font.getGlyphOrder():
    if glyf[name].isComposite():
        continue
    path = Path()
    glyphs[name].draw(path.getPen())
    if not len(path):
        continue
    path.simplify(fix_winding=True, keep_starting_points=False)
    ring = Path(path)
    ring.stroke(width, LineCap.BUTT_CAP, LineJoin.MITER_JOIN, 3)   # a miter join: round joins would produce conics, which TrueType lacks
    pen = TTGlyphPen(None)
    pathops.union([path, ring], pen)
    glyf[name] = pen.glyph()
for table in ('hdmx', 'LTSH', 'VDMX', 'gasp'):   # tables that describe the old outlines
    if table in font:
        del font[table]
font.save(dst)
