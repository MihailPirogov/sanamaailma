/* Procedural SVG art for «Sanamaailma»: Finnish landscapes in a flat Scandinavian style — lakes with mirror reflections,
   geometric spruces, birches, red cottages with white trim, granite skerries, a plain lighthouse, fells with reindeer, aurora ribbons,
   white nights and kaamos. Palette: deep navy, ice blue, snow white, spruce green, rowan/cloudberry warm accents.
   Deliberately NO religious imagery: no churches, crosses, spires or domes. All original code. */
(function () {
  'use strict';
  function rng(seed) { let s = seed >>> 0 || 1; return () => (s = (s * 1664525 + 1013904223) >>> 0) / 4294967296; }
  const C = { navy: '#0b2545', navy2: '#13315c', ice: '#8ecae6', ice2: '#cfe8f3', snow: '#f4f8fb', spruce: '#1f5f4a', spruce2: '#123f33',
    rowan: '#e4572e', berry: '#ff8c42', cloud: '#ffb347', falu: '#a8322a', granite: '#8d99ae', birch: '#f1efe6' };
  const P = {   // sky top/bottom, sun, far, mid, near, water + features
    lake:        { sky: ['#5fa8d3', '#dbeef6'], sun: '#fff4d0', far: '#5d8c8a', mid: '#2f6b5a', near: '#1f4f42', water: '#4f8fb8', spruce: 1, lake: 1 },
    forest:      { sky: ['#6aa9c9', '#e3efe9'], sun: '#fff1c2', far: '#4f7f70', mid: '#2a5f4c', near: '#174034', ground: '#123329', spruce: 2, berries: 1 },
    shore:       { sky: ['#7bb8dc', '#f2f1e6'], sun: '#ffe9a8', far: '#7d9a96', mid: '#44766a', near: '#2c5a4c', water: '#5b9ac4', spruce: .6, rocks: 1, lake: 1, jetty: 1 },
    cabin:       { sky: ['#f2a65a', '#fde7c8'], sun: '#fff1c8', far: '#8a7f78', mid: '#3c5a52', near: '#22403a', water: '#7aa5c2', spruce: 1, lake: 1, cabin: 1 },
    archipelago: { sky: ['#4f9bd0', '#e6f3fa'], sun: '#fffbe8', far: '#8fb0b8', mid: '#5f8c84', near: '#3b6a5e', water: '#3f86bf', islands: 1, lake: 1, boat: 1 },
    birch:       { sky: ['#8cc8e4', '#f3f8ef'], sun: '#ffffff', far: '#9bc4a2', mid: '#6ea67a', near: '#4b8a5a', ground: '#3e7a4c', birch: 1, flowers: 1 },
    summer:      { sky: ['#3d9ad9', '#d7f0fb'], sun: '#ffe066', far: '#79b38c', mid: '#3f8a5f', near: '#25664a', water: '#3a8cc9', spruce: .7, lake: 1, boat: 1 },
    midnight:    { sky: ['#f6b38a', '#fbe3c5'], sun: '#ffd27a', far: '#b08a8a', mid: '#5d6075', near: '#3a3f58', water: '#d79d84', spruce: 1, lake: 1, lowsun: 1 },
    autumn:      { sky: ['#7fb3d5', '#f6ead6'], sun: '#fff0c8', far: '#c48a4a', mid: '#b5522a', near: '#7d3420', ground: '#5a2a1a', spruce: .5, birch: .6, ruska: 1 },
    winter:      { sky: ['#9fc6e4', '#f4f8fb'], sun: '#ffffff', far: '#d8e6f1', mid: '#b9d1e6', near: '#eef4fa', ground: '#ffffff', spruce: 1.2, snowy: 1, snow: 1 },
    aurora:      { sky: ['#06142b', '#173a5e'], sun: '#eef6ff', far: '#1d3d5a', mid: '#132f48', near: '#0c2236', ground: '#e8f0f8', spruce: 1, snowy: 1, aurora: 1, stars: 1 },
    spring:      { sky: ['#86cbe8', '#f2fbe9'], sun: '#fff6c0', far: '#a8d3a0', mid: '#72b37a', near: '#4b9560', water: '#6db1d6', birch: .7, flowers: 1, river: 1 },
    river:       { sky: ['#6eb0d6', '#eaf4f2'], sun: '#fff3c8', far: '#6f9a8c', mid: '#3f7563', near: '#28594a', water: '#5b9fc9', spruce: 1, river: 1, rapids: 1 },
    bog:         { sky: ['#9cc0d6', '#efeee2'], sun: '#fff6dc', far: '#9aa58a', mid: '#a49a62', near: '#7f7a46', ground: '#6a6a3a', spruce: .35, pools: 1, cotton: 1, mist: 1 },
    fell:        { sky: ['#7ab4dc', '#eef5f7'], sun: '#ffffff', far: '#b8c6cf', mid: '#8fa79a', near: '#5f7f6c', ground: '#4c6a58', fell: 1, spruce: .3, reindeer: 1 },
    sea:         { sky: ['#5d9fd1', '#e8f2f7'], sun: '#fffbe8', far: '#8aa6b4', mid: '#6f8f98', near: '#55707a', water: '#2f78b2', rocks: 1, lake: 1, lighthouse: 1, gulls: 1 },
    harbor:      { sky: ['#7db7de', '#f3efe4'], sun: '#ffe9b0', far: '#9fb4bf', mid: '#6d8995', near: '#4c6672', water: '#3d82b8', lake: 1, boat: 2, sheds: 1, gulls: 1 },
    city:        { sky: ['#8ec3e6', '#f6efe2'], sun: '#fff1c8', far: '#b9c6cf', mid: '#8a9aa6', near: '#5e6e7a', water: '#4a88b8', lake: 1, city: 1, gulls: 1 },
    village:     { sky: ['#f3b06d', '#fdeccd'], sun: '#fff3cc', far: '#9b9a7a', mid: '#6e8a5a', near: '#4c6a44', ground: '#3d5a38', birch: .5, cabin: 2, field: .5 },
    field:       { sky: ['#78c0e8', '#fbf3d6'], sun: '#ffd84a', far: '#a7c08a', mid: '#d8c062', near: '#c4a03e', ground: '#a07e2c', spruce: .5, field: 1, bales: 1 },
    dawn:        { sky: ['#f0b6b0', '#fff0dc'], sun: '#ffffff', far: '#c1aab8', mid: '#8f97a8', near: '#64788a', water: '#e2b4b0', spruce: 1, lake: 1, mist: 1 },
  };
  const f1 = n => Math.round(n * 10) / 10;
  function ridge(r, y, amp, w, h, n, sharp) {
    let d = `M0 ${h} L0 ${f1(y)}`; const step = w / n;
    for (let i = 1; i <= n; i++) { const x = i * step, yy = y + (r() - .5) * amp;
      d += sharp ? ` L${f1(x - step / 2)} ${f1(yy - amp * (0.3 + r() * .7))} L${f1(x)} ${f1(yy)}` : ` Q ${f1(x - step / 2)} ${f1(y - amp * (0.3 + r() * .8))} ${f1(x)} ${f1(yy)}`; }
    return d + ` L${w} ${h} Z`;
  }
  /* ---------- motifs (flat, geometric) ---------- */
  function spruce(x, y, s, col, snow) {   // stacked triangles
    let g = `<rect x="${f1(x - s * .05)}" y="${f1(y - s * .12)}" width="${f1(s * .1)}" height="${f1(s * .14)}" fill="#3a2a20"/>`;
    for (let k = 0; k < 4; k++) { const w = s * (.42 - k * .08), top = y - s * (.32 + k * .2), bot = y - s * (.08 + k * .2);
      g += `<path d="M${f1(x)} ${f1(top)} L${f1(x + w)} ${f1(bot)} L${f1(x - w)} ${f1(bot)} Z" fill="${col}"/>`;
      if (snow) g += `<path d="M${f1(x)} ${f1(top)} L${f1(x + w * .45)} ${f1(top + (bot - top) * .45)} L${f1(x - w * .45)} ${f1(top + (bot - top) * .45)} Z" fill="#f4f8fb"/>`; }
    return g;
  }
  function birchTree(x, y, s, leaf, r) {
    let g = `<rect x="${f1(x - s * .03)}" y="${f1(y - s)}" width="${f1(s * .06)}" height="${f1(s)}" fill="${C.birch}"/>`;
    for (let i = 0; i < 4; i++) g += `<rect x="${f1(x - s * .03)}" y="${f1(y - s * (.2 + r() * .7))}" width="${f1(s * .04)}" height="${f1(s * .015)}" fill="#2b2b2b"/>`;
    g += `<ellipse cx="${f1(x)}" cy="${f1(y - s * .85)}" rx="${f1(s * .2)}" ry="${f1(s * .3)}" fill="${leaf}" opacity=".95"/>`;
    return g;
  }
  function cabin(x, y, s, lit) {           // Finnish red cottage (falu red, white trim), plain gable roof
    const w = s, h = s * .55;
    return `<rect x="${f1(x)}" y="${f1(y - h)}" width="${f1(w)}" height="${f1(h)}" fill="${C.falu}"/>` +
      `<path d="M${f1(x - s * .08)} ${f1(y - h)} L${f1(x + w / 2)} ${f1(y - h - s * .38)} L${f1(x + w + s * .08)} ${f1(y - h)} Z" fill="#2d2f36"/>` +
      `<rect x="${f1(x + w * .14)}" y="${f1(y - h * .72)}" width="${f1(w * .2)}" height="${f1(h * .34)}" fill="${lit ? '#ffd27a' : '#cfe3ee'}" stroke="#fff" stroke-width="${f1(s * .03)}"/>` +
      `<rect x="${f1(x + w * .62)}" y="${f1(y - h * .78)}" width="${f1(w * .2)}" height="${f1(h * .78)}" fill="#5a2a22" stroke="#fff" stroke-width="${f1(s * .03)}"/>` +
      `<rect x="${f1(x)}" y="${f1(y - h)}" width="${f1(s * .04)}" height="${f1(h)}" fill="#fff"/><rect x="${f1(x + w - s * .04)}" y="${f1(y - h)}" width="${f1(s * .04)}" height="${f1(h)}" fill="#fff"/>`;
  }
  function lighthouse(x, y, s) {           // plain striped tower with a lamp room
    return `<path d="M${f1(x - s * .12)} ${f1(y)} L${f1(x - s * .07)} ${f1(y - s)} L${f1(x + s * .07)} ${f1(y - s)} L${f1(x + s * .12)} ${f1(y)} Z" fill="#fff"/>` +
      `<path d="M${f1(x - s * .105)} ${f1(y - s * .3)} L${f1(x - s * .09)} ${f1(y - s * .5)} L${f1(x + s * .09)} ${f1(y - s * .5)} L${f1(x + s * .105)} ${f1(y - s * .3)} Z" fill="${C.rowan}"/>` +
      `<path d="M${f1(x - s * .085)} ${f1(y - s * .7)} L${f1(x - s * .075)} ${f1(y - s * .85)} L${f1(x + s * .075)} ${f1(y - s * .85)} L${f1(x + s * .085)} ${f1(y - s * .7)} Z" fill="${C.rowan}"/>` +
      `<rect x="${f1(x - s * .06)}" y="${f1(y - s * 1.1)}" width="${f1(s * .12)}" height="${f1(s * .1)}" fill="#ffe28a"/><rect x="${f1(x - s * .09)}" y="${f1(y - s * 1.16)}" width="${f1(s * .18)}" height="${f1(s * .06)}" fill="${C.navy}"/>`;
  }
  function boat(x, y, s, col) {
    return `<path d="M${f1(x - s)} ${f1(y)} L${f1(x + s)} ${f1(y)} L${f1(x + s * .7)} ${f1(y + s * .3)} L${f1(x - s * .7)} ${f1(y + s * .3)} Z" fill="${col || C.falu}"/>` +
      `<rect x="${f1(x - s * .02)}" y="${f1(y - s * 1.2)}" width="${f1(s * .04)}" height="${f1(s * 1.2)}" fill="#333"/><path d="M${f1(x + s * .04)} ${f1(y - s * 1.15)} L${f1(x + s * .75)} ${f1(y - s * .1)} L${f1(x + s * .04)} ${f1(y - s * .1)} Z" fill="#fff"/>`;
  }
  function reindeer(x, y, s) {
    return `<g fill="#4a3a30"><ellipse cx="${f1(x)}" cy="${f1(y - s * .55)}" rx="${f1(s * .38)}" ry="${f1(s * .18)}"/>` +
      [-.28, -.14, .14, .28].map(d => `<rect x="${f1(x + s * d - s * .02)}" y="${f1(y - s * .5)}" width="${f1(s * .04)}" height="${f1(s * .5)}"/>`).join('') +
      `<path d="M${f1(x + s * .3)} ${f1(y - s * .6)} L${f1(x + s * .48)} ${f1(y - s * .95)} L${f1(x + s * .58)} ${f1(y - s * .9)} L${f1(x + s * .42)} ${f1(y - s * .55)} Z"/></g>` +
      `<path d="M${f1(x + s * .5)} ${f1(y - s * .95)} l${f1(-s * .12)} ${f1(-s * .3)} m${f1(s * .06)} ${f1(s * .14)} l${f1(-s * .14)} ${f1(-s * .06)} M${f1(x + s * .54)} ${f1(y - s * .95)} l${f1(s * .06)} ${f1(-s * .3)} m${f1(-s * .03)} ${f1(s * .12)} l${f1(s * .14)} ${f1(-s * .08)}" stroke="#4a3a30" stroke-width="${f1(s * .04)}" fill="none" stroke-linecap="round"/>`;
  }
  function snowflake(x, y, s, col, w) {      // six-armed geometric crystal
    let g = `<g transform="translate(${f1(x)} ${f1(y)})" stroke="${col}" stroke-width="${w || 1.4}" stroke-linecap="round" fill="none">`;
    for (let k = 0; k < 6; k++) g += `<g transform="rotate(${k * 60})"><path d="M0 0 V${-s}"/><path d="M0 ${f1(-s * .55)} l${f1(-s * .22)} ${f1(-s * .2)} M0 ${f1(-s * .55)} l${f1(s * .22)} ${f1(-s * .2)}"/></g>`;
    return g + '</g>';
  }
  function scene(theme, seed, wide) {
    const p = P[theme] || P.lake, r = rng(seed * 7919 + 13), W = wide ? 800 : 400, H = 800, id = 'n' + theme + seed + (wide ? 'w' : '');
    let s = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" preserveAspectRatio="xMidYMid slice"><defs>` +
      `<linearGradient id="${id}s" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${p.sky[0]}"/><stop offset="1" stop-color="${p.sky[1]}"/></linearGradient>` +
      `<linearGradient id="${id}w" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${p.water || '#4f8fb8'}"/><stop offset="1" stop-color="${C.navy}"/></linearGradient>` +
      `<filter id="${id}b"><feGaussianBlur stdDeviation="7"/></filter></defs><rect width="${W}" height="${H}" fill="url(#${id}s)"/>`;
    if (p.stars) for (let i = 0; i < 70; i++) s += `<circle cx="${f1(r() * W)}" cy="${f1(r() * H * .45)}" r="${f1(.5 + r() * 1.3)}" fill="#fff" opacity="${f1(.4 + r() * .6)}"/>`;
    if (p.aurora) {
      const cols = ['#5cf2a8', '#36d1c4', '#8f7cff'];
      for (let k = 0; k < 3; k++) { const y0 = 90 + k * 60 + r() * 40; let d = `M${-40} ${f1(y0)}`;
        for (let x = 0; x <= W + 80; x += 80) d += ` Q ${f1(x + 40)} ${f1(y0 + (r() - .5) * 120)} ${f1(x + 80)} ${f1(y0 + (r() - .5) * 60)}`;
        s += `<path d="${d}" stroke="${cols[k]}" stroke-width="${30 + k * 10}" fill="none" opacity="${.45 - k * .1}" filter="url(#${id}b)"/>`; }
    }
    // sun / moon (plain circle)
    const sx = W * (.2 + r() * .6), sy = p.lowsun ? H * .44 : H * (.14 + r() * .08);
    if (!p.aurora) s += `<circle cx="${f1(sx)}" cy="${f1(sy)}" r="${p.lowsun ? 46 : 34}" fill="${p.sun}" opacity=".95"/><circle cx="${f1(sx)}" cy="${f1(sy)}" r="${p.lowsun ? 80 : 60}" fill="${p.sun}" opacity=".18"/>`;
    else s += `<circle cx="${f1(W * .78)}" cy="120" r="20" fill="#eef6ff"/>`;
    // clouds: soft horizontal bands
    if (!p.aurora) for (let i = 0; i < 3; i++) { const cx = r() * W, cy = 60 + r() * 200, cw = 80 + r() * 120;
      s += `<rect x="${f1(cx - cw / 2)}" y="${f1(cy)}" width="${f1(cw)}" height="14" rx="7" fill="#fff" opacity=".55"/><rect x="${f1(cx - cw / 4)}" y="${f1(cy - 10)}" width="${f1(cw / 2)}" height="14" rx="7" fill="#fff" opacity=".45"/>`; }
    const horizon = 430;
    s += `<path d="${ridge(r, horizon - 40, p.fell ? 120 : 50, W, horizon + 40, wide ? 7 : 4, !!p.fell)}" fill="${p.far}"/>`;
    if (p.fell) s += `<path d="${ridge(r, horizon - 10, 60, W, horizon + 50, wide ? 6 : 3)}" fill="${p.mid}"/>`;
    if (p.city) { let x = -10; while (x < W) { const bw = 30 + r() * 40, bh = 40 + r() * 90, col = ['#e8d9b5', '#d9e4ea', '#f1c9a5', '#cfd8c4', '#f4efe4'][r() * 5 | 0];
      s += `<rect x="${f1(x)}" y="${f1(horizon - bh)}" width="${f1(bw)}" height="${f1(bh + 30)}" fill="${col}"/><path d="M${f1(x)} ${f1(horizon - bh)} h${f1(bw)} v-6 h${f1(-bw)} Z" fill="#5e6e7a"/>`;
      for (let wy = horizon - bh + 12; wy < horizon - 8; wy += 16) for (let wx = x + 6; wx < x + bw - 8; wx += 12) s += `<rect x="${f1(wx)}" y="${f1(wy)}" width="5" height="8" fill="#5f7d95" opacity=".8"/>`;
      x += bw + 2; } }
    // trees on the far shore
    const treeN = Math.round((p.spruce || 0) * (wide ? 40 : 22));
    for (let i = 0; i < treeN; i++) { const x = r() * W, sz = 40 + r() * 50; s += spruce(x, horizon + 4 + r() * 10, sz, p.mid, p.snowy); }
    if (p.ruska) for (let i = 0; i < (wide ? 24 : 12); i++) s += `<ellipse cx="${f1(r() * W)}" cy="${f1(horizon - 6 + r() * 14)}" rx="${f1(14 + r() * 16)}" ry="${f1(18 + r() * 14)}" fill="${['#e07a2e', '#c9452a', '#f2b33d'][r() * 3 | 0]}"/>`;
    if (p.cabin) { const n = p.cabin; for (let k = 0; k < n; k++) s += cabin(W * (.15 + k * .4 + r() * .2), horizon + 12, 46 + r() * 10, theme === 'cabin'); }
    if (p.lighthouse) s += `<path d="M${f1(W * .62)} ${horizon + 14} q 40 -36 110 0 Z" fill="${C.granite}"/>` + lighthouse(W * .7, horizon + 4, 120);
    if (p.sheds) for (let k = 0; k < (wide ? 7 : 4); k++) { const x = 20 + k * (W - 40) / (wide ? 7 : 4); s += `<rect x="${f1(x)}" y="${horizon - 34}" width="44" height="44" fill="${[C.falu, '#e7c46a', '#f4f8fb', '#5f8fb0'][k % 4]}"/><path d="M${f1(x - 4)} ${horizon - 34} L${f1(x + 22)} ${horizon - 54} L${f1(x + 48)} ${horizon - 34} Z" fill="#2d2f36"/>`; }
    // water or land
    if (p.lake) {
      s += `<rect x="0" y="${horizon + 10}" width="${W}" height="${H - horizon}" fill="url(#${id}w)"/>`;
      for (let i = 0; i < 26; i++) { const y = horizon + 20 + r() * 300, x = r() * W, l = 20 + r() * 80; s += `<rect x="${f1(x)}" y="${f1(y)}" width="${f1(l)}" height="2" rx="1" fill="#fff" opacity="${f1(.12 + r() * .25)}"/>`; }
      s += `<rect x="${f1(sx - 30)}" y="${horizon + 18}" width="60" height="3" fill="${p.sun}" opacity=".7"/><rect x="${f1(sx - 18)}" y="${horizon + 34}" width="36" height="3" fill="${p.sun}" opacity=".5"/>`;
      if (p.islands) for (let k = 0; k < (wide ? 6 : 3); k++) { const x = r() * W, y = horizon + 60 + k * 50 + r() * 30, w = 50 + r() * 80;
        s += `<path d="M${f1(x - w)} ${f1(y)} Q ${f1(x)} ${f1(y - 40)} ${f1(x + w)} ${f1(y)} Z" fill="${C.granite}"/>` + spruce(x, y - 18, 50, p.near) + spruce(x + 20, y - 14, 36, p.near); }
      if (p.rocks) for (let k = 0; k < 4; k++) { const x = r() * W, y = 640 + r() * 120, w = 40 + r() * 60; s += `<path d="M${f1(x - w)} ${f1(y)} Q ${f1(x - w * .3)} ${f1(y - 34)} ${f1(x + w)} ${f1(y)} Z" fill="${['#9aa5b5', '#7f8a9b', '#b3bcc8'][k % 3]}"/>`; }
      if (p.jetty) s += `<rect x="${f1(W * .3)}" y="590" width="${f1(W * .25)}" height="10" fill="#8a6a4a"/>` + [0, .08, .16, .24].map(d => `<rect x="${f1(W * (.31 + d))}" y="598" width="5" height="26" fill="#6a4a30"/>`).join('');
      if (p.boat) for (let k = 0; k < p.boat; k++) s += boat(W * (.25 + k * .4 + r() * .1), horizon + 90 + k * 60, 26, [C.falu, '#f4f8fb'][k % 2]);
    } else {
      s += `<path d="${ridge(r, horizon + 40, 40, W, H, wide ? 6 : 3)}" fill="${p.near}"/><path d="${ridge(r, 560, 50, W, H, wide ? 5 : 3)}" fill="${p.ground || p.near}"/>`;
      if (p.river) s += `<path d="M${f1(W * .45)} ${horizon + 30} C ${f1(W * .3)} 560, ${f1(W * .7)} 620, ${f1(W * .35)} ${H} L${f1(W * .75)} ${H} C ${f1(W * .95)} 640, ${f1(W * .52)} 560, ${f1(W * .55)} ${horizon + 30} Z" fill="url(#${id}w)"/>`;
      if (p.rapids) for (let i = 0; i < 14; i++) s += `<path d="M${f1(W * (.42 + r() * .3))} ${f1(560 + r() * 220)} q 8 -6 16 0" stroke="#fff" stroke-width="2.5" fill="none" opacity=".75"/>`;
      if (p.pools) for (let i = 0; i < 6; i++) s += `<ellipse cx="${f1(r() * W)}" cy="${f1(560 + r() * 200)}" rx="${f1(30 + r() * 50)}" ry="${f1(6 + r() * 8)}" fill="#6b94ad" opacity=".85"/>`;
      if (p.cotton) for (let i = 0; i < 60; i++) { const x = r() * W, y = 540 + r() * 260; s += `<path d="M${f1(x)} ${f1(y)} v-14" stroke="#7a7a50" stroke-width="1.2"/><circle cx="${f1(x)}" cy="${f1(y - 15)}" r="3.2" fill="#fff"/>`; }
      if (p.field) for (let i = 0; i < 14; i++) s += `<path d="M0 ${f1(520 + i * 22)} L${W} ${f1(510 + i * 24)}" stroke="#e8d27a" stroke-width="2" opacity=".5"/>`;
      if (p.bales) for (let i = 0; i < 5; i++) { const x = r() * W, y = 560 + r() * 160, rr = 14 + (y - 540) / 12; s += `<circle cx="${f1(x)}" cy="${f1(y)}" r="${f1(rr)}" fill="#f4f8fb"/><circle cx="${f1(x)}" cy="${f1(y)}" r="${f1(rr * .5)}" fill="none" stroke="#d8dee4" stroke-width="2"/>`; }
      if (p.birch) for (let i = 0; i < Math.round(p.birch * (wide ? 14 : 8)); i++) s += birchTree(r() * W, 600 + r() * 140, 150 + r() * 80, theme === 'autumn' ? '#f2b33d' : p.mid, r);
      if (p.spruce >= 1.2 || p.spruce === 2) for (let i = 0; i < (wide ? 12 : 7); i++) s += spruce(r() * W, 640 + r() * 160, 140 + r() * 80, p.spruce === 2 ? C.spruce2 : p.mid, p.snowy);
      if (p.berries) for (let i = 0; i < 40; i++) s += `<circle cx="${f1(r() * W)}" cy="${f1(700 + r() * 100)}" r="4" fill="${r() < .5 ? '#3b4a9a' : C.rowan}"/>`;
      if (p.flowers) for (let i = 0; i < 40; i++) s += `<circle cx="${f1(r() * W)}" cy="${f1(620 + r() * 180)}" r="${f1(2.5 + r() * 2.5)}" fill="${['#fff', '#ffe066', '#c9a7ff', C.berry][r() * 4 | 0]}"/>`;
      if (p.reindeer) for (let k = 0; k < 2; k++) s += reindeer(W * (.25 + k * .35), 640 + k * 30, 70 - k * 10);
    }
    if (p.snow) for (let i = 0; i < 60; i++) s += `<circle cx="${f1(r() * W)}" cy="${f1(r() * H)}" r="${f1(1 + r() * 2.4)}" fill="#fff" opacity=".85"/>`;
    if (p.mist) s += `<rect x="0" y="${horizon - 30}" width="${W}" height="80" fill="#fff" opacity=".35" filter="url(#${id}b)"/>`;
    if (p.gulls) for (let i = 0; i < 4; i++) { const x = r() * W, y = 150 + r() * 160; s += `<path d="M${f1(x - 9)} ${f1(y)} q 5 -6 9 0 q 4 -6 9 0" stroke="#2d3a4a" stroke-width="2" fill="none"/>`; }
    return s + '</svg>';
  }
  /* ---------- UI patterns: Nordic knit band (a row of small crystals and diamonds) ---------- */
  function ornamentTile(col, col2, size) {
    const z = size || 16;
    return `<svg xmlns="http://www.w3.org/2000/svg" width="${z}" height="${z}" viewBox="0 0 16 16"><path d="M8 2 L11 8 L8 14 L5 8 Z" fill="none" stroke="${col}" stroke-width="1.3"/><circle cx="8" cy="8" r="1.3" fill="${col2}"/><path d="M0 8 h2 M14 8 h2" stroke="${col}" stroke-width="1.3"/></svg>`;
  }
  function bandSvg(col, col2) {
    return `<svg xmlns="http://www.w3.org/2000/svg" width="48" height="12" viewBox="0 0 48 12"><path d="M0 6 L6 0 L12 6 L18 0 L24 6 L30 0 L36 6 L42 0 L48 6" stroke="${col}" stroke-width="1.4" fill="none"/><path d="M0 12 L6 6 L12 12 L18 6 L24 12 L30 6 L36 12 L42 6 L48 12" stroke="${col2}" stroke-width="1.4" fill="none"/></svg>`;
  }
  function cornerSvg() { return '<svg xmlns="http://www.w3.org/2000/svg" width="1" height="1"/>'; }
  function wheelSvg() {   // frosted ice disc with a faint crystal
    return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="-50 -50 100 100">` + snowflake(0, 0, 30, 'rgba(255,255,255,.35)', 1.2) + '</svg>';
  }
  // app icon: lake at dusk + aurora ribbon + a white crystal letter-tile
  function iconSvg(rx = 112) {
    return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><defs><linearGradient id="ib" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0b2545"/><stop offset="1" stop-color="#1d4e89"/></linearGradient>` +
      `<filter id="ibl"><feGaussianBlur stdDeviation="10"/></filter><clipPath id="icl"><rect width="512" height="512" rx="${rx}"/></clipPath></defs><g clip-path="url(#icl)"><rect width="512" height="512" fill="url(#ib)"/>` +
      `<path d="M-20 170 Q 120 90 256 160 T 540 140" stroke="#5cf2a8" stroke-width="46" fill="none" opacity=".55" filter="url(#ibl)"/>` +
      `<path d="M0 360 L60 300 L110 340 L170 280 L230 330 L290 270 L350 330 L410 290 L512 350 V512 H0 Z" fill="#123f33"/></g>` +
      `<rect x="146" y="150" width="220" height="220" rx="48" fill="#f4f8fb"/><text x="256" y="318" text-anchor="middle" font-family="Unbounded,Manrope,Arial,sans-serif" font-weight="800" font-size="150" fill="#0b2545">Ä</text>` +
      `<circle cx="352" cy="166" r="22" fill="#ff8c42"/></svg>`;
  }
  /* ---------- line icons (stroke = currentColor) ---------- */
  const I = (d, extra) => `<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${d}${extra || ''}</svg>`;
  const ICONS = {
    gear: I('<circle cx="12" cy="12" r="3.2"/><path d="M12 2.5v3M12 18.5v3M2.5 12h3M18.5 12h3M5.3 5.3l2.1 2.1M16.6 16.6l2.1 2.1M5.3 18.7l2.1-2.1M16.6 7.4l2.1-2.1"/>'),
    back: I('<path d="M15 5l-7 7 7 7"/>'),
    flame: I('<path d="M12 21c-4 0-6.5-2.7-6.5-6.2 0-3.6 3-5.6 3.6-9.3 2.6 1.5 4 3.8 4 6 1-.6 1.7-1.8 1.9-3 2 1.8 3.5 4 3.5 6.3 0 3.5-2.5 6.2-6.5 6.2z"/>'),
    shuffle: I('<path d="M4 7h3.5c2 0 3.2 1 4.3 2.8l1.4 2.4C14.3 14 15.5 15 17.5 15H20M17 12l3 3-3 3M4 15h3.5c1 0 1.8-.3 2.5-.8M14 9.8c.7-.5 1.5-.8 2.5-.8H20M17 6l3 3-3 3"/>'),
    basket: I('<path d="M3.5 10h17l-1.6 9.2a1.6 1.6 0 0 1-1.6 1.3H6.7a1.6 1.6 0 0 1-1.6-1.3z"/><path d="M8 10l3-6M16 10l-3-6M9 14v3M12 14v3M15 14v3"/>'),
    bulb: I('<path d="M9 18h6M10 21h4M12 3a6 6 0 0 0-3.6 10.8c.7.6 1.1 1.4 1.1 2.2h5c0-.8.4-1.6 1.1-2.2A6 6 0 0 0 12 3z"/>'),
    target: I('<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="4.5"/><circle cx="12" cy="12" r="1" fill="currentColor"/>'),
    film: I('<rect x="3" y="5" width="18" height="14" rx="2.5"/><path d="M10 9.5v5l4.2-2.5z" fill="currentColor"/>'),
    sunrise: I('<path d="M3 18h18M6 18a6 6 0 0 1 12 0M12 4v3M4.9 9.9l1.8 1.3M19.1 9.9l-1.8 1.3"/>'),
    flake: I('<path d="M12 2.5v19M3.8 7.2l16.4 9.6M3.8 16.8l16.4-9.6M9.6 4l2.4 2 2.4-2M9.6 20l2.4-2 2.4 2"/>'),
    gift: I('<rect x="3.5" y="8.5" width="17" height="12" rx="1.5"/><path d="M12 8.5v12M3.5 12.5h17M12 8.5c-1.5-3-5-4-5.5-2s2.5 2 5.5 2c3 0 6-.1 5.5-2s-4-1-5.5 2z"/>'),
    flag: I('<path d="M5 21V4M5 4h11l-2.2 3.5L16 11H5"/>'),
    wheel: I('<circle cx="12" cy="12" r="8.5"/><path d="M12 3.5v17M3.5 12h17M6 6l12 12M18 6L6 18"/><circle cx="12" cy="12" r="2" fill="currentColor"/>'),
    map: I('<path d="M3.5 6.5l5-2 7 2.5 5-2v13l-5 2-7-2.5-5 2z"/><path d="M8.5 4.5v13M15.5 7v13"/>'),
    book: I('<path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v15H6.5A2.5 2.5 0 0 0 4 20.5zM4 20.5A2.5 2.5 0 0 0 6.5 23H20"/><path d="M8.5 7.5h7M8.5 11h5"/>'),
    trophy: I('<path d="M8 4h8v5a4 4 0 0 1-8 0zM8 6H4.5c0 3 1.5 4.5 3.7 4.8M16 6h3.5c0 3-1.5 4.5-3.7 4.8M12 13v4M8.5 21h7M10 17h4v4h-4z"/>'),
    music: I('<path d="M9 18V5l11-2v13"/><circle cx="6.5" cy="18" r="2.5"/><circle cx="17.5" cy="16" r="2.5"/>'),
    play: I('<path d="M8 5v14l11-7z" fill="currentColor"/>'),
  };
  function uri(svg) { return 'url("data:image/svg+xml;charset=utf-8,' + encodeURIComponent(svg) + '")'; }
  const cache = {};
  window.Art = {
    themes: Object.keys(P), palette: t => P[t] || P.lake, colors: C, icons: ICONS, snowflake,
    scene, bg(theme, seed, wide) { const k = theme + ':' + seed + (wide ? ':w' : ''); return cache[k] || (cache[k] = uri(scene(theme, seed, wide))); },
    ornament(col, col2, size) { return uri(ornamentTile(col || C.ice, col2 || C.berry, size)); },
    band(col, col2) { return uri(bandSvg(col || C.ice, col2 || C.berry)); },
    corner() { return uri(cornerSvg()); },
    wheel() { return uri(wheelSvg()); }, iconSvg,
  };
})();
