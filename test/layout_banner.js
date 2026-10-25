// Layout check for small screens with the Android native banner (WebView shrinks by the banner height).
// Usage: node layout_banner.js [dir=android|web|yandex] [shotPrefix]
const { chromium } = require('playwright-core');
const http = require('http'), fs = require('fs'), path = require('path');
const ROOT = path.resolve(__dirname, '..');
const DIR = process.argv[2] && process.argv[2] !== 'android' ? path.resolve(ROOT, process.argv[2]) : path.join(ROOT, 'android/app/src/main/assets/www');
const PFX = process.argv[3] || '';
const MIME = { '.html': 'text/html; charset=utf-8', '.js': 'application/javascript', '.css': 'text/css', '.webp': 'image/webp', '.json': 'application/json', '.png': 'image/png', '.woff2': 'font/woff2', '.mp3': 'audio/mpeg' };
const srv = http.createServer((q, r) => { let u = decodeURIComponent(q.url.split('?')[0]); if (u === '/') u = '/index.html'; if (u === '/blank') { r.writeHead(200); return r.end('ok'); }
  fs.readFile(path.join(DIR, u), (e, b) => { if (e) { r.writeHead(404); return r.end(); } r.writeHead(200, { 'Content-Type': MIME[path.extname(u)] || 'application/octet-stream' }); r.end(b); }); }).listen(8793);
const sleep = ms => new Promise(r => setTimeout(r, ms));
const BANNER = 56; let fails = 0;
(async () => {
  const browser = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  for (const [w, h] of [[320, 568], [360, 640], [360, 740]]) {
    const ctx = await browser.newContext({ viewport: { width: w, height: h - BANNER }, deviceScaleFactor: 2 });
    await ctx.addInitScript(() => { window.AndroidBridge = { vibrate() {}, share() {}, shareImage() {}, openUrl() {}, rewardedAvailable: () => true, showRewarded() {}, interstitialAvailable: () => false, showInterstitial() {}, bannerAvailable: () => true, showBanner() {}, hideBanner() {} }; });
    const page = await ctx.newPage(); await page.goto('http://127.0.0.1:8793/index.html'); await sleep(1200);
    const n = await page.evaluate(() => TT_DATA.levels.length);
    const big = await page.evaluate(() => { let bi = 0, bs = 0; TT_DATA.levels.forEach((l, i) => { const s = l.r * 100 + l.l.length; if (s > bs) { bs = s; bi = i; } }); return bi; });
    for (const lvl of [0, big]) {
      await page.goto('http://127.0.0.1:8793/blank'); await page.evaluate(lvl => { const s = JSON.parse(localStorage.getItem('sanamaailma.v1') || '{}'); s.level = lvl; s.cur = null; s.tut = { done: true, step: 99 }; localStorage.setItem('sanamaailma.v1', JSON.stringify(s)); }, lvl);
      await page.goto('http://127.0.0.1:8793/index.html'); await sleep(1200);
      const t = await page.$('#tutSkip'); if (t && await t.isVisible()) { await t.click(); await sleep(200); }
      await page.click('#hPlay'); await sleep(1200);
      await page.evaluate(() => { const s = document.getElementById('word'); s.textContent = 'KESKIVIIKKO'; });
      const m = await page.evaluate(() => { const R = id => document.getElementById(id).getBoundingClientRect(); const g = R('grid'), p = R('word'), wh = R('wheel'), b = R('bottom');
        const zw = getComputedStyle(document.getElementById('preview')).zIndex; const top = document.elementFromPoint(p.left + p.width / 2, p.top + p.height / 2);
        return { lv: TT_DATA.levels[0] && 0, gridB: g.bottom | 0, pillT: p.top | 0, pillB: p.bottom | 0, wheelT: wh.top | 0, wheelB: wh.bottom | 0, botB: b.bottom | 0, H: innerHeight, cell: document.querySelector('.cell').getBoundingClientRect().width | 0, wheel: wh.width | 0, pillOnTop: !!top && !!top.closest('#preview') }; });
      const bad = m.gridB > m.pillT + 1 || m.pillB > m.wheelT - 4 || m.botB > m.H + 1 || !m.pillOnTop || m.cell < 14;
      if (bad) fails++;
      console.log((bad ? 'FAIL ' : 'PASS ') + `${w}x${h}-${BANNER} lvl${lvl + 1}`, JSON.stringify(m));
      if (PFX) await page.screenshot({ path: `${PFX}_${w}x${h}_lvl${lvl + 1}.png` });
    }
    await ctx.close();
  }
  await browser.close(); srv.close(); console.log(fails ? fails + ' FAILED' : 'ALL PASS'); process.exit(fails ? 1 : 0);
})();
