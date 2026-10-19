// Regression (ported from chuvash-wow/test/dup_swipe.js): swiping a word through the *other* copy of a duplicated wheel letter must work
// (touch, normal play + tutorial). Bug: hit zones used the CSS-scaled (.sel 1.1×) rects, the first matching letter won instead of the nearest,
// and passing near the previous letter counted as backtracking. Usage: node dup_swipe.js  (URL=… for a deployed copy)
const { chromium } = require('playwright-core'); const path = require('path');
const sleep = ms => new Promise(r => setTimeout(r, ms));
const ROOT = process.env.URL || ('file://' + (process.env.ROOT || path.resolve(__dirname, '..')) + '/index.html');
const perms = (word, L) => { const out = []; const rec = (k, used, acc) => { if (k === word.length) return out.push(acc.slice()); for (let j = 0; j < L.length; j++) if (!used.has(j) && L[j] === word[k]) { used.add(j); acc.push(j); rec(k + 1, used, acc); acc.pop(); used.delete(j); } }; rec(0, new Set(), []); return out; };
const firstCopy = (w, L) => { const used = new Set(); return Array.from(w).map(c => { const j = L.findIndex((x, k) => x === c && !used.has(k)); used.add(j); return j; }); };
let fails = 0; const check = (c, m) => { console.log((c ? 'ok   ' : 'FAIL ') + m); if (!c) fails++; };
(async () => {
  const b = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, hasTouch: true, isMobile: true, deviceScaleFactor: 2 }); const page = await ctx.newPage();
  const cdp = await ctx.newCDPSession(page); const errs = []; page.on('pageerror', e => errs.push(e.message));
  const touch = (type, x, y) => cdp.send('Input.dispatchTouchEvent', { type, touchPoints: type === 'touchEnd' ? [] : [{ x, y }] });
  const xyOf = () => page.evaluate(() => sanamaailma.game.letterEls.map(e => { const r = e.getBoundingClientRect(); return [r.left + r.width / 2, r.top + r.height / 2]; }));
  // A finger slides straight over letters it has ALREADY used (that is the case the old hit-test broke: the used copy, scaled up by .sel,
  // grabbed the swipe or counted as backtracking); only when an UNUSED letter lies on the straight line does it curve through the
  // empty middle of the wheel (a straight chord over an unused letter selects it in every wheel game).
  const seg = async (x0, y0, x1, y1) => { for (let t = 1; t <= 8; t++) await touch('touchMove', x0 + (x1 - x0) * t / 8, y0 + (y1 - y0) * t / 8); };
  const dSeg = ([px, py], [x0, y0], [x1, y1]) => { const vx = x1 - x0, vy = y1 - y0, t = Math.max(0, Math.min(1, ((px - x0) * vx + (py - y0) * vy) / (vx * vx + vy * vy))); return Math.hypot(px - x0 - t * vx, py - y0 - t * vy); };
  let straightOverUsed = 0;
  async function swipe(ord) { const xy = await xyOf(), g = await page.evaluate(() => { const r = document.getElementById('wheel').getBoundingClientRect(); return [r.left + r.width / 2, r.top + r.height / 2, r.width]; });
    const c = [g[0], g[1]], hr = g[2] * .23 * .62; await touch('touchStart', ...xy[ord[0]]);
    for (let k = 1; k < ord.length; k++) { const a = ord[k - 1], b = ord[k], used = new Set(ord.slice(0, k));
      const blockers = xy.map((p, j) => j).filter(j => j !== a && j !== b && dSeg(xy[j], xy[a], xy[b]) < hr * 1.05);
      if (blockers.some(j => !used.has(j))) { await seg(...xy[a], ...c); await seg(...c, ...xy[b]); }
      else { if (blockers.length) straightOverUsed++; await seg(...xy[a], ...xy[b]); }
      await sleep(15); }
    const typed = await page.evaluate(() => document.getElementById('word').textContent); await touch('touchEnd'); await sleep(250); return typed; }
  const open = async (id, tut) => { await page.evaluate(([i, tut]) => { const s = sanamaailma.state; s.cur = null; if (tut != null) s.tut = { done: false, step: tut }; sanamaailma.state = s; sanamaailma.startGame('main', i); }, [id, tut]); await sleep(900); };
  const casesOf = async () => { const info = await page.evaluate(() => ({ L: sanamaailma.game.letters.slice(), w: sanamaailma.game.lv.w.map(x => x[0]) })); const cases = [];
    for (const w of info.w.filter(w => new Set(w).size < w.length)) { const f = firstCopy(w, info.L).join(); for (const o of perms(w, info.L)) if (o.join() !== f) { cases.push([w, o]); break; } }
    return [info, cases]; };
  await page.goto(ROOT); await page.evaluate(() => localStorage.clear()); await page.reload(); await sleep(800);
  await page.evaluate(() => sanamaailma.tutSkip());
  // levels with repeated letters: an early one (5 letters) and late ones (7-8 letters, dense wheel)
  const lvls = await page.evaluate(() => { const L = sanamaailma.data.levels, pick = []; const dup = l => l.w.some(x => new Set(x[0]).size < x[0].length && [...x[0]].some(ch => l.l.split(ch).length > 2));
    for (const from of [3, 600, 900]) { const i = L.findIndex((l, k) => k >= from && dup(l)); if (i >= 0) pick.push(i); } return pick; });
  let firstCases = null, firstLv = null;
  for (const id of lvls) {
    await open(id); const [info, cases] = await casesOf();
    check(cases.length > 0, `level ${id + 1} [${info.L.join('')}] has duplicate-letter words: ${cases.map(c => c[0]).join(', ')}`);
    if (!firstCases && cases.length) { firstCases = cases; firstLv = id; }
    for (const [w, o] of cases) { await page.evaluate(() => sanamaailma.game.found.clear());
      const typed = await swipe(o); const ok = await page.evaluate(w => sanamaailma.game.found.has(w), w);
      check(ok, `normal play L${id + 1}: ${w} via other copy ${JSON.stringify(o)} (typed "${typed}")`); await page.evaluate(() => sanamaailma.closeModal()); }
  }
  // Precise hit-test regressions on an 8-letter wheel (fail on the old code):
  //  T1 a used letter (drawn 1.1× bigger by .sel) must not steal a point that is nearer to its neighbour → nearest letter wins;
  //  T2 brushing the edge of the previous letter on the way elsewhere must not undo the last letter (backtrack only near its centre).
  { const id = lvls[lvls.length - 1]; await open(id);
    const xy = await xyOf(), W = await page.evaluate(() => document.getElementById('wheel').getBoundingClientRect().width), hr = W * .23 * .62, n = xy.length;
    const L = await page.evaluate(() => sanamaailma.game.letters.join(''));
    const along = (p, q, dist) => { const dx = q[0] - p[0], dy = q[1] - p[1], l = Math.hypot(dx, dy); return [p[0] + dx / l * dist, p[1] + dy / l * dist]; };
    const typedNow = () => page.evaluate(() => document.getElementById('word').textContent);
    // T1: touch letter 0, slide to a point 0.9·hr from letter 1 (that point is inside letter 0's old scaled zone)
    await touch('touchStart', ...xy[0]); const p1 = along(xy[1], xy[0], hr * .9);
    for (let t = 1; t <= 6; t++) await touch('touchMove', xy[0][0] + (p1[0] - xy[0][0]) * t / 6, xy[0][1] + (p1[1] - xy[0][1]) * t / 6);
    await sleep(80); const t1 = await typedNow(); await touch('touchEnd'); await sleep(300); await page.evaluate(() => sanamaailma.closeModal());
    check(t1 === L[0] + L[1], `T1 nearest letter wins next to a selected letter: typed "${t1}", want "${L[0] + L[1]}"`);
    // T2: swipe letter 1 → letter 2 (selected [1, 2]), then move back to 0.82·hr from letter 1 (inside its zone, not near its centre:
    //     which used to count as backtracking and drop letter 2), then on through the middle to letter 4
    const a = 1, b = 2, c = 4; await touch('touchStart', ...xy[a]); await seg(...xy[a], ...xy[b]);
    const ctr = await page.evaluate(() => { const r = document.getElementById('wheel').getBoundingClientRect(); return [r.left + r.width / 2, r.top + r.height / 2]; });
    const edge = along(xy[a], xy[b], hr * .82);   // 0.82·hr from the previous letter: inside its zone but far from its centre
    await seg(...xy[b], ...edge); await seg(...edge, ...ctr); await seg(...ctr, ...xy[c]);
    await sleep(80); const t2 = await typedNow(); await touch('touchEnd'); await sleep(300); await page.evaluate(() => sanamaailma.closeModal());
    check(t2 === L[a] + L[b] + L[c], `T2 brushing the previous letter's edge does not undo: typed "${t2}", want "${L[a] + L[b] + L[c]}"`); }
  // T3: deliberate backtracking still works: 1 → 2 → back onto the centre of 1 removes 2
  { const xy = await xyOf(); const L = await page.evaluate(() => sanamaailma.game.letters.join(''));
    await touch('touchStart', ...xy[1]); await seg(...xy[1], ...xy[2]); await seg(...xy[2], ...xy[1]); await sleep(80);
    const t3 = await page.evaluate(() => document.getElementById('word').textContent); await touch('touchEnd'); await sleep(300); await page.evaluate(() => sanamaailma.closeModal());
    check(t3 === L[1], `T3 sliding back onto the previous letter undoes the last one: typed "${t3}", want "${L[1]}"`); }
  // Tutorial: the 'swipe' step must accept a word swiped through the non-hinted copy and advance to 'grid'
  await open(firstLv, 1); await page.evaluate(() => sanamaailma.game.found.clear()); await sleep(500);
  const before = await page.evaluate(() => sanamaailma.tutStep);
  if (before === 'swipe') { const [w, o] = firstCases[0]; const typed = await swipe(o); await sleep(1300);
    const after = await page.evaluate(() => sanamaailma.tutStep); const ok = await page.evaluate(w => sanamaailma.game.found.has(w), w);
    check(ok && after === 'grid', `tutorial: ${w} via other copy ${JSON.stringify(o)} typed "${typed}" → step ${before}→${after}`);
  } else check(false, `tutorial did not reach swipe step (at ${before})`);
  check(straightOverUsed > 0, `some swipes slid straight over an already used letter (${straightOverUsed} segments)`);
  check(errs.length === 0, 'no JS errors ' + errs.slice(0, 2).join(' | '));
  console.log(fails ? `DUP TEST FAILED (${fails})` : 'DUP TEST PASSED'); await b.close(); process.exit(fails ? 1 : 0);
})();
