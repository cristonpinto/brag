/*
 * owl-mascot: a vector owl mascot with a state engine.
 *
 * The drawing is traced from the reference owl (tools/trace.py -> shapes.generated.js).
 * The motion vocabulary follows jeremy-prt/bloub (MIT): a catalogue of states, an
 * engine that is a pure function of time, exponential ease-outs with no body
 * overshoot, a forced blink hiding most entries, and a resting life made only of
 * gaze drift and blinking. No code is copied from bloub; the timings are its.
 */
(function (global) {
  'use strict';

  const NS = 'http://www.w3.org/2000/svg';
  const DECOR = 1.45; // decor is drawn this much bigger so it still reads when the owl is ~100px
  const FRAME = SHAPES.size[0]; // the owl is drawn on a square canvas of this many units
  const TAU = Math.PI * 2;
  const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
  const lerp = (a, b, k) => a + (b - a) * k;
  const smooth = (a, b, x) => { const t = clamp((x - a) / (b - a)); return t * t * (3 - 2 * t); };
  const outQuint = (x) => 1 - Math.pow(1 - clamp(x), 5);
  /** envelope: rises a..b, holds, falls c..d */
  const bump = (s, a, b, c, d) => smooth(a, b, s) * (1 - smooth(c, d, s));
  /** pop-in with a small overshoot, like bloub's notification pastille (+14%) */
  const pop = (s, t0, dur) => {
    const x = (s - t0) / dur;
    if (x <= 0) return 0;
    if (x >= 1) return 1;
    const c1 = 2.4, c3 = c1 + 1;
    return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2);
  };
  const frac = (x) => x - Math.floor(x);
  const rnd = (i) => frac(Math.sin(i * 127.1 + 311.7) * 43758.5453);

  /* ------------------------------------------------------------ colours */
  const rgb = (c) => `rgb(${c[0]},${c[1]},${c[2]})`;
  const C = SHAPES.colors;
  const INK = rgb(C.navy);
  const RED = '#e0402d';
  const CREAM = rgb(C.cream);

  /* ------------------------------------------------------------ resting life */
  // blink calendar and gaze targets are pre-drawn, so liveliness(t) is a pure function of t
  const BLINKS = (() => {
    const out = []; let t = 1.4, k = 7;
    while (t < 3600) {
      out.push(t);
      t += 1.9 + rnd(k++) * 2.7;
      if (rnd(k++) < 0.18) { out.push(t); t += 0.24; }
    }
    return out;
  })();
  const BLINK_DUR = 0.18;
  function blinkLid(t) {
    // binary search for the last blink start <= t
    let lo = 0, hi = BLINKS.length - 1, i = -1;
    while (lo <= hi) { const m = (lo + hi) >> 1; if (BLINKS[m] <= t) { i = m; lo = m + 1; } else hi = m - 1; }
    if (i < 0) return 1;
    const k = (t - BLINKS[i]) / BLINK_DUR;
    if (k < 0 || k > 1) return 1;
    return k < 0.45 ? 1 - k / 0.45 : (k - 0.45) / 0.55;
  }
  const GAZE = (() => {
    const segs = []; let t = 0, i = 0, px = 0, py = 0;
    while (t < 3600) {
      const d = 2.2 + rnd(i * 3 + 1) * 3.2;
      const center = rnd(i * 3 + 2) < 0.18;
      const nx = center ? 0 : (rnd(i * 5 + 3) - 0.5) * 2, ny = center ? 0 : (rnd(i * 7 + 5) - 0.5) * 1.4;
      segs.push({ t, d, px, py, nx, ny });
      px = nx; py = ny; t += d; i++;
    }
    return segs;
  })();
  function gazeAt(t) {
    let lo = 0, hi = GAZE.length - 1, i = 0;
    while (lo <= hi) { const m = (lo + hi) >> 1; if (GAZE[m].t <= t) { i = m; lo = m + 1; } else hi = m - 1; }
    const g = GAZE[i], k = outQuint((t - g.t) / 0.35); // a quick saccade, then a hold
    return { x: lerp(g.px, g.nx, k), y: lerp(g.py, g.ny, k) };
  }
  function liveliness(t) {
    const g = gazeAt(t);
    return {
      gx: g.x * 13 + Math.sin(t * 0.9) * 1.2, gy: g.y * 8 + Math.sin(t * 0.7 + 1) * 0.8,
      tilt: g.x * 1.2 + Math.sin(t * 0.31 + 0.6) * 0.5,
      breath: 1 + Math.sin((t / 3.4) * TAU) * 0.004,
      lid: blinkLid(t)
    };
  }

  /* ------------------------------------------------------------ poses */
  function base() {
    return {
      gx: 0, gy: 0, ew: 1, eh: 1, lidL: 1, lidR: 1, arcL: 0, arcR: 0, arcK: 0, hlx: 0, hly: 0, hl: 1,
      tilt: 0, dx: 0, dy: 0, sx: 1, sy: 1, turn: 1, tuftL: 0, tuftR: 0, tuftUp: 0, wing: 0,
      live: 1, d: {}
    };
  }
  const NUM = ['gx', 'gy', 'ew', 'eh', 'lidL', 'lidR', 'arcL', 'arcR', 'arcK', 'hlx', 'hly', 'hl', 'tilt', 'dx', 'dy', 'sx', 'sy', 'turn', 'tuftL', 'tuftR', 'tuftUp', 'wing', 'live'];

  const BLINK_IN = 0.2; // forced blink that hides an entry, as in the reference
  const slot = (x, y, s = 1, r = 0, a = 1, z = 'f') => ({ x, y, s, r, a, z });

  /** the catalogue. `duration` is how long the full sequence holds a state. */
  const STATES = [
    {
      id: 'idle', duration: 2.4, morph: 0.45, blinkIn: false,
      pose: () => base()
    },
    {
      id: 'thinking', duration: 2.6, morph: 0.4, blinkIn: true,
      pose(s) {
        const p = base(), e = smooth(0, 0.5, s);
        p.tilt = -4.5 * e; p.gx = -17 * e; p.gy = -17 * e; p.tuftR = 4 * e; p.live = 0.35;
        for (let i = 0; i < 3; i++) {
          const w = Math.max(0, Math.sin(TAU * (s * 1.05 - i * 0.17)));
          p.d['dot' + i] = slot(420 + i * 125, 92, 0.6 + 0.75 * w * w, 0, e);
        }
        return p;
      }
    },
    {
      id: 'wink', duration: 1.6, morph: 0.3, blinkIn: true,
      pose(s) {
        const p = base(), e = smooth(0.12, 0.3, s) * (1 - smooth(1.15, 1.4, s));
        p.lidL = 1 - e; p.arcL = e; p.arcK = -38; p.tilt = 5 * e; p.gx = 6 * e; p.gy = -4 * e; p.tuftL = -3 * e; p.live = 0.4;
        return p;
      }
    },
    {
      id: 'wide', duration: 1.8, morph: 0.55, blinkIn: true,
      pose(s) {
        const p = base(), e = outQuint(s / 0.55);
        const shake = Math.sin(s * 30) * 0.8 * bump(s, 0.5, 0.6, 1.0, 1.4);
        p.ew = 1 + 0.17 * e; p.eh = p.ew; p.hl = 1 + 0.15 * e; p.tuftUp = 12 * e; p.tuftL = -9 * e; p.tuftR = 8 * e;
        p.dy = -9 * e; p.sy = 1 + 0.02 * e; p.tilt = shake; p.live = 0.5;
        return p;
      }
    },
    {
      id: 'alert', duration: 2.4, minDuration: 2, morph: 0.45, blinkIn: false,
      pose(s) {
        const p = base(), e = outQuint(s / 0.4), hop = Math.sin(clamp(s / 0.5) * Math.PI);
        p.ew = 1.12 * e + (1 - e); p.eh = p.ew; p.tuftUp = 14 * e; p.tuftL = -10 * e; p.tuftR = 10 * e;
        p.dy = -26 * hop; p.sy = 1 + 0.03 * hop;
        p.gx = lerp(-20, 14, smooth(1.0, 1.5, s)); p.gy = -6; p.live = 0.2;
        const out = 1 - smooth(1.95, 2.35, s);
        p.d.bang = slot(1135, 225, pop(s, 0.12, 0.4), Math.sin(s * 15) * 6 * bump(s, 0.5, 0.6, 1.5, 1.9), out);
        return p;
      }
    },
    {
      id: 'notify', duration: 2.2, morph: 0.5, blinkIn: true,
      pose(s) {
        const p = base(), e = smooth(0, 0.45, s);
        p.tilt = 4.5 * e; p.gx = 21 * e; p.gy = -13 * e; p.tuftR = 5 * e; p.live = 0.3;
        p.d.badge = slot(1150, 170, pop(s, 0.15, 0.5) * (1 + Math.sin(s * 6) * 0.03 * smooth(0.7, 1, s)), 0, 1 - smooth(2.0, 2.2, s));
        return p;
      }
    },
    {
      id: 'exclaim', duration: 2, morph: 0.45, blinkIn: false,
      pose(s) {
        const p = base(), e = outQuint(s / 0.35);
        p.ew = 1 + 0.1 * e; p.eh = p.ew; p.dx = -22 * e; p.tilt = -4 * e; p.tuftUp = 10 * e; p.tuftR = 9 * e; p.live = 0.2; p.gx = 18 * e; p.gy = -8 * e;
        p.d.bangI = slot(1150, 235, pop(s, 0.1, 0.45), 12 + Math.sin(s * 22) * 4 * bump(s, 0.45, 0.55, 1.2, 1.6), 1 - smooth(1.75, 2.0, s));
        return p;
      }
    },
    {
      id: 'sleep', duration: 2.4, morph: 0.5, blinkIn: false,
      pose(s) {
        const p = base(), e = smooth(0, 0.6, s);
        p.lidL = p.lidR = 1 - e; p.arcL = p.arcR = e; p.arcK = 30; p.tilt = 7 * e; p.dy = 14 * e; p.live = 0;
        p.sy = 1 + Math.sin((s / 2.9) * TAU) * 0.011; p.tuftL = 4 * e; p.tuftR = -3 * e;
        for (let i = 0; i < 3; i++) {
          const u = frac(s * 0.42 + i / 3);
          p.d['z' + i] = slot(1105 + u * 70, 330 - u * 250, 0.55 + u * 0.7, -8 + u * 16, Math.sin(Math.PI * u) * smooth(0.3, 0.9, s));
        }
        return p;
      }
    },
    {
      id: 'hop', duration: 1.8, morph: 0.4, blinkIn: true,
      pose(s) {
        const p = base();
        const crouch = bump(s, 0, 0.22, 0.22, 0.34), air = clamp((s - 0.28) / 0.5), land = bump(s, 0.76, 0.84, 0.84, 1.1);
        const arc = Math.sin(air * Math.PI), happy = bump(s, 0.15, 0.3, 1.3, 1.55);
        p.sy = 1 - 0.09 * crouch + 0.07 * arc - 0.07 * land; p.sx = 1 + 0.05 * crouch - 0.03 * arc + 0.05 * land;
        p.dy = -52 * arc; p.arcL = p.arcR = happy; p.lidL = p.lidR = 1 - happy; p.arcK = -34;
        p.tuftUp = 10 * arc; p.live = 0.3;
        return p;
      }
    },
    {
      id: 'shake', duration: 1.6, morph: 0.4, blinkIn: true,
      pose(s) {
        const p = base(), env = bump(s, 0.05, 0.2, 1.05, 1.4);
        p.tilt = Math.sin(s * TAU * 2.6) * 6.5 * env; p.dx = Math.sin(s * TAU * 2.6 + 0.6) * 14 * env;
        p.eh = 1 - 0.28 * env; p.tuftUp = -7 * env; p.tuftL = 6 * env; p.tuftR = -6 * env; p.gx = Math.sin(s * TAU * 2.6) * -10 * env; p.live = 0.2;
        return p;
      }
    },
    {
      id: 'play', duration: 2, morph: 0.5, blinkIn: true,
      pose(s) {
        const p = base(), e = smooth(0, 0.5, s);
        p.tilt = Math.sin(s * TAU * 0.8) * 4.5 * e; p.dy = -Math.abs(Math.sin(s * TAU * 0.8)) * 14 * e;
        p.gx = 18 * e; p.gy = -9 * e; p.tuftR = Math.sin(s * TAU * 1.6) * 5 * e; p.live = 0.3;
        p.d.playBtn = slot(1150, 190, pop(s, 0.15, 0.5), Math.sin(s * TAU * 0.8) * 5, 1 - smooth(1.8, 2.0, s));
        return p;
      }
    },
    {
      id: 'orbit', duration: 3.4, minDuration: 2.5, morph: 0.6, blinkIn: false,
      pose(s) {
        const p = base(), e = smooth(0, 0.6, s), out = 1 - smooth(3.0, 3.4, s);
        p.tilt = Math.sin(s * 2.2) * 3 * e; p.gx = Math.cos(s * 3.6) * 12 * e; p.gy = Math.sin(s * 3.6) * 7 * e; p.live = 0.2;
        for (let i = 0; i < 3; i++) {
          const a = TAU * (s * 0.62 + i / 3), front = Math.sin(a) > 0;
          p.d['st' + i] = slot(640 + Math.cos(a) * 400, 190 + Math.sin(a) * 74, 1.15 + 0.4 * Math.sin(a), s * 90, e * out, front ? 'f' : 'b');
        }
        return p;
      }
    },
    {
      id: 'swirl', duration: 1.3, minDuration: 1.3, morph: 0.3, blinkIn: true,
      pose(s) {
        // a quick look-around: the head sweeps left, right, then settles. Used as a transition.
        const p = base(), u = clamp((s - 0.05) / 1.15), env = Math.sin(u * Math.PI);
        p.gx = -30 * Math.sin(u * TAU) * Math.min(1, env * 2); p.gy = -6 * env;
        p.tilt = -7 * Math.sin(u * TAU) * env; p.dx = 16 * Math.sin(u * TAU) * env;
        p.ew = 1 + 0.08 * env; p.eh = p.ew; p.tuftL = -6 * env; p.tuftR = 6 * env; p.live = 0.2;
        return p;
      }
    },
    {
      id: 'burst', duration: 2.6, minDuration: 2.4, morph: 0.4, blinkIn: false,
      pose(s) {
        const p = base(), hop = Math.sin(clamp(s / 0.7) * Math.PI), happy = bump(s, 0.15, 0.3, 1.7, 2.0);
        p.dy = -40 * hop; p.sy = 1 + 0.05 * hop; p.arcL = p.arcR = happy; p.lidL = p.lidR = 1 - happy; p.arcK = -34;
        p.tuftUp = 12 * hop; p.tilt = Math.sin(s * 10) * 2 * bump(s, 0.3, 0.4, 1.2, 1.6); p.live = 0.3;
        for (let i = 0; i < 18; i++) {
          const a = TAU * (i / 18) + rnd(i) * 0.5, v = 520 + rnd(i + 40) * 360, u = Math.max(0, s - 0.25);
          const dist = v * (1 - Math.exp(-3.2 * u)), g = 140 * u * u;
          p.d['cf' + i] = slot(627 + Math.cos(a) * dist, 627 + Math.sin(a) * dist + g, 1.5 + rnd(i + 80) * 0.9, (s * 300 + i * 40) % 360, s < 0.25 ? 0 : 1 - smooth(1.6, 2.5, s));
        }
        return p;
      }
    },
    {
      id: 'comet', duration: 2.4, minDuration: 2.4, morph: 0.45, blinkIn: false,
      pose(s) {
        const p = base(), e = smooth(0, 0.5, s), out = 1 - smooth(2.1, 2.4, s), th = -1.2 + s * TAU * 0.46;
        p.gx = Math.cos(th) * 20 * e; p.gy = Math.sin(th) * 12 * e; p.live = 0.1;
        for (let j = 0; j < 8; j++) {
          const a = th - j * 0.13;
          const cs = Math.cos(a), sn = Math.sin(a);
          p.d['cm' + j] = slot(627 + 700 * Math.sign(cs) * Math.sqrt(Math.abs(cs)), 627 + 700 * Math.sign(sn) * Math.sqrt(Math.abs(sn)), 1.25 - j * 0.1, 0, e * out * (1 - j * 0.11));
        }
        return p;
      }
    },
    {
      id: 'like', duration: 1.8, morph: 0.3, blinkIn: true,
      pose(s) {
        const p = base(), arc = Math.sin(clamp((s - 0.05) / 0.55) * Math.PI), happy = bump(s, 0.08, 0.22, 1.2, 1.5);
        p.dy = -34 * arc; p.sy = 1 + 0.04 * arc; p.arcL = p.arcR = happy; p.lidL = p.lidR = 1 - happy; p.arcK = -34;
        p.tilt = Math.sin(s * 9) * 3 * bump(s, 0.2, 0.3, 0.9, 1.3); p.tuftUp = 8 * arc; p.live = 0.3;
        for (let i = 0; i < 3; i++) {
          const u = clamp((s - 0.15 - i * 0.16) / 1.2);
          p.d['h' + i] = slot(540 + i * 110 + Math.sin(u * 5 + i) * 26, 560 - u * 640, (0.5 + 0.7 * smooth(0, 0.25, u)) * (1 + i * 0.1), Math.sin(u * 4 + i) * 12, u <= 0 ? 0 : 1 - smooth(0.7, 1, u));
        }
        return p;
      }
    }
  ];
  const BY_ID = {}; STATES.forEach((d) => { BY_ID[d.id] = d; });
  /** states played in order by the full sequence (swirl is a transition, like is a reaction) */
  const SEQUENCE = ['idle', 'thinking', 'wink', 'wide', 'alert', 'notify', 'exclaim', 'sleep', 'hop', 'shake', 'play', 'orbit', 'burst', 'comet'];

  /* ------------------------------------------------------------ engine */
  /**
   * engine.sample(t) is a pure function of time and of the recorded state changes:
   * re-reading a date gives the same image, which is what the frozen board relies on.
   */
  class Engine {
    constructor() { this.cur = { id: 'idle', start: 0 }; this.from = null; this.life = true; }
    setState(id, t) {
      if (!BY_ID[id]) return;
      const def = BY_ID[this.cur.id];
      // a change landing inside a fade blends from the frozen frame that was on screen
      const inFade = t - this.cur.start < def.morph;
      this.from = inFade ? { frozen: this.sample(t, null, true) } : { id: this.cur.id, start: this.cur.start };
      this.cur = { id, start: t };
    }
    raw(id, start, t, look) {
      const def = BY_ID[id], s = Math.max(0, t - start), p = def.pose(s);
      // resting life, scaled by how much of it this pose keeps
      const lv = this.life ? liveliness(t) : { gx: 0, gy: 0, tilt: 0, breath: 1, lid: 1 }, live = p.live;
      p.gx += lv.gx * live + (look ? look.x * 22 * (look.w * Math.max(live, 0.35)) : 0);
      p.gy += lv.gy * live + (look ? look.y * 13 * (look.w * Math.max(live, 0.35)) : 0);
      p.tilt += lv.tilt * live; p.sy *= lv.breath;
      let lid = 1;
      if (live > 0.05) lid = lv.lid;
      if (def.blinkIn && s < BLINK_IN) lid = Math.min(lid, s < BLINK_IN * 0.45 ? 1 - s / (BLINK_IN * 0.45) : (s - BLINK_IN * 0.45) / (BLINK_IN * 0.55));
      p.lidL *= lid; p.lidR *= lid;
      return p;
    }
    sample(t, look, noLook) {
      const def = BY_ID[this.cur.id], k = outQuint((t - this.cur.start) / def.morph);
      const cur = this.raw(this.cur.id, this.cur.start, t, noLook ? null : look);
      if (k >= 1 || !this.from) return cur;
      const prev = this.from.frozen || this.raw(this.from.id, this.from.start, t, noLook ? null : look);
      const out = base();
      for (const key of NUM) out[key] = lerp(prev[key], cur[key], k);
      const names = new Set([...Object.keys(prev.d), ...Object.keys(cur.d)]);
      for (const n of names) {
        const a = prev.d[n], b = cur.d[n];
        if (a && b) out.d[n] = { x: lerp(a.x, b.x, k), y: lerp(a.y, b.y, k), s: lerp(a.s, b.s, k), r: lerp(a.r, b.r, k), a: lerp(a.a, b.a, k), z: b.z };
        else if (b) out.d[n] = { ...b, a: b.a * k };
        else out.d[n] = { ...a, a: a.a * (1 - k) };
      }
      return out;
    }
  }

  /* ------------------------------------------------------------ drawing */
  let uid = 0;
  const el = (tag, attrs, parent) => {
    const e = document.createElementNS(NS, tag);
    for (const k in attrs) e.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(e);
    return e;
  };
  const f1 = (n) => (Math.round(n * 10) / 10).toString();

  function makeSlot(name, badgeText) {
    const g = el('g', { opacity: 0 });
    if (/^dot/.test(name)) el('circle', { r: 30, fill: INK }, g);
    else if (name === 'bang') { el('rect', { x: -22, y: -170, width: 44, height: 190, rx: 22, fill: INK }, g); el('circle', { cy: 72, r: 27, fill: INK }, g); }
    else if (name === 'bangI') { el('rect', { x: -28, y: -150, width: 56, height: 230, rx: 28, fill: INK }, g); el('circle', { cy: 140, r: 34, fill: INK }, g); }
    else if (name === 'badge') {
      el('circle', { r: 80, fill: RED, stroke: '#fff', 'stroke-width': 10 }, g);
      const t = el('text', { 'text-anchor': 'middle', y: 32, 'font-size': 96, 'font-weight': 800, fill: '#fff', 'font-family': 'system-ui,Arial,sans-serif' }, g);
      t.textContent = badgeText; g._text = t;
    }
    else if (/^z\d/.test(name)) el('path', { d: 'M-34 -34 H34 L-34 34 H34', fill: 'none', stroke: INK, 'stroke-width': 16, 'stroke-linejoin': 'round', 'stroke-linecap': 'round' }, g);
    else if (/^st\d/.test(name)) el('path', { d: 'M0 -46 Q7 -7 46 0 Q7 7 0 46 Q-7 7 -46 0 Q-7 -7 0 -46Z', fill: '#fff4d6', stroke: INK, 'stroke-width': 7, 'stroke-linejoin': 'round' }, g);
    else if (/^cf\d/.test(name)) {
      const i = +name.slice(2), col = ['#fbe5ba', INK, RED, '#fff'][i % 4];
      if (i % 3 === 0) el('circle', { r: 15, fill: col, stroke: INK, 'stroke-width': col === INK ? 0 : 3 }, g);
      else el('rect', { x: -17, y: -9, width: 34, height: 18, rx: 4, fill: col, stroke: INK, 'stroke-width': col === INK ? 0 : 3 }, g);
    }
    else if (/^h\d/.test(name)) el('path', { d: 'M0 36 C-70 -8 -46 -62 0 -28 C46 -62 70 -8 0 36Z', fill: RED, stroke: '#fff', 'stroke-width': 7, 'stroke-linejoin': 'round' }, g);
    else if (name === 'playBtn') {
      el('circle', { r: 80, fill: CREAM, stroke: INK, 'stroke-width': 10 }, g);
      el('path', { d: 'M-22 -36 L42 0 L-22 36Z', fill: INK, stroke: INK, 'stroke-width': 10, 'stroke-linejoin': 'round' }, g);
    }
    else if (/^cm\d/.test(name)) el('circle', { r: 36 - 3.6 * (+name.slice(2)), fill: INK, stroke: '#fff', 'stroke-width': 5 }, g);
    return g;
  }

  /**
   * Draw one owl into `host`. Returns { render(pose) , svg, setBadge }.
   * `shape`: 'rounded' | 'circle' | 'square'.
   */
  function buildSvg(host, opt) {
    const id = 'owl' + (++uid);
    const svg = el('svg', { viewBox: `0 0 ${FRAME} ${FRAME}`, width: '100%', height: '100%', 'aria-hidden': 'true', focusable: 'false' });
    svg.style.overflow = 'visible'; svg.style.display = 'block';
    const defs = el('defs', {}, svg);
    // user-space gradients: every piece of the owl samples the same colour field, so the tufts blend into the body
    const grad = (gid, x1, y1, x2, y2, stops) => { const g = el('linearGradient', { id: `${id}-${gid}`, gradientUnits: 'userSpaceOnUse', x1, y1, x2, y2 }, defs); stops.forEach(([o, c]) => el('stop', { offset: o, 'stop-color': rgb(c) }, g)); };
    grad('body', 560, 0, FRAME, 0, [[0, C.navyLight], [0.55, [14, 37, 70]], [1, C.navyDark]]);
    grad('wing', 0, 0, FRAME, FRAME, [[0, [19, 43, 78]], [1, [18, 40, 74]]]);
    grad('cream', 250, 340, 1060, 940, [[0, C.creamLight], [0.5, C.cream], [1, [247, 222, 174]]]);
    const shadow = (sid, dx, dy, blur, op) => { const f = el('filter', { id: `${id}-sh-${sid}`, x: '-20%', y: '-20%', width: '140%', height: '140%' }, defs); el('feDropShadow', { dx, dy, stdDeviation: blur, 'flood-color': '#010c26', 'flood-opacity': op }, f); };
    shadow('face', 0, 16, 16, 0.55); shadow('beak', 10, 12, 8, 0.4); shadow('wing', -12, 0, 6, 0.6);
    const rx = opt.shape === 'circle' ? FRAME / 2 : opt.shape === 'square' ? 0 : FRAME * 0.22;
    const clip = el('clipPath', { id: `${id}-clip` }, defs); el('rect', { width: FRAME, height: FRAME, rx }, clip);

    const framed = el('g', { 'clip-path': `url(#${id}-clip)` }, svg);
    el('rect', { x: -300, y: -300, width: FRAME + 600, height: FRAME + 600, fill: rgb(C.yellow) }, framed);
    const back = el('g', {}, framed);
    const owl = el('g', {}, framed);
    const front = el('g', {}, svg);

    // the cropped reference runs off the right and bottom edges, so push those edges outward:
    // tilting or squashing then never reveals the background
    const bodyD = SHAPES.body.replace(/(-?\d+\.?\d*) (-?\d+\.?\d*)/g, (m, x, y) => `${+x >= FRAME - 2 ? FRAME + 500 : x} ${+y >= FRAME - 2 ? FRAME + 500 : y}`);
    el('path', { d: bodyD, fill: `url(#${id}-body)` }, owl);
    const tuftL = el('g', {}, owl); el('path', { d: SHAPES.tufts.L, fill: `url(#${id}-body)` }, tuftL);
    const tuftR = el('g', {}, owl); el('path', { d: SHAPES.tufts.R, fill: `url(#${id}-body)` }, tuftR);
    el('path', { d: SHAPES.face, fill: `url(#${id}-cream)`, filter: `url(#${id}-sh-face)` }, owl);
    const eyes = SHAPES.eyes.map((c, i) => {
      const g = el('g', {}, owl);
      el('circle', { cx: c[0], cy: c[1], r: c[2], fill: INK }, g);
      const h = SHAPES.highlights[i];
      const hl = el('circle', { cx: h[0], cy: h[1], r: h[2], fill: rgb(C.creamLight) }, g);
      const arc = el('path', { fill: 'none', stroke: INK, 'stroke-width': 30, 'stroke-linecap': 'round', opacity: 0 }, owl);
      return { g, hl, arc, c, h };
    });
    el('path', { d: SHAPES.beak, fill: INK, filter: `url(#${id}-sh-beak)` }, owl);
    const wing = el('g', { filter: `url(#${id}-sh-wing)` }, owl);
    el('path', { d: SHAPES.wing.path, fill: `url(#${id}-wing)` }, wing);

    const slots = {};
    const ensure = (name) => {
      if (!slots[name]) { const g = makeSlot(name, opt.badge || '1'); front.appendChild(g); slots[name] = { g, z: 'f' }; }
      return slots[name];
    };

    function render(p) {
      const eyeFx = [Math.max(0, -p.gx / 28), Math.max(0, p.gx / 28)];
      eyes.forEach((e, i) => {
        const lid = i === 0 ? p.lidL : p.lidR, arc = i === 0 ? p.arcL : p.arcR;
        const sx = (1 - 0.16 * clamp(eyeFx[i])) * p.ew, sy = (0.06 + 0.94 * clamp(lid)) * p.eh * p.ew;
        const [cx, cy] = e.c;
        e.g.setAttribute('transform', `translate(${f1(cx + p.gx)} ${f1(cy + p.gy)}) scale(${sx.toFixed(3)} ${sy.toFixed(3)}) translate(${-cx} ${-cy})`);
        e.hl.setAttribute('transform', `translate(${f1(p.hlx)} ${f1(p.hly)}) translate(${e.h[0]} ${e.h[1]}) scale(${p.hl.toFixed(3)}) translate(${-e.h[0]} ${-e.h[1]})`);
        e.hl.setAttribute('opacity', lid > 0.3 ? 1 : 0);
        if (arc > 0.01) {
          const ax = cx + p.gx, ay = cy + p.gy;
          e.arc.setAttribute('d', `M${f1(ax - 72)} ${f1(ay)} Q${f1(ax)} ${f1(ay + p.arcK * 1.9)} ${f1(ax + 72)} ${f1(ay)}`);
        }
        e.arc.setAttribute('opacity', clamp(arc).toFixed(2));
      });
      owl.setAttribute('transform',
        `translate(${f1(p.dx)} ${f1(p.dy)}) rotate(${p.tilt.toFixed(2)} 650 800) translate(650 ${FRAME}) scale(${(p.sx * p.turn).toFixed(3)} ${p.sy.toFixed(3)}) translate(-650 ${-FRAME})`);
      tuftL.setAttribute('transform', `translate(0 ${f1(-p.tuftUp)}) rotate(${p.tuftL.toFixed(2)} 310 400)`);
      tuftR.setAttribute('transform', `translate(0 ${f1(-p.tuftUp)}) rotate(${p.tuftR.toFixed(2)} 905 280)`);
      wing.setAttribute('transform', `rotate(${p.wing.toFixed(2)} 1000 850)`);

      for (const name in slots) if (!p.d[name]) slots[name].g.setAttribute('opacity', 0);
      for (const name in p.d) {
        const d = p.d[name], s = ensure(name);
        if (d.a < 0.01) { s.g.setAttribute('opacity', 0); continue; }
        if (d.z !== s.z) { (d.z === 'b' ? back : front).appendChild(s.g); s.z = d.z; }
        s.g.setAttribute('transform', `translate(${f1(d.x)} ${f1(d.y)}) rotate(${f1(d.r)}) scale(${(d.s * DECOR).toFixed(3)})`);
        s.g.setAttribute('opacity', clamp(d.a).toFixed(2));
      }
    }
    host.appendChild(svg);
    return {
      svg, render,
      setBadge(txt) { opt.badge = String(txt); if (slots.badge && slots.badge.g._text) slots.badge.g._text.textContent = opt.badge; }
    };
  }

  /* ------------------------------------------------------------ the mascot */
  const reducedMotion = () => !!(global.matchMedia && global.matchMedia('(prefers-reduced-motion: reduce)').matches);

  /**
   * OwlMascot.create(container, options)
   *   size       px (default 120)
   *   shape      'rounded' | 'circle' | 'square'
   *   follow     eyes follow the pointer (default true)
   *   interactive hover / click reactions (default true)
   *   autoSleep  seconds without interaction before it dozes off (0 = never, default 90)
   *   at         freeze on one exact frame (seconds into `state`): no loop, no events
   *   state      initial state
   */
  function create(container, options) {
    const opt = Object.assign({ size: 120, shape: 'rounded', follow: true, interactive: true, autoSleep: 90, state: 'idle', badge: '1' }, options || {});
    const root = document.createElement('div');
    root.className = 'owl-mascot';
    root.style.cssText = `width:${opt.size}px;height:${opt.size}px;position:relative;display:inline-block;line-height:0;touch-action:manipulation;`;
    container.appendChild(root);
    const view = buildSvg(root, opt);
    const engine = new Engine();
    if (opt.life === false) engine.life = false;
    const reduced = reducedMotion();
    let t0 = null, raf = 0, destroyed = false, holdTimer = 0, sleepTimer = 0, lastTouch = 0;
    const look = { x: 0, y: 0, w: 0, tx: 0, ty: 0, tw: 0 };
    const now = () => (global.performance ? performance.now() : Date.now()) / 1000;
    const clock = () => (t0 === null ? 0 : now() - t0);

    if (opt.at != null) {
      // one exact frame, used by the state board and the visual tests
      engine.setState(opt.state, 0);
      view.render(engine.sample(opt.at + 0, null));
      return { root, engine, state() {}, react() {}, setBadge: view.setBadge, destroy() { root.remove(); }, view };
    }
    if (opt.state !== 'idle') engine.setState(opt.state, 0);

    function frame() {
      if (destroyed) return;
      const t = clock();
      look.x += (look.tx - look.x) * 0.12; look.y += (look.ty - look.y) * 0.12; look.w += (look.tw - look.w) * 0.1;
      view.render(engine.sample(reduced ? Math.min(t, engine.cur.start + 0.9) : t, opt.follow && !reduced ? look : null));
      raf = global.requestAnimationFrame(frame);
    }
    function start() { if (t0 === null) t0 = now(); if (!raf && !destroyed) raf = global.requestAnimationFrame(frame); }
    function stop() { if (raf) global.cancelAnimationFrame(raf); raf = 0; }

    const api = {
      root, engine, view,
      /** switch state and stay there until the next call */
      state(id) { clearTimeout(holdTimer); engine.setState(id, clock()); armSleep(); return api; },
      /** play a state, then return to idle after its duration */
      react(id) {
        const def = BY_ID[id]; if (!def) return api;
        clearTimeout(holdTimer); engine.setState(id, clock()); armSleep();
        holdTimer = setTimeout(() => { if (engine.cur.id === id) engine.setState('idle', clock()); }, def.duration * 1000);
        return api;
      },
      /** the whole catalogue, one after the other */
      tour() { let i = 0; const next = () => { if (destroyed || i >= SEQUENCE.length) { api.state('idle'); return; } const id = SEQUENCE[i++]; api.state(id); holdTimer = setTimeout(next, BY_ID[id].duration * 1000); }; next(); return api; },
      setBadge: view.setBadge,
      destroy() { destroyed = true; stop(); clearTimeout(holdTimer); clearTimeout(sleepTimer); document.removeEventListener('visibilitychange', vis); global.removeEventListener('pointermove', move); root.remove(); }
    };
    function armSleep() {
      clearTimeout(sleepTimer);
      if (opt.autoSleep > 0) sleepTimer = setTimeout(() => { if (engine.cur.id === 'idle') api.state('sleep'); }, opt.autoSleep * 1000);
    }
    function wake() { if (engine.cur.id === 'sleep') api.react('wide'); else armSleep(); }
    const vis = () => { if (document.hidden) stop(); else start(); };
    function move(e) {
      const r = root.getBoundingClientRect(), cx = r.left + r.width / 2, cy = r.top + r.height / 2;
      const dx = e.clientX - cx, dy = e.clientY - cy, d = Math.hypot(dx, dy) || 1, reach = Math.max(260, global.innerWidth / 2);
      look.tx = clamp(dx / reach, -1, 1); look.ty = clamp(dy / reach, -1, 1); look.tw = 1;
      clearTimeout(lastTouch); lastTouch = setTimeout(() => { look.tw = 0; }, 2500);
      if (engine.cur.id === 'sleep' && d < r.width * 1.2) wake();
    }
    document.addEventListener('visibilitychange', vis);
    if (opt.follow) global.addEventListener('pointermove', move, { passive: true });
    if (opt.interactive) {
      root.addEventListener('pointerenter', () => { if (engine.cur.id === 'idle') api.react('wide'); else wake(); });
      const picks = ['wink', 'hop', 'like', 'play', 'swirl'];
      let n = 0;
      root.addEventListener('click', () => { wake(); api.react(picks[n++ % picks.length]); });
      root.addEventListener('dblclick', () => api.react('burst'));
    }
    armSleep(); start();
    return api;
  }

  /** draw one frozen frame (state board, thumbnails, tests) */
  function frameOf(container, state, at, options) {
    return create(container, Object.assign({}, options, { state, at }));
  }

  /* ------------------------------------------------------------ corner widget */
  const CSS = `.owl-corner{position:fixed;z-index:1030;display:flex;flex-direction:column;align-items:center;gap:6px;font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif}
.owl-corner .owl-mascot{cursor:pointer;filter:drop-shadow(0 6px 14px rgba(0,0,0,.28));transition:transform .2s}
.owl-corner .owl-mascot:active{transform:scale(.96)}
.owl-corner button.owl-like{position:absolute;right:-6px;bottom:-6px;width:34px;height:34px;border-radius:50%;border:2px solid #fff;background:#e0402d;color:#fff;font-size:16px;line-height:1;cursor:pointer;opacity:0;transform:scale(.7);transition:opacity .15s,transform .15s;padding:0;display:flex;align-items:center;justify-content:center;box-shadow:0 3px 8px rgba(0,0,0,.3)}
.owl-corner:hover button.owl-like,.owl-corner:focus-within button.owl-like{opacity:1;transform:scale(1)}
.owl-corner button.owl-like:focus-visible,.owl-corner .owl-hit:focus-visible{outline:3px solid #0f2a52;outline-offset:3px}
.owl-corner .owl-count{position:absolute;left:-4px;bottom:-4px;min-width:24px;padding:0 6px;height:24px;border-radius:12px;background:#12284a;color:#fff;font-size:13px;font-weight:700;display:none;align-items:center;justify-content:center;box-shadow:0 3px 8px rgba(0,0,0,.3)}
.owl-corner .owl-say{position:absolute;bottom:100%;right:0;margin-bottom:10px;max-width:230px;width:max-content;background:#fff;color:#12284a;border-radius:14px;padding:9px 13px;font-size:14px;line-height:1.35;box-shadow:0 6px 18px rgba(0,0,0,.25);opacity:0;transform:translateY(6px);transition:opacity .2s,transform .2s;pointer-events:none}
.owl-corner .owl-say.on{opacity:1;transform:none}
@media (prefers-reduced-motion:reduce){.owl-corner *{transition:none!important}}`;

  /**
   * OwlMascot.mount(options): a mascot pinned to a corner of the page.
   *   corner  'bottom-right' | 'bottom-left' | 'top-right' | 'top-left'
   *   offset  [x, y] px from that corner
   *   like    show the heart button (default true); `onLike(count)` is called on click
   *   moodle  wire Moodle page events ('auto' = only when Moodle is detected)
   */
  function mount(options) {
    const o = Object.assign({ corner: 'bottom-right', offset: [20, 90], size: 112, like: true, moodle: 'auto' }, options || {});
    if (!document.getElementById('owl-mascot-css')) { const s = document.createElement('style'); s.id = 'owl-mascot-css'; s.textContent = CSS; document.head.appendChild(s); }
    const box = document.createElement('div'); box.className = 'owl-corner';
    const [vy, vx] = o.corner.split('-');
    box.style[vy] = o.offset[1] + 'px'; box.style[vx] = o.offset[0] + 'px';
    document.body.appendChild(box);
    const holder = document.createElement('div'); holder.style.position = 'relative';
    holder.className = 'owl-hit';
    holder.setAttribute('role', 'button'); holder.setAttribute('tabindex', '0'); holder.setAttribute('aria-label', o.label || 'Study buddy owl. Press to interact.');
    box.appendChild(holder);
    const say = document.createElement('div'); say.className = 'owl-say'; say.setAttribute('role', 'status'); say.setAttribute('aria-live', 'polite'); box.appendChild(say);
    const owl = create(holder, Object.assign({}, o, { size: o.size }));
    let likes = 0, sayTimer = 0;
    const countEl = document.createElement('span'); countEl.className = 'owl-count'; holder.appendChild(countEl);
    owl.say = (text, ms = 3200) => { say.textContent = text; say.classList.add('on'); clearTimeout(sayTimer); sayTimer = setTimeout(() => say.classList.remove('on'), ms); return owl; };
    owl.like = () => { likes++; countEl.textContent = likes; countEl.style.display = 'flex'; owl.react('like'); if (o.onLike) o.onLike(likes); return owl; };
    if (o.like) {
      const b = document.createElement('button'); b.type = 'button'; b.className = 'owl-like'; b.setAttribute('aria-label', 'Like'); b.textContent = '♥';
      b.addEventListener('click', (e) => { e.stopPropagation(); owl.like(); });
      holder.appendChild(b);
    }
    holder.addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); holder.click(); } });
    const wrapDestroy = owl.destroy; owl.destroy = () => { wrapDestroy(); box.remove(); };
    owl.box = box;
    const isMoodle = !!(global.M && global.M.cfg) || /moodle/i.test(document.body.className + ' ' + (document.documentElement.getAttribute('data-theme') || ''));
    if (o.moodle === true || (o.moodle === 'auto' && isMoodle)) moodleHooks(owl, o);
    return owl;
  }

  /* ------------------------------------------------------------ Moodle */
  /**
   * Reactions to what a Moodle page does. These read the page, they do not call
   * Moodle APIs, so a theme that renames a class only loses that one reaction.
   */
  function moodleHooks(owl, o) {
    const safe = (fn) => (...a) => { try { fn(...a); } catch (e) { /* a missing selector must never break the page */ } };
    const text = (n) => parseInt((n && n.textContent || '').replace(/\D+/g, ''), 10) || 0;
    const body = document.body, id = body.id || '';

    // 1. first visit of the session: a wink
    safe(() => { if (!sessionStorage.getItem('owl-mascot-hello')) { sessionStorage.setItem('owl-mascot-hello', '1'); setTimeout(() => owl.react('wink'), 1200); } })();

    // 2. the notification counter in the navbar went up
    const counter = () => document.querySelector('.popover-region-notifications [data-region="count-container"], #nav-notification-popover-container [data-region="count-container"]');
    let last = text(counter());
    new MutationObserver(safe(() => { const n = text(counter()); if (n > last) { owl.setBadge(n); owl.react('notify'); owl.say && owl.say(n === 1 ? 'You have a new notification' : `You have ${n} notifications`); } last = n; }))
      .observe(body, { childList: true, subtree: true, characterData: true });

    // 3. alerts and toasts that appear on the page
    const seen = new WeakSet();
    const scan = safe((root) => {
      root.querySelectorAll && root.querySelectorAll('.alert-success, .alert-danger, .alert-error, .alert-warning, .toast').forEach((n) => {
        if (seen.has(n)) return; seen.add(n);
        const c = n.className;
        if (/danger|error/.test(c)) owl.react('alert'); else if (/warning/.test(c)) owl.react('exclaim'); else owl.react('hop');
      });
    });
    setTimeout(() => scan(document), 700);
    new MutationObserver(safe((muts) => muts.forEach((m) => m.addedNodes.forEach((n) => { if (n.nodeType === 1) { if (n.matches && n.matches('.alert, .toast')) scan(n.parentNode); else scan(n); } })))).observe(body, { childList: true, subtree: true });

    // 4. an activity marked as done
    document.addEventListener('click', safe((e) => {
      const b = e.target.closest && e.target.closest('[data-action="toggle-manual-completion"]');
      if (b) setTimeout(() => { if (b.classList.contains('btn-success')) owl.react('burst'); }, 700);
    }));

    // 5. a quiz was finished and is being reviewed
    if (id === 'page-mod-quiz-review') setTimeout(() => owl.react('burst'), 900);

    // 6. a form is being sent: look busy until the page changes
    document.addEventListener('submit', safe(() => owl.state('thinking')), true);
  }

  global.OwlMascot = { create, mount, frame: frameOf, STATES, SEQUENCE, Engine, version: '1.0.0' };
})(typeof window !== 'undefined' ? window : globalThis);
