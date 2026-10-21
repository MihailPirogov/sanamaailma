// Web ads layer (public site build, js/adapters/web.js + js/webads_config.js) with a MOCKED Yandex.RTB loader (Ya.Context.AdvManager).
// Usage: bash tools/stage_public.sh && node test_webads.js
const { chromium } = require('playwright-core');
const http = require('http'), fs = require('fs'), path = require('path');
const ROOT = path.resolve(__dirname, '..'), DIR = path.join(ROOT, 'dist_web');
const MIME = { '.html': 'text/html; charset=utf-8', '.js': 'application/javascript; charset=utf-8', '.css': 'text/css', '.mp3': 'audio/mpeg', '.webp': 'image/webp', '.json': 'application/json', '.png': 'image/png', '.woff2': 'font/woff2', '.svg': 'image/svg+xml' };
const srv = http.createServer((q, r) => { let u = decodeURIComponent(q.url.split('?')[0]); if (u === '/') u = '/index.html';
  fs.readFile(path.join(DIR, u), (e, b) => { if (e) { r.writeHead(404); return r.end(); } r.writeHead(200, { 'Content-Type': MIME[path.extname(u)] || 'application/octet-stream' }); r.end(b); }); }).listen(8799);
const sleep = ms => new Promise(r => setTimeout(r, ms));
let fails = 0; const ok = (c, m) => { console.log((c ? 'PASS ' : 'FAIL ') + m); if (!c) fails++; };
const MOCK = `(function(){ const M = window.__rtb = { log: [] };
  window.Ya = { Context: { AdvManager: { render(o) { M.log.push(o.type ? o.type + ':' + o.blockId.slice(-1) : 'banner'); M.last = o;
    setTimeout(() => { if ((window.__mockMode || 'fill') === 'nofill') { o.onError && o.onError({ type: 'error', code: 'NO_ADS' }); return; }
      if (!o.type) { const el = document.getElementById(o.renderTo); if (el) el.innerHTML = '<div class="mockBanner">AD</div>'; o.onRender && o.onRender(); return; }
      o.onRender && o.onRender(); setTimeout(() => o.onClose && o.onClose(), 150); }, 60); } } } };
  const q = window.yaContextCb || []; window.yaContextCb = { push: f => f() }; q.forEach(f => f()); })();`;
const REAL = { banner: 'R-A-1234567-1', interstitial: 'R-A-1234567-2', rewarded: 'R-A-1234567-3' };
async function open(browser, { ids = REAL, loader = 'mock', mode = 'fill', tutDone = false } = {}) {
  const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 1 });
  const ext = [];
  await ctx.route(/^https?:\/\/(?!127\.0\.0\.1)/, r => { const u = r.request().url(); ext.push(u);
    if (/yandex\.ru\/ads\/system\/context\.js/.test(u) && loader === 'mock') return r.fulfill({ contentType: 'application/javascript', body: MOCK });
    return r.abort(); });
  if (ids) await ctx.route('**/js/webads_config.js*', r => r.fulfill({ contentType: 'application/javascript',
    body: `window.WEBADS_CONFIG=${JSON.stringify(Object.assign({ loader: 'https://yandex.ru/ads/system/context.js' }, ids))};` }));
  await ctx.addInitScript(([mode, tutDone]) => { window.__mockMode = mode; const n = Date.now; Date.now = () => n() + (window.__skew || 0);
    if (tutDone && !sessionStorage.__seeded) { sessionStorage.__seeded = 1; window.__seedTut = 1; } }, [mode, tutDone]);
  const page = await ctx.newPage(); const errors = [];
  page.on('pageerror', e => errors.push(e.message)); page.on('console', m => { if (m.type() === 'error' && !/ERR_FAILED|ERR_BLOCKED|Failed to load resource/.test(m.text())) errors.push(m.text()); });
  await page.goto('http://127.0.0.1:8799/index.html'); await sleep(1500);
  if (tutDone) { await page.evaluate(() => { const s = sanamaailma.state; s.tut = { done: true, step: 0 }; s.level = 3; sanamaailma.state = s; }); await page.reload(); await sleep(1500); }
  return { ctx, page, errors, ext };
}
const st = p => p.evaluate(() => ({ name: Platform.name, banner: !!document.querySelector('#webAdBanner .mockBanner'), withBanner: document.documentElement.classList.contains('withBanner'),
  rtb: (window.__rtb || { log: [] }).log.slice(), web: (window.__webads || []).slice(), rew: Platform.ads.rewardedAvailable(), inter: Platform.ads.interstitialAvailable() }));
