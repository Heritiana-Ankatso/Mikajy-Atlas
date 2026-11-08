#!/usr/bin/env python3
"""Draws the Mikajy Max logo: the Mikajy mark (white M on a black / red rounded square with a diagonal sweep), pushed harder:
heavier forward-leaning M with a hard shadow and red glow, a layered double sweep, speed stripes and a slanted MAX plaque.
Writes branding/logo-max-512.png, branding/logo-max-1024.png and the 192 px launcher icon android/res/drawable/icon.png.
The MAX lettering uses Noto Sans Black Italic (SIL OFL) when installed; only the rendered PNGs are shipped."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops
S = 2048                                  # draw big, shrink for smooth edges
U = S / 1000.0
here = Path(__file__).resolve().parent
P = lambda pts: [(x * U, y * U) for x, y in pts]
RED, RED_D, RED_L, INK = (238, 49, 36), (150, 22, 20), (255, 112, 64), (20, 20, 20)

def bezier(p0, p1, p2, n=60):
    return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0], (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]) for t in [i / n for i in range(n + 1)]]

img = Image.new('RGB', (S, S), INK)
d = ImageDraw.Draw(img)
# red field: everything right of / below the sweep (same sweep as the Mikajy logo, from the top edge down to the left edge)
sweep = bezier((430, 0), (150, 170), (0, 560))
d.polygon(P(sweep + [(0, 1000), (1000, 1000), (1000, 0)]), fill=RED)
# Max: a second, darker sweep below it and a bright edge light, so the split reads as layered steel plates
sweep2 = bezier((560, 0), (260, 230), (0, 760))
d.polygon(P(sweep2 + [(0, 1000), (1000, 1000), (1000, 0)]), fill=RED_D)
sweep3 = bezier((500, 0), (190, 200), (0, 650))
ImageDraw.Draw(img).line(P(sweep3), fill=RED_L, width=int(9 * U))
d.polygon(P(sweep3 + sweep2[::-1]), fill=RED)
# speed stripes cutting in from the right
for k, (y, w) in enumerate([(120, 9), (165, 5), (205, 3)]):
    d.polygon(P([(1000, y), (700 - k * 60, y), (690 - k * 60, y + w), (1000, y + w)]), fill=(255, 140, 110))
# red glow behind the M
glow = Image.new('RGB', (S, S), (0, 0, 0)); gd = ImageDraw.Draw(glow)
gd.ellipse(P([(150, 190), (850, 760)]), fill=(255, 70, 40))
glow = glow.filter(ImageFilter.GaussianBlur(170))
img = ImageChops.add(img, Image.eval(glow, lambda v: int(v * 0.55)))
d = ImageDraw.Draw(img)

# the M: heavy, leaning forward (italic skew), with a hard black shadow and a red-orange rim
lean = lambda x, y: (x + (700 - y) * 0.16, y)
M = [(150, 700), (150, 235), (292, 235), (500, 505), (708, 235), (850, 235), (850, 700), (700, 700), (700, 430), (545, 650), (455, 650), (300, 430), (300, 700)]
Mp = [lean(x, y) for x, y in M]
shadow = [(x + 26, y + 30) for x, y in Mp]
d.polygon(P(shadow), fill=(0, 0, 0))
rim = ImageDraw.Draw(img)
rim.polygon(P([(x - 7, y - 7) for x, y in Mp]), fill=(255, 150, 90))
d.polygon(P(Mp), fill=(255, 255, 255))
# bevel: a light-grey lower half on each stem gives the letter weight
d.polygon(P([lean(x, y) for x, y in [(150, 520), (300, 520), (300, 700), (150, 700)]]), fill=(214, 214, 214))
d.polygon(P([lean(x, y) for x, y in [(700, 520), (850, 520), (850, 700), (700, 700)]]), fill=(214, 214, 214))

# MAX plaque: slanted black plate with a red edge and three chevrons
plate = [(95, 745), (905, 745), (865, 905), (55, 905)]
d.polygon(P([(x + 14, y + 16) for x, y in plate]), fill=(0, 0, 0))
d.polygon(P(plate), fill=RED_L)
inner = [(112, 762), (888, 762), (853, 889), (77, 889)]
d.polygon(P(inner), fill=INK)
font = None
for f in ('/usr/share/fonts/google-noto/NotoSans-BlackItalic.ttf', '/usr/share/fonts/dejavu-sans-fonts/DejaVuSans-BoldOblique.ttf'):
    if Path(f).exists():
        font = ImageFont.truetype(f, int(122 * U)); break
if font:
    tw = d.textlength('MAX', font=font)
    d.text(((560 - tw / 2 + 25) * U - 0, 758 * U), 'MAX', font=font, fill=(255, 255, 255))
for k in range(3):                         # chevrons in the plaque's left end
    x = 140 + k * 46
    d.polygon(P([(x, 790), (x + 28, 790), (x + 52, 825), (x + 28, 860), (x, 860), (x + 24, 825)]), fill=RED if k < 2 else RED_L)

# rounded square mask (same proportions as the Mikajy mark)
mask = Image.new('L', (S, S), 0)
ImageDraw.Draw(mask).rounded_rectangle([0, 0, S - 1, S - 1], radius=int(S * 0.2), fill=255)
out = Image.new('RGBA', (S, S), (0, 0, 0, 0)); out.paste(img.convert('RGBA'), (0, 0), mask)
for size, path in ((1024, here / 'logo-max-1024.png'), (512, here / 'logo-max-512.png')):
    out.resize((size, size), Image.Resampling.LANCZOS).save(path, optimize=True)
# Android 5 launchers expect a square legacy icon; the original is RGB on a black corner, keep that convention
flat = Image.new('RGB', (S, S), (0, 0, 0)); flat.paste(out, (0, 0), out)
flat.resize((192, 192), Image.Resampling.LANCZOS).save(here.parent / 'android/res/drawable/icon.png', optimize=True)
print('Mikajy Max logo written')
