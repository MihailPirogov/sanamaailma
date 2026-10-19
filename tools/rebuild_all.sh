#!/bin/bash
# Rebuild game data (levels, chapters, daily puzzles, word of the day, card chunks) + religion/profanity scan + headless tests.
# Sources must be in src/ (see SOURCES.md; tools/fetch_sources.sh). Override: LEVELS=800 CHAPTER=16 tools/rebuild_all.sh
# NO deploy step: this project is not published anywhere yet.
set -e
cd "$(dirname "$0")/.."
for f in fiwiki_freq lemma_freq form_lemma ru_zipf; do [ -f src/$f.json ] || { echo "run tools/fetch_sources.sh first (missing src/$f.json)"; exit 1; }; done
[ -f css/fonts.css ] || python3 tools/embed_fonts.py
PYTHONHASHSEED=0 python3 tools/build_game.py "${LEVELS:-1000}" "${CHAPTER:-20}"
python3 tools/scan_religion.py
python3 tools/validate_levels.py
(cd test && SHOTS=../screens node test.js && SHOTS=../screens/tutorial node test_tutorial.js && node dup_swipe.js)
# release bundles (Yandex Games zip + Android www) and their tests — local only, nothing is uploaded
python3 tools/build_release.py yandex && python3 tools/build_release.py android
(cd test && node test_release.js && node test_android_www.js)
