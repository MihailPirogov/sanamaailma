#!/usr/bin/env python3
"""Word-form frequencies from (the first part of) the fi.wikipedia dump, read from stdin (bzcat output)
-> src/fiwiki_freq.json (forms with count>=3). Only counts are used, no text is shipped.
Usage: curl -s https://dumps.wikimedia.org/fiwiki/latest/fiwiki-latest-pages-articles1.xml-p1p1500000.bz2 | head -c 300M | python3 tools/fiwiki_freq.py"""
import sys, re, collections, json, os, bz2
S = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src')
TOK = re.compile(r'[a-zåäö]+')
c = collections.Counter(); intext = False; n = 0
def lines():
    d = bz2.BZ2Decompressor(); buf = b''
    while True:
        chunk = sys.stdin.buffer.read(1 << 20)
        if not chunk: break
        try: out = d.decompress(chunk)
        except EOFError: break
        if d.eof:   # multistream: restart on the next stream
            rest = d.unused_data; d = bz2.BZ2Decompressor(); out += d.decompress(rest) if rest else b''
        buf += out; *ls, buf = buf.split(b'\n')
        yield from ls
for line in lines():
    line = line.decode('utf-8', 'ignore')
    if '<text' in line: intext = True
    if intext: c.update(TOK.findall(line.lower()))
    if '</text>' in line: intext = False
    n += 1
json.dump({w: k for w, k in c.items() if k >= 3}, open(f'{S}/fiwiki_freq.json', 'w'), ensure_ascii=False)
print('lines', n, 'forms', len(c), 'kept', sum(1 for k in c.values() if k >= 3))
