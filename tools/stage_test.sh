#!/bin/bash
# Stage the TEST web build into dist_test/ (game files only) with <meta name="robots" content="noindex, nofollow"> in every page.
# Deploy (only with the owner's OK): rsync -a --delete dist_test/ root@95.142.37.63:/var/www/www-root/data/www/pirogovlab.ru/sanamaailma/ && chown -R www-root:www-root …
set -e
cd "$(dirname "$0")/.."
rm -rf dist_test && mkdir dist_test
cp -r index.html css js data fonts img privacy dist_test/
# signed release APK for the download link on /sanamaailma-igra/ (kept in the folder; rsync --delete would otherwise remove it)
[ -f release/sanamaailma.apk ] && cp release/sanamaailma.apk dist_test/sanamaailma.apk
for f in dist_test/index.html dist_test/privacy/index.html; do
  grep -q 'name="robots"' "$f" || sed -i 's#<meta charset="utf-8">#<meta charset="utf-8">\n<meta name="robots" content="noindex, nofollow">#' "$f"
  grep -q 'noindex' "$f"
done
grep -q 'id="testBadge"' dist_test/index.html || sed -i 's|^<body>|<body>\n<div id="testBadge" style="position:fixed;left:8px;bottom:6px;z-index:9;font:600 10px Manrope,sans-serif;color:#fff;opacity:.6;pointer-events:none;text-shadow:0 1px 2px #0008">тестовая версия</div>|' dist_test/index.html
grep -q 'id="testBadge"' dist_test/index.html
du -sh dist_test
