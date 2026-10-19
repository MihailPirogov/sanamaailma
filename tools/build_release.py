#!/usr/bin/env python3
"""Release builds of Sanamaailma (no test hooks, no test badge, no noindex). Ported from tatar-wow/tools/build_release.py.
  python3 tools/build_release.py yandex   -> release/build/yandex/ + release/sanamaailma-yandex.zip   (Yandex Games; nothing is uploaded)
  python3 tools/build_release.py android  -> android/app/src/main/assets/www/                       (then tools/build_android.sh)
"""
import os, re, sys, shutil, time, zipfile
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
target = sys.argv[1]
V = time.strftime('%Y%m%d%H%M')
out = {'yandex': 'release/build/yandex', 'android': 'android/app/src/main/assets/www'}[target]
shutil.rmtree(out, ignore_errors=True); os.makedirs(out)
for d in ('css', 'data', 'img', 'audio', 'fonts'):
    if os.path.isdir(d): shutil.copytree(d, os.path.join(out, d))
os.makedirs(os.path.join(out, 'js/adapters'))
for f in os.listdir('js'):
    if f.endswith('.js'): shutil.copy(os.path.join('js', f), os.path.join(out, 'js', f))
shutil.copy(f'js/adapters/{target}.js', os.path.join(out, f'js/adapters/{target}.js'))
shutil.copy('index.html', os.path.join(out, 'index.html'))

def edit(rel, fn):
    p = os.path.join(out, rel); s = open(p, encoding='utf-8').read(); s2 = fn(s)
    open(p, 'w', encoding='utf-8').write(s2)

def html(s):
    assert 'testBadge' not in s and 'noindex' not in s
    s = re.sub(r'\?v=[0-9a-z]+', '', s)   # drop the dev cache-buster, set the release one
    s = re.sub(r'(src|href)="((?:js|css|data)/[^"?]+)"', lambda m: f'{m.group(1)}="{m.group(2)}?v={V}"', s)
    s = re.sub(r"<script>window\.BUILD_V='[^']*';</script>\n?", '', s)
    pre = f'<script>window.RELEASE=true;window.BUILD_V="{V}";</script>\n'
    if target == 'yandex':
        pre = '<script src="/sdk.js"></script>\n' + pre
    s = s.replace('<script src="js/platform.js', pre + '<script src="js/platform.js', 1)
    s = re.sub(r'(<script src="js/platform\.js[^"]*"></script>)', lambda m: m.group(1) + f'\n<script src="js/adapters/{target}.js?v={V}"></script>', s, count=1)
    if target == 'yandex':
        s = s.replace('<a class="brand" id="hBrand" href="https://pirogovlab.ru" target="_blank" rel="noopener">Проект PirogovLab · pirogovlab.ru</a>',
                      '<a class="brand" id="hBrand">Проект PirogovLab</a>')
    return s
edit('index.html', html)

if target == 'yandex':
    # Yandex rule 8.4.2: no links / domains to external resources anywhere in UI texts
    SUBS = [('\'<a href="https://pirogovlab.ru/sanamaailma/privacy/" target="_blank" rel="noopener">Политика конфиденциальности</a>\'', "'Политика конфиденциальности'"),
            ('\'<a href="https://pirogovlab.ru" target="_blank" rel="noopener">PirogovLab</a>\'', "'PirogovLab'"),
            (' · pirogovlab.ru', ''), ('Викисловарь (ru.wiktionary.org)', 'Викисловарь'), ('Викисловаря (ru.wiktionary.org, ', 'Викисловаря ('),
            ('Wiktextract / kaikki.org', 'Wiktextract'), ('en.wiktionary.org', 'English Wiktionary'), ('ru.wiktionary.org', 'Викисловарь'),
            ('fi.wikipedia.org', 'финская Википедия'), ('kaikki.org', 'Wiktextract'), ("'https://pirogovlab.ru/sanamaailma/'", 'null')]
    for rel in ('js/i18n.js', 'js/app.js', 'js/tracks.js', 'js/platform.js'):
        def sub(s):
            for a, b in SUBS: s = s.replace(a, b)
            return s
        edit(rel, sub)

# ---- guards
bad = []
for dp, _, fs in os.walk(out):
    for f in fs:
        if not f.endswith(('.html', '.js', '.css', '.json')): continue
        p = os.path.join(dp, f); s = open(p, encoding='utf-8', errors='ignore').read()
        if f.endswith('.html') and ('testBadge' in s or 'noindex' in s): bad.append(p + ': test badge/noindex')
        if target == 'yandex' and '/data/' not in p:
            for m in re.finditer(r'https?://[^\s"\'`<>)]+|\b[\w.-]*(?:pirogovlab|wiktionary|wikipedia|kaikki|github|youtube|vk|play\.google|rustore)[\w-]*\.(?:ru|com|org|net|me|io)\b', s, re.I):
                u = m.group(0)
                if 'w3.org' in u or u.startswith('https://yandex.ru/dev/games'): continue
                bad.append(f'{p}: external ref {u}')
s = open(os.path.join(out, 'js/app.js'), encoding='utf-8').read()
if 'if (!window.RELEASE) window.sanamaailma' not in s: bad.append('app.js: test hooks not guarded')
if bad:
    print('\n'.join(bad)); sys.exit('build_release: ABORT')
size = sum(os.path.getsize(os.path.join(dp, f)) for dp, _, fs in os.walk(out) for f in fs)
print(f'build_release {target}: {out} v={V} {size/1e6:.1f} MB')
if target == 'yandex':
    assert size < 100e6, 'Yandex limit 100 MB unpacked'
    z = 'release/sanamaailma-yandex.zip'
    if os.path.exists(z): os.remove(z)
    with zipfile.ZipFile(z, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for dp, _, fs in os.walk(out):
            for f in sorted(fs):
                p = os.path.join(dp, f); arc = os.path.relpath(p, out)
                assert re.fullmatch(r'[A-Za-z0-9._/-]+', arc), 'bad filename for Yandex: ' + arc
                zf.write(p, arc, compress_type=zipfile.ZIP_STORED if f.endswith(('.mp3', '.webp', '.png', '.jpg', '.woff2')) else zipfile.ZIP_DEFLATED)
    print(f'zip: {z} {os.path.getsize(z)/1e6:.1f} MB')
