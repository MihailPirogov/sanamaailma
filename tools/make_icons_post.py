#!/usr/bin/env python3
"""Resize the rendered icon (tools/make_icons.js) into img/icon.png, legacy + round launcher PNGs and store icons."""
import os
from PIL import Image, ImageDraw
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sq = Image.open(R + '/release/art_src/icon_1024.png').convert('RGBA'); full = Image.open(R + '/release/art_src/icon_full_1024.png').convert('RGBA')
sq.resize((512, 512), Image.LANCZOS).save(R + '/img/icon.png', optimize=True)
m = Image.new('L', (1024, 1024), 0); ImageDraw.Draw(m).ellipse((0, 0, 1023, 1023), fill=255)
rnd = full.copy(); rnd.putalpha(m)
for d, s in {'mdpi': 48, 'hdpi': 72, 'xhdpi': 96, 'xxhdpi': 144, 'xxxhdpi': 192}.items():
    res = f'{R}/android/app/src/main/res/mipmap-{d}/'
    sq.resize((s, s), Image.LANCZOS).save(res + 'ic_launcher.png', optimize=True)
    rnd.resize((s, s), Image.LANCZOS).save(res + 'ic_launcher_round.png', optimize=True)
# store icons: full-bleed square (stores apply their own mask)
full.convert('RGB').resize((512, 512), Image.LANCZOS).save(R + '/release/art_src/icon_store_512.png', optimize=True)
print('icons ok')
