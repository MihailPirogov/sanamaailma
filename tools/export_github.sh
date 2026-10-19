#!/bin/bash
# Export the public GitHub tree of Sanamaailma (github.com/MihailPirogov/sanamaailma) into $DEST (default /workspace/sanamaailma-gh).
# Same layout as the other PirogovLab games: code + data + android + tools + test, docs/ (checklists), store/ (texts, icon, graphics, screenshots), design/ (promo art).
# NEVER exported: release/keys, keystore.properties, *.p12/*.jks, local.properties, build outputs, APK/AAB/zip, src/ dumps, screens/, site_stage/.
set -euo pipefail
cd "$(dirname "$0")/.."
DEST="${DEST:-/workspace/sanamaailma-gh}"
mkdir -p "$DEST"; (cd "$DEST" && find . -mindepth 1 -maxdepth 1 ! -name .git -exec rm -rf {} +)
git ls-files | grep -vE '^(release/|screens/|site_stage/|src/|tools/github/|README\.md$|\.gitignore$)' | grep -vE '(\.p12|\.jks|\.keystore|keystore\.properties|local\.properties)$' > /tmp/gh_files.txt
tar -cf - -T /tmp/gh_files.txt | tar -xf - -C "$DEST"
cp tools/github/README.md tools/github/LICENSE "$DEST/"; cp tools/github/gitignore "$DEST/.gitignore"
mkdir -p "$DEST/docs" "$DEST/store/screenshots" "$DEST/design"
cp README.md "$DEST/docs/DEVELOPMENT.md"; cp release/ANDROID_CHECKLIST.md release/YANDEX_CHECKLIST.md release/STORE_STEPS.md "$DEST/docs/"
cp release/store/TEXTS_ru.md release/store/PLAY_FORMS.md release/store/icon_512.png release/store/feature_graphic_1024x500.png "$DEST/store/"
cp release/store/screenshots/*.png "$DEST/store/screenshots/"
sed 's#\.\./\.\./#../#g' release/art_src/art.html > "$DEST/design/art.html"
sed "s#'../../test/node_modules/playwright-core'#'../test/node_modules/playwright-core'#" release/art_src/render.js > "$DEST/design/render.js"
cp release/privacy_with_ads/index.html "$DEST/docs/privacy_with_ads.html"
# safety: no secrets
if grep -rIlE 'storePassword=.|keyPassword=.|BEGIN [A-Z ]*PRIVATE KEY' "$DEST" --exclude-dir=.git --exclude=export_github.sh; then echo "SECRET FOUND — abort"; exit 1; fi
find "$DEST" -name '*.p12' -o -name '*.jks' -o -name 'keystore.properties' -o -name 'local.properties' | grep . && { echo "key file found — abort"; exit 1; } || true
du -sh --exclude=.git "$DEST"; echo "exported $(wc -l < /tmp/gh_files.txt) tracked files -> $DEST"
