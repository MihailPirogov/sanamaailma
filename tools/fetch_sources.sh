#!/bin/bash
# Download the open sources into src/ (licences: SOURCES.md)
set -e
cd "$(dirname "$0")/../src"
B="https://kaikki.org/ruwiktionary/%D0%A4%D0%B8%D0%BD%D1%81%D0%BA%D0%B8%D0%B9"
curl -fsS -o ru_fi.jsonl "$B/kaikki.org-dictionary-%D0%A4%D0%B8%D0%BD%D1%81%D0%BA%D0%B8%D0%B9.jsonl"
# word frequencies: the first ~300 MB (compressed) of the fi.wikipedia articles dump is enough (~1M word forms); only counts are kept
curl -s https://dumps.wikimedia.org/fiwiki/latest/fiwiki-latest-pages-articles1.xml-p1p1500000.bz2 | head -c 300M | python3 ../tools/fiwiki_freq.py
# lemma frequencies: FrequencyWords (OpenSubtitles 2018, CC BY-SA 4.0) + wordfreq (CC BY-SA 4.0), lemmatised with simplemma (MIT, build only)
curl -fsS -o fw_fi_full.txt https://raw.githubusercontent.com/hermitdave/FrequencyWords/master/content/2018/fi/fi_full.txt
cd ..
[ -x .venv/bin/python ] || { python3 -m venv .venv && .venv/bin/pip install -q wordfreq==3.1.1 simplemma==2.0.0; }
.venv/bin/python tools/lemma_freq.py
