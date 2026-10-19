// Contact sheet of all procedural chapter backgrounds (js/art.js). Usage: cd test && node shots_art.js [out.png]
const { chromium } = require('playwright-core'); const path = require('path');
(async () => {
  const b = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  const p = await b.newPage({ viewport: { width: 1400, height: 1000 } });
  await p.goto('file://' + path.resolve(__dirname, '../js/art.js').replace(/art\.js$/, '') + '../index.html');
  await p.evaluate(() => { document.body.innerHTML = '<div id="cs" style="display:grid;grid-template-columns:repeat(7,1fr);gap:6px;background:#000;padding:6px"></div>';
    document.body.style.overflow = 'visible'; document.documentElement.style.overflow = 'visible';
    for (const t of Art.themes) { const d = document.createElement('div'); d.style.cssText = 'height:340px;background-size:cover;background-position:center;position:relative;background-image:' + Art.bg(t, 3, false);
      d.innerHTML = '<span style="position:absolute;left:4px;top:4px;background:#000a;color:#fff;font:12px sans-serif;padding:2px 4px">' + t + '</span>'; document.getElementById('cs').appendChild(d); } });
  await p.waitForTimeout(500); await p.screenshot({ path: process.argv[2] || path.resolve(__dirname, '../screens/art_sheet.png'), fullPage: true }); await b.close();
})();
