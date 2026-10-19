#!/usr/bin/env python3
"""Store + site assets from release/art_src/*_raw.png (render.js), the icon (tools/make_icons.js) and the screenshots (test/shots_release.js [play]).
-> release/play_assets, rustore_assets, yandex_assets (icon/cover), store/ (for GitHub), site_stage/out/{sanamaailma-igra/img,blog/media}."""
from PIL import Image
import os, shutil, glob
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(R + '/release')
A = 'art_src/'
for d in ['play_assets', 'rustore_assets', 'yandex_assets', 'store/screenshots']: os.makedirs(d, exist_ok=True)
feat = Image.open(A + 'feature_raw.png').convert('RGB'); feat.save('play_assets/feature_graphic_1024x500.png'); feat.save('store/feature_graphic_1024x500.png')
ic = Image.open(A + 'icon_store_512.png').convert('RGB')
for p in ['play_assets/play_icon_512.png', 'rustore_assets/icon_512.png', 'yandex_assets/icon_512x512.png', 'store/icon_512.png']: ic.save(p)
Image.open(A + 'banner_raw.png').convert('RGB').save('rustore_assets/banner_1920x1080.png')
Image.open(A + 'cover_raw.png').convert('RGB').save('yandex_assets/cover_800x470.png')
for f in glob.glob('rustore_assets/mobile_*.png'): os.remove(f)
for a, b in {'2_game': '1_game', '3_card': '2_card', '4_map': '3_map', '5_daily': '4_daily', '6_spin': '5_spin', '7_home': '6_home'}.items():
    shutil.copy(f'play_assets/screenshots/phone_{a}.png', f'rustore_assets/mobile_{b}.png')
for f in glob.glob('play_assets/screenshots/*.png'): shutil.copy(f, 'store/screenshots/')
S = R + '/site_stage/out/sanamaailma-igra/img/'; B = R + '/site_stage/out/blog/media/'
os.makedirs(S, exist_ok=True); os.makedirs(B, exist_ok=True)
for k in ['tutorial', 'game', 'card', 'map', 'daily', 'spin', 'home']:
    f = glob.glob(f'play_assets/screenshots/phone_*_{k}.png')[0]
    Image.open(f).convert('RGB').resize((540, 960), Image.LANCZOS).save(S + f'screen-{k}.webp', quality=84)
for k, n in [('game', '2_game'), ('card', '3_card')]:
    Image.open(f'yandex_assets/screenshot_desktop_{n}.png').convert('RGB').resize((1280, 720), Image.LANCZOS).save(S + f'desktop-{k}.webp', quality=84)
feat.save(S + 'feature-graphic.webp', quality=88)
Image.open(A + 'icon_1024.png').convert('RGBA').resize((256, 256), Image.LANCZOS).save(S + 'logo.webp', quality=90)
og = Image.open(A + 'og_raw.png').convert('RGB'); og.save(S + 'og-sanamaailma.jpg', quality=88); og.save(B + 'sanamaailma.jpg', quality=88)
Image.open(A + 'banner_raw.png').convert('RGB').resize((960, 540), Image.LANCZOS).save(B + 'sanamaailma-thumb.webp', quality=84)
feat.resize((int(1024 * 320 / 500), 320), Image.LANCZOS).crop((0, 0, 480, 320)).save(S + 'kartochka-sanamaailma.webp', quality=86)
Image.open(A + 'showcase_raw.png').convert('RGB').save('yandex_assets/cover_showcase_1560x520.png')
os.makedirs('play_assets/tablet', exist_ok=True); os.makedirs('rustore_assets/tablet', exist_ok=True)
for f in glob.glob('yandex_assets/screenshot_desktop_*.png'):   # 1920x1080 landscape = 7"/10" tablet screenshots (no ads)
    n = os.path.basename(f).replace('screenshot_desktop_', 'tablet_'); shutil.copy(f, 'play_assets/tablet/' + n); shutil.copy(f, 'rustore_assets/tablet/' + n)
print('assets ok')
