// Readability check of the crossword / letter wheel over chapter photos (mobile + desktop). Usage: URL=… SHOTS=… node shots_photo.js [chapters…]
const { chromium } = require('playwright-core'); const path = require('path'); const fs = require('fs');
const URL = process.env.URL || 'http://127.0.0.1:8093/'; const SHOTS = process.env.SHOTS || '../screens/photo';
const CH = process.argv.slice(2).map(Number); const chs = CH.length ? CH : [1, 13, 29, 43, 44, 45, 47];
const sleep = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  fs.mkdirSync(SHOTS, { recursive: true });
  const b = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  for (const [tag, vp] of (process.env.VPS === 'all' ? [['m', { width: 390, height: 844 }], ['s', { width: 360, height: 640 }], ['d', { width: 1440, height: 900 }]] : [['m', { width: 390, height: 844 }], ['d', { width: 1440, height: 900 }]])) {
    const p = await (await b.newContext({ viewport: vp, deviceScaleFactor: tag === 'd' ? 1 : 2 })).newPage(); const errs = [];
    p.on('pageerror', e => errs.push(e.message));
    await p.goto(URL); await p.evaluate(() => { localStorage.clear(); }); await p.reload(); await sleep(800);
    await p.evaluate(() => { const s = sanamaailma.state; s.tut = s.tut || {}; }); await p.click('#tutSkip').catch(() => {});
    for (const c of chs) {
      await p.evaluate(i => sanamaailma.startGame('main', i), (c - 1) * 20 + 3); await sleep(1600);
      // reveal one word so found (filled) cells are visible as well
      await p.evaluate(() => { const w = sanamaailma.game.lv.w[0][0]; sanamaailma.submit(w, []); }); await sleep(900);
      const photo = await p.evaluate(() => document.body.classList.contains('photoBg') && /webp/.test(document.getElementById('bg').style.backgroundImage));
      console.log(tag, 'ch' + c, 'photo:', photo);
      await p.screenshot({ path: path.join(SHOTS, `${tag}_ch${String(c).padStart(2, '0')}.png`) });
    }
    console.log(tag, 'errors', errs.length ? errs : 'none');
  }
  await b.close();
})();