async function winLevel(page) {
  await page.evaluate(() => { const g = sanamaailma.game; g.lv.w.forEach(x => { if (!g.found.has(x[0])) sanamaailma.submit(x[0], []); }); });
  await page.waitForSelector('#wNext', { timeout: 5000 }); await sleep(500);
}
async function next(page) { await page.click('#wNext'); await sleep(700);
  for (let i = 0; i < 3 && !(await page.isHidden('#modal')); i++) { const b = await page.$('#modal button.big'); if (b) await b.click(); await sleep(700); }
  for (let i = 0; i < 40 && !(await page.evaluate(() => document.getElementById('scrGame').classList.contains('on') && sanamaailma.game && sanamaailma.game.found.size === 0)); i++) await sleep(100); }
(async () => {
  const browser = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox', '--autoplay-policy=no-user-gesture-required'] });
  // 1) fresh player: ads loaded, but nothing before the tutorial is finished
  { const { ctx, page, errors, ext } = await open(browser);
    let s = await st(page);
    ok(s.name === 'web' && ext.some(u => /context\.js/.test(u)), 'web adapter active, RTB loader requested');
    ok(!s.banner && !s.rtb.length, 'tutorial not done -> no banner, no ad requests ' + JSON.stringify(s.rtb));
    await page.click('#tutSkip'); await sleep(500); s = await st(page);
    ok(s.banner && s.withBanner && s.rtb[0] === 'banner', 'after tutorial: sticky banner rendered via renderTo (#webAdBanner), game area shrunk');
    ok(errors.length === 0, 'no JS errors ' + errors.join(' | ')); await ctx.close(); }
  // 2) returning player: rewarded hint, ×2 coins, interstitial caps, extra spin cap
  { const { ctx, page, errors } = await open(browser, { tutDone: true });
    await page.click('#hPlay'); await sleep(1200);
    ok(await page.isVisible('#bAd'), '🎬 hint button visible when rewarded is available');
    const before = await page.evaluate(() => document.querySelectorAll('#grid .cell.open, #grid .on, .cell.hint').length);
    await page.click('#bAd'); await page.click('#adGo'); await sleep(800);
    let s = await st(page);
    ok(s.rtb.includes('fullscreen:3') && s.rtb.filter(x => x === 'fullscreen:3').length === 1 && s.web.includes('rewarded close'), 'rewarded hint: separate fullscreen block shown and closed -> reward ' + s.web.join(','));
    ok(await page.evaluate(() => !/реклам/i.test(document.getElementById('toast').textContent) || !document.getElementById('toast').classList.contains('show')), 'reward granted (no ad-fail toast)');
    const last = await page.evaluate(() => ({ p: __rtb.last.platform, b: __rtb.last.blockId, t: __rtb.last.type })); ok(last.b === 'R-A-1234567-3' && last.t === 'fullscreen' && /touch|desktop/.test(last.p), 'reward ad = type fullscreen, own block ' + last.b + ', platform ' + last.p);
    // win #1 with ×2 coins
    await winLevel(page);
    const c0 = await page.evaluate(() => sanamaailma.state.coins); const dbl = await page.$('#wDouble');
    ok(!!dbl, '×2 coins button offered after a win');
    if (dbl) { await dbl.click(); await sleep(900); }
    const c1 = await page.evaluate(() => sanamaailma.state.coins);
    ok(c1 > c0 && (await st(page)).rtb.filter(x => x === 'fullscreen:3').length === 2, '×2 coins: rewarded watched, coins ' + c0 + ' -> ' + c1);
    await next(page); await winLevel(page); await next(page); await winLevel(page); await next(page);
    s = await st(page); ok(!s.rtb.includes('fullscreen:2'), '3 wins within 150 s of session start -> no fullscreen');
    await page.evaluate(() => { window.__skew = 200000; }); await winLevel(page); await next(page);
    s = await st(page); ok(s.rtb.filter(x => x === 'fullscreen:2').length === 1 && s.web.includes('interstitial close'), 'win after >=150 s and >=3 wins -> one fullscreen (type fullscreen) ' + s.web.join(','));
    ok(await page.evaluate(() => __rtb.last.blockId) === 'R-A-1234567-2', 'fullscreen uses interstitial block');
    await winLevel(page); await next(page); await winLevel(page); await next(page);
    s = await st(page); ok(s.rtb.filter(x => x === 'fullscreen:2').length === 1, 'next 2 wins -> no second fullscreen (cap: every 3rd win, 150 s)');
    await page.evaluate(() => { window.__skew = 400000; }); await winLevel(page); await next(page);
    s = await st(page); ok(s.rtb.filter(x => x === 'fullscreen:2').length === 2, '3rd win after the last ad + 150 s -> second fullscreen');
    // extra spin for rewarded (up to 3/day)
    await page.evaluate(() => { const s = sanamaailma.state; s.spin = { last: sanamaailma.dayKey(), adDay: null, adN: 0 }; sanamaailma.state = s; sanamaailma.goHome(); sanamaailma.openSpin(); }); await sleep(600);
    ok(await page.isVisible('#spAd'), 'extra-spin 🎬 button shown after the free spin is used');
    await page.click('#spAd'); await sleep(8000);
    ok(await page.evaluate(() => sanamaailma.state.spin.adN) === 1, 'extra spin granted after rewarded (adN=1)');
    await page.evaluate(() => { sanamaailma.closeModal(); const s = sanamaailma.state; s.spin.adN = 3; sanamaailma.state = s; sanamaailma.openSpin(); }); await sleep(600);
    ok(!(await page.isVisible('#spAd')), 'after 3 extra spins today -> button hidden');
    ok(errors.length === 0, 'no JS errors ' + errors.join(' | ')); await ctx.close(); }
  // 3) no fill: error callbacks -> no crash, 🎬 hidden, banner removed
  { const { ctx, page, errors } = await open(browser, { tutDone: true, mode: 'nofill' });
    let s = await st(page); ok(!s.banner && !s.withBanner && s.web.includes('banner error'), 'banner no-fill -> container removed, no empty bar');
    await page.click('#hPlay'); await sleep(1000);
    if (await page.isVisible('#bAd')) { await page.click('#bAd'); await page.click('#adGo'); await sleep(900); }
    s = await st(page); ok(!s.rew && await page.isHidden('#bAd'), 'rewarded no-fill -> rewarded unavailable, 🎬 hidden');
    ok(!(await page.evaluate(() => document.body.classList.contains('adShowing'))) && await page.isHidden('#modal'), 'game continues');
    ok(errors.length === 0, 'no JS errors ' + errors.join(' | ')); await ctx.close(); }
  // 4) ad blocker: loader request fails
  { const { ctx, page, errors } = await open(browser, { tutDone: true, loader: 'block' });
    await page.click('#hPlay'); await sleep(1000); const s = await st(page);
    ok(!s.banner && !s.withBanner && !s.rew && !s.inter && await page.isHidden('#bAd') && s.web.includes('loader blocked'), 'blocked loader -> no banner, 🎬 hidden, no fullscreen');
    await winLevel(page); await next(page); ok(errors.length === 0, 'no JS errors, levels still play ' + errors.join(' | ')); await ctx.close(); }
  // 5) placeholder IDs (current config) -> ads off, no request to yandex.ru
  { const { ctx, page, errors, ext } = await open(browser, { ids: null, tutDone: true });
    await page.click('#hPlay'); await sleep(800); const s = await st(page);
    ok(!ext.some(u => /yandex\.ru\/ads/.test(u)) && !s.banner && await page.isHidden('#bAd'), 'placeholder IDs -> no loader request, no ads');
    ok(errors.length === 0, 'no JS errors ' + errors.join(' | ')); await ctx.close(); }
  // 5b) explicit empty-string IDs -> off as well
  { const { ctx, page, errors, ext } = await open(browser, { ids: { banner: '', interstitial: '', rewarded: '' }, tutDone: true });
    await page.click('#hPlay'); await sleep(800); const s = await st(page);
    ok(!ext.some(u => /yandex\.ru\/ads/.test(u)) && !s.banner && !s.rew && !s.inter && await page.isHidden('#bAd'), "empty-string IDs ('') -> no loader request, no ads");
    await winLevel(page); await next(page); ok(errors.length === 0, 'no JS errors, levels play ' + errors.join(' | ')); await ctx.close(); }
  { const c = fs.readFileSync(path.join(ROOT, 'js/webads_config.js'), 'utf8'); ok(/banner: ''/.test(c) && /interstitial: ''/.test(c) && /rewarded: ''/.test(c), 'shipped config has empty IDs (RSYa site not approved yet)'); }
  // 6) other builds untouched
  for (const d of ['release/build/yandex', 'android/app/src/main/assets/www']) { const p = path.join(ROOT, d); if (!fs.existsSync(p)) { console.log('skip ' + d); continue; }
    const h = fs.readFileSync(path.join(p, 'index.html'), 'utf8');
    ok(!/webads|adapters\/web\.js|context\.js/.test(h) && !fs.existsSync(path.join(p, 'js/adapters/web.js')) && !fs.existsSync(path.join(p, 'js/webads_config.js')), d + ': no web ads layer'); }
  await browser.close(); srv.close();
  console.log(fails ? fails + ' FAILED' : 'ALL PASSED'); process.exit(fails ? 1 : 0);
})().catch(e => { console.error(e); process.exit(1); });
