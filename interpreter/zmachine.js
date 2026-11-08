// zmachine.js - a Z-machine interpreter (versions 3, 4, 5, 7 and 8) for text adventures in the browser.
// The core (ZMachine) knows nothing about the page: it talks to an "io" object with these methods:
//   print(text), setStyle(bits), splitWindow(lines), setWindow(w), eraseWindow(w), setCursor(line, col),
//   eraseLine(), statusV3(name, a, b, isTime), requestLine(maxLength), requestChar(), quit(),
//   save(key, json) -> bool, restore(key) -> json or null
// When the game wants input, run() returns; the page calls line(text) or char(code) to continue.
(function (root) {
  "use strict";

  const A0 = "abcdefghijklmnopqrstuvwxyz", A1 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
  const A2v1 = " 0123456789.,!?_#'\"/\\<-:()", A2 = " \n0123456789.,!?_#'\"/\\-:()";
  const UNI = "äöüÄÖÜß»«ëïÿËÏáéíóúýÁÉÍÓÚÝàèìòùÀÈÌÒÙâêîôûÂÊÎÔÛåÅøØãñõÃÑÕæÆçÇþðÞÐ£œŒ¡¿";
  const s16 = (v) => (v << 16) >> 16;

  class ZMachine {
    constructor(bytes, io) {
      this.story = new Uint8Array(bytes);
      this.io = io;
      this.restartGame(true);
    }

    // ------------------------------------------------------------------ setup
    restartGame(first) {
      const keepFlags = first ? 0 : this.mem[0x11] & 3;
      this.mem = new Uint8Array(this.story);
      const m = this.mem;
      this.version = m[0];
      if (![1, 2, 3, 4, 5, 7, 8].includes(this.version)) throw new Error("Unsupported Z-machine version " + this.version);
      this.pm = this.version <= 3 ? 2 : this.version <= 5 ? 4 : 8;
      this.globals = this.w(0x0c);
      this.objTable = this.w(0x0a);
      this.abbrev = this.w(0x18);
      this.staticBase = this.w(0x0e);
      this.dict = this.w(0x08);
      if (this.version >= 6) { this.routineOff = this.w(0x28) * 8; this.stringOff = this.w(0x2a) * 8; }
      else { this.routineOff = this.stringOff = 0; }
      this.alphabet = null;
      if (this.version >= 5 && this.w(0x34)) {
        const a = this.w(0x34), t = [];
        for (let i = 0; i < 78; i++) t.push(m[a + i]);
        this.alphabet = t;
      }
      this.uniTable = this.version >= 5 && this.w(0x36) && this.w(this.w(0x36)) >= 3 ? this.w(this.w(0x36) + 6) : 0;
      this.stack = [];
      this.frames = [];
      this.frame = { locals: [], base: 0, store: -1, args: 0, ret: 0 };
      this.streams3 = [];
      this.screenOn = true;
      this.halted = false;
      this.waiting = null;
      this.undo = null;
      this.seedRandom(0);
      this.setHeader();
      m[0x11] = (m[0x11] & ~3) | keepFlags;
      if (this.version === 6) this.pc = this.unpack(this.w(6), true) + 1;
      else this.pc = this.w(6);
    }

    setHeader() {
      const m = this.mem, cols = this.io.cols || 80, rows = this.io.rows || 255;
      if (this.version <= 3) {
        m[1] = (m[1] & ~0x70) | 0x20; // split screen available, status line available
      } else {
        m[1] = (m[1] | 0x1c) & ~0x80; // bold, italic, fixed-space; no timed input
        if (this.version >= 5) m[1] |= 0x01; // colours
        m[0x1e] = 6; m[0x1f] = 65;
        m[0x20] = rows; m[0x21] = cols;
        if (this.version >= 5) {
          this.sw(0x22, cols); this.sw(0x24, rows); m[0x26] = 1; m[0x27] = 1;
          m[0x2c] = 2; m[0x2d] = 9; // default background black, foreground white
        }
      }
      m[0x10] &= ~0x08; // no pictures
      if (this.version >= 5) m[0x11] &= ~(0x08 | 0x20 | 0x80); // no pictures, mouse, sound
      m[0x32] = 1; m[0x33] = 1;
    }

    // ------------------------------------------------------------------ memory
    w(a) { return (this.mem[a] << 8) | this.mem[a + 1]; }
    sw(a, v) { this.mem[a] = (v >> 8) & 255; this.mem[a + 1] = v & 255; }
    unpack(p, routine) {
      return p * this.pm + (this.version >= 6 ? (routine ? this.routineOff : this.stringOff) : 0);
    }
    checkWrite(a) {
      if (a >= this.staticBase) throw new Error("Write to static memory at " + a.toString(16));
    }
    storeb(a, v) { this.checkWrite(a); this.mem[a] = v & 255; }
    storew(a, v) { this.checkWrite(a + 1); this.sw(a, v & 0xffff); }

    // ------------------------------------------------------------------ variables
    getVar(n) {
      if (n === 0) {
        if (this.stack.length <= this.frame.base) throw new Error("Stack underflow");
        return this.stack.pop();
      }
      if (n < 16) return this.frame.locals[n - 1];
      return this.w(this.globals + 2 * (n - 16));
    }
    setVar(n, v) {
      v &= 0xffff;
      if (n === 0) this.stack.push(v);
      else if (n < 16) this.frame.locals[n - 1] = v;
      else this.sw(this.globals + 2 * (n - 16), v);
    }
    peekVar(n) { return n === 0 ? this.stack[this.stack.length - 1] : this.getVar(n); }
    pokeVar(n, v) {
      if (n === 0) this.stack[this.stack.length - 1] = v & 0xffff;
      else this.setVar(n, v);
    }

    // ------------------------------------------------------------------ text
    decode(addr, out) {
      // returns the address after the string; appends the characters to out (array)
      const m = this.mem;
      let alpha = 0, shiftLock = 0, abbrevNext = 0, escape = 0, esc1 = 0;
      for (;;) {
        const word = (m[addr] << 8) | m[addr + 1];
        addr += 2;
        for (const z of [(word >> 10) & 31, (word >> 5) & 31, word & 31]) {
          if (abbrevNext) {
            const a = this.w(this.abbrev + 2 * (32 * (abbrevNext - 1) + z)) * 2;
            this.decode(a, out);
            abbrevNext = 0; alpha = shiftLock;
            continue;
          }
          if (escape === 1) { esc1 = z; escape = 2; continue; }
          if (escape === 2) { out.push(this.zsciiChar((esc1 << 5) | z)); escape = 0; alpha = shiftLock; continue; }
          if (z === 0) { out.push(" "); alpha = shiftLock; continue; }
          if (z <= 3 && (this.version >= 3 || (this.version === 2 && z === 1))) { abbrevNext = z; continue; }
          if (z === 1 && this.version === 1) { out.push("\n"); continue; }
          if (z === 4 || z === 5) {
            if (this.version <= 2) {
              if (z === 2) alpha = (shiftLock + 1) % 3;
              else if (z === 3) alpha = (shiftLock + 2) % 3;
              else { shiftLock = (shiftLock + (z === 4 ? 1 : 2)) % 3; alpha = shiftLock; }
            } else alpha = z === 4 ? 1 : 2;
            continue;
          }
          if (alpha === 2 && z === 6) { escape = 1; alpha = shiftLock; continue; }
          out.push(this.alphaChar(alpha, z - 6));
          alpha = shiftLock;
        }
        if (word & 0x8000) return addr;
      }
    }
    alphaChar(alpha, i) {
      if (this.alphabet) {
        const c = this.alphabet[alpha * 26 + i];
        if (alpha === 2 && i === 1) return "\n";
        return this.zsciiChar(c);
      }
      if (alpha === 0) return A0[i];
      if (alpha === 1) return A1[i];
      return (this.version === 1 ? A2v1 : A2)[i];
    }
    zsciiChar(c) {
      if (c === 13) return "\n";
      if (c >= 32 && c <= 126) return String.fromCharCode(c);
      if (c >= 155 && c <= 251) {
        if (this.uniTable) {
          const n = this.mem[this.uniTable];
          if (c - 155 < n) return String.fromCharCode(this.w(this.uniTable + 1 + 2 * (c - 155)));
          return "?";
        }
        return c - 155 < UNI.length ? UNI[c - 155] : "?";
      }
      if (c === 0) return "";
      return "?";
    }
    charZscii(ch) {
      const o = ch.charCodeAt(0);
      if (o >= 32 && o <= 126) return o;
      if (ch === "\n" || ch === "\r") return 13;
      const i = UNI.indexOf(ch);
      return i >= 0 ? 155 + i : 63;
    }
    readString(addr) { const out = []; this.decode(addr, out); return out.join(""); }

    // ------------------------------------------------------------------ output
    print(text) {
      if (!text) return;
      if (this.streams3.length) {
        const s = this.streams3[this.streams3.length - 1];
        for (const ch of text) { this.mem[s.addr + 2 + s.len] = this.charZscii(ch); s.len++; }
        return;
      }
      if (this.screenOn) this.io.print(text);
    }

    // ------------------------------------------------------------------ objects
    objAddr(o) {
      return this.version <= 3 ? this.objTable + 62 + (o - 1) * 9 : this.objTable + 126 + (o - 1) * 14;
    }
    parent(o) { const a = this.objAddr(o); return this.version <= 3 ? this.mem[a + 4] : this.w(a + 6); }
    sibling(o) { const a = this.objAddr(o); return this.version <= 3 ? this.mem[a + 5] : this.w(a + 8); }
    child(o) { const a = this.objAddr(o); return this.version <= 3 ? this.mem[a + 6] : this.w(a + 10); }
    setRel(o, which, v) {
      const a = this.objAddr(o);
      if (this.version <= 3) this.mem[a + 4 + which] = v;
      else this.sw(a + 6 + 2 * which, v);
    }
    propTable(o) { const a = this.objAddr(o); return this.w(a + (this.version <= 3 ? 7 : 12)); }
    objName(o) { const p = this.propTable(o); return this.mem[p] ? this.readString(p + 1) : ""; }
    testAttr(o, a) { return (this.mem[this.objAddr(o) + (a >> 3)] >> (7 - (a & 7))) & 1; }
    setAttr(o, a, on) {
      const ad = this.objAddr(o) + (a >> 3), bit = 0x80 >> (a & 7);
      if (on) this.mem[ad] |= bit; else this.mem[ad] &= ~bit;
    }
    detach(o) {
      const p = this.parent(o);
      if (!p) return;
      const sib = this.sibling(o);
      if (this.child(p) === o) this.setRel(p, 2, sib);
      else {
        let c = this.child(p);
        while (c) {
          const n = this.sibling(c);
          if (n === o) { this.setRel(c, 1, sib); break; }
          c = n;
        }
      }
      this.setRel(o, 0, 0);
      this.setRel(o, 1, 0);
    }
    insert(o, d) {
      this.detach(o);
      this.setRel(o, 1, this.child(d));
      this.setRel(d, 2, o);
      this.setRel(o, 0, d);
    }
    // property walking: returns [number, dataAddr, size] for the property at entry address a
    propAt(a) {
      const b = this.mem[a];
      if (this.version <= 3) return [b & 31, a + 1, (b >> 5) + 1];
      if (b & 0x80) {
        const s = this.mem[a + 1] & 63;
        return [b & 63, a + 2, s === 0 ? 64 : s];
      }
      return [b & 63, a + 1, b & 0x40 ? 2 : 1];
    }
    firstProp(o) { const p = this.propTable(o); return p + 1 + 2 * this.mem[p]; }
    findProp(o, n) {
      let a = this.firstProp(o);
      while (this.mem[a]) {
        const [num, data, size] = this.propAt(a);
        if (num === n) return [data, size];
        if (num < n) return null;
        a = data + size;
      }
      return null;
    }
    getProp(o, n) {
      const f = this.findProp(o, n);
      if (!f) return this.w(this.objTable + 2 * (n - 1));
      return f[1] === 1 ? this.mem[f[0]] : this.w(f[0]);
    }
    propLen(a) {
      if (a === 0) return 0;
      const b = this.mem[a - 1];
      if (this.version <= 3) return (b >> 5) + 1;
      if (b & 0x80) { const s = b & 63; return s === 0 ? 64 : s; }
      return b & 0x40 ? 2 : 1;
    }

    // ------------------------------------------------------------------ dictionary
    encodeWord(chars) {
      const n = this.version <= 3 ? 6 : 9, z = [];
      for (const ch of chars) {
        if (z.length >= n) break;
        const c = ch.toLowerCase();
        let i = -1;
        if (this.alphabet) {
          const code = this.charZscii(c);
          i = this.alphabet.indexOf(code);
          if (i >= 0 && i < 26) { z.push(i + 6); continue; }
          if (i >= 52 && i !== 52 && i !== 53) { z.push(5, i - 52 + 6); continue; }
        } else {
          i = A0.indexOf(c);
          if (i >= 0) { z.push(i + 6); continue; }
          i = (this.version === 1 ? A2v1 : A2).indexOf(c);
          if (i >= 2 || (this.version === 1 && i >= 1)) { z.push(this.version <= 2 ? 3 : 5, i + 6); continue; }
        }
        const code = this.charZscii(c);
        z.push(5, 6, code >> 5, code & 31);
      }
      while (z.length < n) z.push(5);
      z.length = n;
      const words = [];
      for (let i = 0; i < n; i += 3) words.push((z[i] << 10) | (z[i + 1] << 5) | z[i + 2]);
      words[words.length - 1] |= 0x8000;
      return words;
    }
    lookup(word, dict) {
      const m = this.mem, nsep = m[dict], elen = m[dict + nsep + 1];
      let count = s16(this.w(dict + nsep + 2));
      const start = dict + nsep + 4, enc = this.encodeWord(word);
      count = Math.abs(count);
      for (let i = 0; i < count; i++) {
        const a = start + i * elen;
        let ok = true;
        for (let j = 0; j < enc.length; j++) if (this.w(a + 2 * j) !== enc[j]) { ok = false; break; }
        if (ok) return a;
      }
      return 0;
    }
    tokenise(text, parse, dict, flag) {
      const m = this.mem;
      dict = dict || this.dict;
      const nsep = m[dict], seps = [];
      for (let i = 0; i < nsep; i++) seps.push(String.fromCharCode(m[dict + 1 + i]));
      let start, end;
      if (this.version >= 5) { start = text + 2; end = start + m[text + 1]; }
      else { start = text + 1; end = start; while (m[end]) end++; }
      const tokens = [];
      let i = start;
      while (i < end) {
        const ch = String.fromCharCode(m[i]);
        if (ch === " ") { i++; continue; }
        if (seps.includes(ch)) { tokens.push([ch, i - text]); i++; continue; }
        let j = i, w = "";
        while (j < end) {
          const c = String.fromCharCode(m[j]);
          if (c === " " || seps.includes(c)) break;
          w += this.zsciiChar(m[j]); j++;
        }
        tokens.push([w, i - text]);
        i = j;
      }
      const max = m[parse];
      let n = 0;
      for (const [w, pos] of tokens) {
        if (n >= max) break;
        const a = this.lookup(w, dict), e = parse + 2 + 4 * n;
        if (!(flag && a === 0)) {
          this.sw(e, a); m[e + 2] = w.length; m[e + 3] = pos;
        }
        n++;
      }
      m[parse + 1] = n;
    }

    // ------------------------------------------------------------------ calls
    call(addr, args, store) {
      if (addr === 0) { if (store >= 0) this.setVar(store, 0); return; }
      const a = this.unpack(addr, true), m = this.mem;
      const n = m[a];
      const locals = [];
      let pc = a + 1;
      for (let i = 0; i < n; i++) {
        if (this.version <= 4) { locals.push(this.w(pc)); pc += 2; } else locals.push(0);
      }
      for (let i = 0; i < args.length && i < n; i++) locals[i] = args[i];
      this.frames.push(this.frame);
      this.frame = { locals, base: this.stack.length, store, args: args.length, ret: this.pc };
      this.pc = pc;
    }
    ret(v) {
      const f = this.frame;
      this.stack.length = f.base;
      this.frame = this.frames.pop();
      this.pc = f.ret;
      if (f.store >= 0) this.setVar(f.store, v);
    }
    branch(cond) {
      const m = this.mem;
      let b = m[this.pc++];
      const onTrue = b & 0x80;
      let off;
      if (b & 0x40) off = b & 0x3f;
      else { off = ((b & 0x3f) << 8) | m[this.pc++]; if (off & 0x2000) off -= 0x4000; }
      if (!cond === !onTrue) {
        if (off === 0 || off === 1) this.ret(off);
        else this.pc += off - 2;
      }
    }

    // ------------------------------------------------------------------ random
    seedRandom(s) {
      this.seq = 0;
      if (s === 0) { this.rmode = 0; return; }
      if (s < 1000) { this.rmode = 1; this.seqMax = s; this.seq = 0; return; }
      this.rmode = 2; this.rs = s >>> 0;
    }
    random(n) {
      if (this.rmode === 1) { this.seq = (this.seq % this.seqMax) + 1; return ((this.seq - 1) % n) + 1; }
      if (this.rmode === 2) { this.rs = (Math.imul(this.rs, 1103515245) + 12345) >>> 0; return ((this.rs >>> 8) % n) + 1; }
      return Math.floor(Math.random() * n) + 1;
    }

    // ------------------------------------------------------------------ save/restore
    snapshot() {
      return {
        mem: Array.from(this.mem.subarray(0, this.staticBase)),
        stack: this.stack.slice(),
        frames: this.frames.map((f) => ({ ...f, locals: f.locals.slice() })),
        frame: { ...this.frame, locals: this.frame.locals.slice() },
        pc: this.pc,
      };
    }
    load(s) {
      const keep = this.mem[0x11] & 3;
      this.mem.set(s.mem, 0);
      this.mem[0x11] = (this.mem[0x11] & ~3) | keep;
      this.setHeader();
      this.stack = s.stack.slice();
      this.frames = s.frames.map((f) => ({ ...f, locals: f.locals.slice() }));
      this.frame = { ...s.frame, locals: s.frame.locals.slice() };
      this.pc = s.pc;
    }
    saveKey() {
      let serial = "";
      for (let i = 0x12; i < 0x18; i++) serial += String.fromCharCode(this.mem[i]);
      return "zsave:" + this.w(2) + ":" + serial + ":" + this.w(0x1c);
    }
    packState(s) {
      let bin = "";
      for (const b of s.mem) bin += String.fromCharCode(b);
      return JSON.stringify({ ...s, mem: btoa(bin) });
    }
    unpackState(json) {
      const s = JSON.parse(json), bin = atob(s.mem), mem = [];
      for (let i = 0; i < bin.length; i++) mem.push(bin.charCodeAt(i));
      s.mem = mem;
      return s;
    }

    // ------------------------------------------------------------------ input
    line(input) {
      const wt = this.waiting;
      if (!wt || wt.type !== "line") return;
      this.waiting = null;
      const m = this.mem, max = wt.max;
      let s = input.toLowerCase().slice(0, max);
      const codes = Array.from(s).map((c) => this.charZscii(c));
      if (this.version >= 5) {
        for (let i = 0; i < codes.length; i++) m[wt.text + 2 + i] = codes[i];
        m[wt.text + 1] = codes.length;
      } else {
        for (let i = 0; i < codes.length; i++) m[wt.text + 1 + i] = codes[i];
        m[wt.text + 1 + codes.length] = 0;
      }
      if (wt.parse) this.tokenise(wt.text, wt.parse, 0, 0);
      if (this.version >= 5) this.setVar(wt.store, 13);
      this.run();
    }
    char(code) {
      const wt = this.waiting;
      if (!wt || wt.type !== "char") return;
      this.waiting = null;
      this.setVar(wt.store, code);
      this.run();
    }

    // ------------------------------------------------------------------ main loop
    run() {
      try {
        let n = 0;
        while (!this.halted && !this.waiting) {
          this.step();
          if (++n > 5e6) { this.io.print("\n[The story seems to be stuck in a loop.]\n"); this.halted = true; }
        }
      } catch (e) {
        this.halted = true;
        this.io.print("\n[Z-machine error: " + e.message + "]\n");
        if (typeof console !== "undefined") console.error(e);
      }
      if (this.halted) this.io.quit();
    }

    operand(type) {
      const m = this.mem;
      if (type === 0) { const v = this.w(this.pc); this.pc += 2; return v; }
      if (type === 1) return m[this.pc++];
      return this.getVar(m[this.pc++]);
    }
    varOperands(bytes) {
      const types = [];
      for (const b of bytes) for (let s = 6; s >= 0; s -= 2) types.push((b >> s) & 3);
      const ops = [];
      for (const t of types) { if (t === 3) break; ops.push(this.operand(t)); }
      return ops;
    }

    step() {
      const m = this.mem;
      const op = m[this.pc++];
      let kind, num, ops;
      if (op === 0xbe && this.version >= 5) {
        num = m[this.pc++]; kind = 4;
        ops = this.varOperands([m[this.pc++]]);
      } else if (op >= 0xc0) {
        num = op & 0x1f;
        kind = op & 0x20 ? 3 : 2;
        if (kind === 3 && (num === 12 || num === 26)) { const b1 = m[this.pc++], b2 = m[this.pc++]; ops = this.varOperands([b1, b2]); }
        else ops = this.varOperands([m[this.pc++]]);
      } else if (op >= 0x80) {
        const t = (op >> 4) & 3;
        num = op & 15;
        if (t === 3) { kind = 0; ops = []; }
        else { kind = 1; ops = [this.operand(t)]; }
      } else {
        kind = 2; num = op & 0x1f;
        const a = op & 0x40 ? this.getVar(m[this.pc++]) : m[this.pc++];
        const b = op & 0x20 ? this.getVar(m[this.pc++]) : m[this.pc++];
        ops = [a, b];
      }
      this.exec(kind, num, ops, op);
    }

    st(v) { this.setVar(this.mem[this.pc++], v); }

    exec(kind, num, o, op) {
      const m = this.mem, V = this.version;
      const [a, b] = o;
      if (kind === 2) {
        switch (num) {
          case 1: this.branch(o.slice(1).includes(a)); return;
          case 2: this.branch(s16(a) < s16(b)); return;
          case 3: this.branch(s16(a) > s16(b)); return;
          case 4: { const v = s16(this.peekVar(a)) - 1; this.pokeVar(a, v); this.branch(v < s16(b)); return; }
          case 5: { const v = s16(this.peekVar(a)) + 1; this.pokeVar(a, v); this.branch(v > s16(b)); return; }
          case 6: this.branch(this.parent(a) === b); return;
          case 7: this.branch((a & b) === b); return;
          case 8: this.st(a | b); return;
          case 9: this.st(a & b); return;
          case 10: this.branch(this.testAttr(a, b)); return;
          case 11: this.setAttr(a, b, true); return;
          case 12: this.setAttr(a, b, false); return;
          case 13: this.pokeVar(a, b); return;
          case 14: this.insert(a, b); return;
          case 15: this.st(this.w((a + 2 * b) & 0xffff)); return;
          case 16: this.st(m[(a + b) & 0xffff]); return;
          case 17: this.st(this.getProp(a, b)); return;
          case 18: { const f = a ? this.findProp(a, b) : null; this.st(f ? f[0] : 0); return; }
          case 19: {
            let r = 0;
            if (b === 0) { const p = this.firstProp(a); r = m[p] ? this.propAt(p)[0] : 0; }
            else {
              const f = this.findProp(a, b);
              if (!f) throw new Error("get_next_prop: no property " + b);
              const nx = f[0] + f[1];
              r = m[nx] ? this.propAt(nx)[0] : 0;
            }
            this.st(r); return;
          }
          case 20: this.st(a + b); return;
          case 21: this.st(a - b); return;
          case 22: this.st(Math.imul(a, b)); return;
          case 23: if (s16(b) === 0) throw new Error("Division by zero"); this.st(Math.trunc(s16(a) / s16(b))); return;
          case 24: if (s16(b) === 0) throw new Error("Division by zero"); this.st(s16(a) % s16(b)); return;
          case 25: this.call(a, o.slice(1), m[this.pc++]); return;
          case 26: this.call(a, o.slice(1), -1); return;
          case 27: if (this.io.setColour) this.io.setColour(a, b); return;
          case 28: {
            while (this.frames.length && this.frames.length + 1 > b) { this.frame = this.frames.pop(); }
            const f = this.frame; this.frame = this.frames.pop();
            this.frames.push(this.frame); this.frame = f;
            this.ret(a); return;
          }
        }
      } else if (kind === 1) {
        switch (num) {
          case 0: this.branch(a === 0); return;
          case 1: { const s = a ? this.sibling(a) : 0; this.st(s); this.branch(s !== 0); return; }
          case 2: { const c = a ? this.child(a) : 0; this.st(c); this.branch(c !== 0); return; }
          case 3: this.st(a ? this.parent(a) : 0); return;
          case 4: this.st(this.propLen(a)); return;
          case 5: this.pokeVar(a, this.peekVar(a) + 1); return;
          case 6: this.pokeVar(a, this.peekVar(a) - 1); return;
          case 7: this.print(this.readString(a)); return;
          case 8: this.call(a, [], m[this.pc++]); return;
          case 9: this.detach(a); return;
          case 10: this.print(this.objName(a)); return;
          case 11: this.ret(a); return;
          case 12: this.pc += s16(a) - 2; return;
          case 13: this.print(this.readString(this.unpack(a, false))); return;
          case 14: this.st(this.peekVar(a)); return;
          case 15: if (V >= 5) this.call(a, [], -1); else this.st((~a) & 0xffff); return;
        }
      } else if (kind === 0) {
        switch (num) {
          case 0: this.ret(1); return;
          case 1: this.ret(0); return;
          case 2: { const out = []; this.pc = this.decode(this.pc, out); this.print(out.join("")); return; }
          case 3: { const out = []; this.pc = this.decode(this.pc, out); this.print(out.join("") + "\n"); this.ret(1); return; }
          case 4: return;
          case 5: { const ok = this.doSave(); if (V <= 3) this.branch(ok); else this.st(ok ? 1 : 0); return; }
          case 6: { const r = this.doRestore(); if (!r) { if (V <= 3) this.branch(false); else this.st(0); } return; }
          case 7: this.restartGame(false); return;
          case 8: this.ret(this.getVar(0)); return;
          case 9: if (V >= 5) this.st(this.frames.length + 1); else this.getVar(0); return;
          case 10: this.halted = true; return;
          case 11: this.print("\n"); return;
          case 12: this.showStatus(); return;
          case 13: this.branch(true); return;
          case 15: this.branch(true); return;
        }
      } else if (kind === 3) {
        switch (num) {
          case 0: this.call(a, o.slice(1), m[this.pc++]); return;
          case 1: this.storew((a + 2 * b) & 0xffff, o[2]); return;
          case 2: this.storeb((a + b) & 0xffff, o[2]); return;
          case 3: {
            const f = this.findProp(a, b);
            if (!f) throw new Error("put_prop: object " + a + " has no property " + b);
            if (f[1] === 1) m[f[0]] = o[2] & 255; else this.sw(f[0], o[2]);
            return;
          }
          case 4: {
            if (V <= 3) this.showStatus();
            const max = V >= 5 ? m[a] : m[a] - 1;
            this.waiting = { type: "line", text: a, parse: b || 0, store: V >= 5 ? m[this.pc++] : -1, max };
            this.io.requestLine(max);
            return;
          }
          case 5: this.print(this.zsciiChar(a)); return;
          case 6: this.print(String(s16(a))); return;
          case 7: {
            const n = s16(a);
            if (n > 0) this.st(this.random(n));
            else { this.seedRandom(-n); this.st(0); }
            return;
          }
          case 8: this.setVar(0, a); return;
          case 9: {
            if (V === 6) { const v = this.getVar(0); this.st(v); }
            else { const v = this.getVar(0); this.pokeVar(a, v); }
            return;
          }
          case 10: this.io.splitWindow(a); return;
          case 11: this.io.setWindow(a); return;
          case 12: this.call(a, o.slice(1), m[this.pc++]); return;
          case 13: this.io.eraseWindow(s16(a)); return;
          case 14: if (a === 1) this.io.eraseLine(); return;
          case 15: this.io.setCursor(s16(a), b); return;
          case 16: { const c = this.io.getCursor ? this.io.getCursor() : [1, 1]; this.storew(a, c[0]); this.storew(a + 2, c[1]); return; }
          case 17: this.io.setStyle(a); return;
          case 18: return;
          case 19: {
            const n = s16(a);
            if (n === 3) { this.streams3.push({ addr: b, len: 0 }); }
            else if (n === -3) { const s = this.streams3.pop(); if (s) this.sw(s.addr, s.len); }
            else if (n === 1) this.screenOn = true;
            else if (n === -1) this.screenOn = false;
            return;
          }
          case 20: return;
          case 21: if (this.io.beep && (a === 1 || a === 2)) this.io.beep(); return;
          case 22: this.waiting = { type: "char", store: m[this.pc++] }; this.io.requestChar(); return;
          case 23: {
            const form = o.length > 3 ? o[3] : 0x82, len = form & 0x7f, words = form & 0x80;
            let r = 0;
            for (let i = 0, ad = b; i < o[2]; i++, ad += len) {
              if ((words ? this.w(ad) : m[ad]) === a) { r = ad; break; }
            }
            this.st(r); this.branch(r !== 0); return;
          }
          case 24: this.st((~a) & 0xffff); return;
          case 25: case 26: this.call(a, o.slice(1), -1); return;
          case 27: this.tokenise(a, b, o[2] || 0, o[3] || 0); return;
          case 28: {
            const chars = [];
            for (let i = 0; i < b; i++) chars.push(this.zsciiChar(m[a + o[2] + i]));
            const enc = this.encodeWord(chars.join(""));
            enc.forEach((wv, i) => this.sw(o[3] + 2 * i, wv));
            return;
          }
          case 29: {
            const size = s16(o[2]);
            if (b === 0) { for (let i = 0; i < Math.abs(size); i++) m[a + i] = 0; }
            else if (size < 0 || b < a) { for (let i = 0; i < Math.abs(size); i++) m[b + i] = m[a + i]; }
            else { for (let i = size - 1; i >= 0; i--) m[b + i] = m[a + i]; }
            return;
          }
          case 30: {
            const width = b, height = o[2] || 1, skip = o[3] || 0;
            for (let y = 0; y < height; y++) {
              let s = "";
              for (let x = 0; x < width; x++) s += this.zsciiChar(m[a + y * (width + skip) + x]);
              this.print(s + (y < height - 1 ? "\n" : ""));
            }
            return;
          }
          case 31: this.branch(a <= this.frame.args); return;
        }
      } else if (kind === 4) {
        switch (num) {
          case 0: { const ok = this.doSave(); this.st(ok ? 1 : 0); return; }
          case 1: { const r = this.doRestore(); if (!r) this.st(0); return; }
          case 2: this.st(s16(b) >= 0 ? a << b : a >>> -s16(b)); return;
          case 3: this.st(s16(b) >= 0 ? a << b : s16(a) >> -s16(b)); return;
          case 4: this.st(a === 1 || a === 4 ? 1 : 0); return;
          case 9: { const st = m[this.pc]; this.undo = this.snapshot(); this.pc++; this.setVar(st, 1); return; }
          case 10: {
            if (!this.undo) { this.st(0); return; }
            this.load(this.undo); this.undo = null;
            const st = m[this.pc++]; this.setVar(st, 2); return;
          }
          case 11: this.print(String.fromCharCode(a)); return;
          case 12: this.st(3); return;
        }
      }
      throw new Error("Unknown opcode " + op.toString(16) + " (" + ["0OP", "1OP", "2OP", "VAR", "EXT"][kind] + ":" + num + ") at " + (this.pc - 1).toString(16));
    }

    doSave() {
      // the snapshot's pc points at the store/branch byte of the save instruction
      const s = this.snapshot();
      return this.io.save(this.saveKey(), this.packState(s));
    }
    doRestore() {
      const json = this.io.restore(this.saveKey());
      if (!json) return false;
      let s;
      try { s = this.unpackState(json); } catch (e) { return false; }
      this.load(s);
      if (this.version <= 3) this.branch(true);
      else this.st(2);
      return true;
    }

    showStatus() {
      if (this.version > 3 || !this.io.statusV3) return;
      const loc = this.getVar(16), name = loc ? this.objName(loc) : "";
      const isTime = this.version === 3 && (this.mem[1] & 2);
      this.io.statusV3(name, s16(this.getVar(17)), s16(this.getVar(18)), !!isTime);
    }
  }

  root.ZMachine = ZMachine;
  if (typeof module !== "undefined") module.exports = ZMachine;
})(typeof window !== "undefined" ? window : globalThis);
