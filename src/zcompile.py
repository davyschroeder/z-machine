"""zcompile.py - a small compiler from a Python-embedded language to Z-machine version 5 story files.

The game source (see blue_lantern.py) builds a Story: globals, arrays, objects with properties and
attributes, routines whose bodies are nested tuples (statements and expressions), and the compiler
turns it into a standard .z5 file that any Z-machine interpreter can play.

Expressions
  123                 constant              'name'            local or global variable
  W('word')           dictionary address    R('routine')      packed routine address
  S('text')           packed string addr    A('array')        array address
  ('+', a, b) - * / % & |                   ('call', 'r', args...)   ('callv', addr, args...)
  ('prop', o, p) ('propaddr', o, p) ('proplen', a) ('parent', o) ('child', o) ('sibling', o)
  ('lw', arr, i) ('lb', arr, i) ('random', n) ('bnot', x) ('?', cond)
  ('aread', tb, pb) ('save',) ('restore',) ('save_undo',) ('restore_undo',)
Conditions
  ('==', a, b[, c, d]) != < > <= >=  ('has', o, attr) ('hasnt', o, attr) ('in', o, p) ('notin', o, p)
  ('not', c) ('and', c...) ('or', c...)  any expression (true when non-zero)
Statements
  'text' (print)  ('pr', 'text') print+newline+return true   ('set', v, e) ('inc', v) ('dec', v)
  ('if', c, [then], [else]) ('while', c, [body]) ('for', v, a, b, [body]) ('break',)
  ('switch', e, [((vals...), [body]), ...], [default])
  ('ret', e) ('rtrue',) ('rfalse',) ('do', e) ('pnum', e) ('pobj', e) ('pchar', e) ('ppaddr', e) ('nl',)
  ('move', o, d) ('remove', o) ('give', o, attr) ('ungive', o, attr) ('putprop', o, p, v)
  ('sw', arr, i, v) ('sb', arr, i, v) ('style', n) ('split', n) ('window', n) ('cursor', l, c)
  ('erase', n) ('tokenise', tb, pb) ('quit',) ('restart',) ('buffer', n)
"""

import struct

# ---------------------------------------------------------------- text encoding

A0 = 'abcdefghijklmnopqrstuvwxyz'
A1 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
A2 = '0123456789.,!?_#\'"/\\-:()'          # Z-characters 8..31 of alphabet 2
UNI = 'äöüÄÖÜß»«ëïÿËÏáéíóúýÁÉÍÓÚÝàèìòùÀÈÌÒÙâêîôûÂÊÎÔÛåÅøØãñõÃÑÕæÆçÇþðÞÐ£œŒ¡¿'  # ZSCII 155..


def zscii(ch):
    if ch == '\n':
        return 13
    o = ord(ch)
    if 32 <= o <= 126:
        return o
    if ch in UNI:
        return 155 + UNI.index(ch)
    raise ValueError('cannot encode character %r' % ch)


def zchars(s):
    out = []
    for ch in s:
        if ch == ' ':
            out.append(0)
        elif ch in A0:
            out.append(A0.index(ch) + 6)
        elif ch in A1:
            out += [4, A1.index(ch) + 6]
        elif ch == '\n':
            out += [5, 7]
        elif ch in A2:
            out += [5, A2.index(ch) + 8]
        else:
            z = zscii(ch)
            out += [5, 6, z >> 5, z & 31]
    return out


def pack_zchars(zc):
    zc = list(zc)
    while len(zc) % 3 or not zc:
        zc.append(5)
    out = bytearray()
    for i in range(0, len(zc), 3):
        w = (zc[i] << 10) | (zc[i + 1] << 5) | zc[i + 2]
        if i + 3 >= len(zc):
            w |= 0x8000
        out += struct.pack('>H', w)
    return out


def encode_string(s):
    return pack_zchars(zchars(s))


def encode_dict_word(w):
    zc = zchars(w.lower())[:9]
    while len(zc) < 9:
        zc.append(5)
    return pack_zchars(zc)


# ---------------------------------------------------------------- symbols


class Sym:
    def __init__(self, v):
        self.v = v

    def __repr__(self):
        return '%s(%r)' % (type(self).__name__, self.v)

    def __eq__(self, o):
        return type(self) is type(o) and self.v == o.v

    def __hash__(self):
        return hash((type(self).__name__, self.v))


class W(Sym):
    pass


class R(Sym):
    pass


class S(Sym):
    pass


class A(Sym):
    pass


# ---------------------------------------------------------------- opcodes

OPS = {
    # name: (kind, number, store, branch)
    'je': ('2OP', 1, 0, 1), 'jl': ('2OP', 2, 0, 1), 'jg': ('2OP', 3, 0, 1), 'jin': ('2OP', 6, 0, 1),
    'test': ('2OP', 7, 0, 1), 'or': ('2OP', 8, 1, 0), 'and': ('2OP', 9, 1, 0),
    'test_attr': ('2OP', 10, 0, 1), 'set_attr': ('2OP', 11, 0, 0), 'clear_attr': ('2OP', 12, 0, 0),
    'store': ('2OP', 13, 0, 0), 'insert_obj': ('2OP', 14, 0, 0), 'loadw': ('2OP', 15, 1, 0),
    'loadb': ('2OP', 16, 1, 0), 'get_prop': ('2OP', 17, 1, 0), 'get_prop_addr': ('2OP', 18, 1, 0),
    'add': ('2OP', 20, 1, 0), 'sub': ('2OP', 21, 1, 0), 'mul': ('2OP', 22, 1, 0),
    'div': ('2OP', 23, 1, 0), 'mod': ('2OP', 24, 1, 0),
    'jz': ('1OP', 0, 0, 1), 'get_sibling': ('1OP', 1, 1, 1), 'get_child': ('1OP', 2, 1, 1),
    'get_parent': ('1OP', 3, 1, 0), 'get_prop_len': ('1OP', 4, 1, 0), 'inc': ('1OP', 5, 0, 0),
    'dec': ('1OP', 6, 0, 0), 'print_addr': ('1OP', 7, 0, 0), 'remove_obj': ('1OP', 9, 0, 0),
    'print_obj': ('1OP', 10, 0, 0), 'ret': ('1OP', 11, 0, 0), 'jump': ('1OP', 12, 0, 0),
    'print_paddr': ('1OP', 13, 0, 0),
    'rtrue': ('0OP', 0, 0, 0), 'rfalse': ('0OP', 1, 0, 0), 'restart': ('0OP', 7, 0, 0),
    'ret_popped': ('0OP', 8, 0, 0), 'quit': ('0OP', 10, 0, 0), 'new_line': ('0OP', 11, 0, 0),
    'call_vs': ('VAR', 0, 1, 0), 'storew': ('VAR', 1, 0, 0), 'storeb': ('VAR', 2, 0, 0),
    'put_prop': ('VAR', 3, 0, 0), 'aread': ('VAR', 4, 1, 0), 'print_char': ('VAR', 5, 0, 0),
    'print_num': ('VAR', 6, 0, 0), 'random': ('VAR', 7, 1, 0), 'push': ('VAR', 8, 0, 0),
    'pull': ('VAR', 9, 0, 0), 'split_window': ('VAR', 10, 0, 0), 'set_window': ('VAR', 11, 0, 0),
    'call_vs2': ('VAR', 12, 1, 0), 'erase_window': ('VAR', 13, 0, 0), 'set_cursor': ('VAR', 15, 0, 0),
    'set_text_style': ('VAR', 17, 0, 0), 'buffer_mode': ('VAR', 18, 0, 0), 'not': ('VAR', 24, 1, 0),
    'call_vn': ('VAR', 25, 0, 0), 'call_vn2': ('VAR', 26, 0, 0), 'tokenise': ('VAR', 27, 0, 0),
    'save': ('EXT', 0, 1, 0), 'restore': ('EXT', 1, 1, 0),
    'save_undo': ('EXT', 9, 1, 0), 'restore_undo': ('EXT', 10, 1, 0),
}

BINOPS = {'+': 'add', '-': 'sub', '*': 'mul', '/': 'div', '%': 'mod', '&': 'and', '|': 'or'}


def optype(op):
    k, v = op
    if k == 'c':
        return 1 if 0 <= v <= 255 else 0
    if k == 'v':
        return 2
    return 0  # symbol: large


class Routine:
    def __init__(self, story, name, args, locs, body):
        self.story, self.name = story, name
        self.vars = {n: i + 1 for i, n in enumerate(list(args) + list(locs))}
        if len(self.vars) > 15:
            raise ValueError('%s: too many locals' % name)
        self.b = bytearray([len(self.vars)])
        self.labels, self.brfix, self.symfix = {}, [], []
        self.nlab = 0
        self.loops = []
        self.block(body)
        # every routine ends with "return false" in case control falls off the end
        self.emit('rfalse', [])
        for pos, lab, kind in self.brfix:
            t = self.labels[lab]
            if kind == 'jump':
                off = t - (pos + 2) + 2
                self.b[pos:pos + 2] = struct.pack('>h', off)
            else:
                off = t - (pos + 2) + 2
                if not -8192 <= off <= 8191:
                    raise ValueError('%s: branch too far' % name)
                v = (off & 0x3FFF) | (0x8000 if kind else 0)
                self.b[pos:pos + 2] = struct.pack('>H', v)

    # ------------------------------------------------ low level
    def label(self):
        self.nlab += 1
        return self.nlab

    def place(self, lab):
        self.labels[lab] = len(self.b)

    def emit(self, name, ops, store=None, branch=None):
        kind, num, hs, hb = OPS[name]
        b = self.b
        if kind == '2OP' and len(ops) == 2 and optype(ops[0]) and optype(ops[1]):
            b.append(num | (0x40 if optype(ops[0]) == 2 else 0) | (0x20 if optype(ops[1]) == 2 else 0))
            for op in ops:
                b.append(op[1])
        else:
            if kind == '2OP':
                b.append(0xC0 | num)
            elif kind == '1OP':
                b.append(0x80 | (optype(ops[0]) << 4) | num)
            elif kind == '0OP':
                b.append(0xB0 | num)
            elif kind == 'VAR':
                b.append(0xE0 | num)
            else:
                b += bytes([0xBE, num])
            if kind in ('2OP', 'VAR', 'EXT'):
                n = 8 if name in ('call_vs2', 'call_vn2') else 4
                if len(ops) > n:
                    raise ValueError('too many operands for ' + name)
                types = [optype(o) for o in ops] + [3] * (n - len(ops))
                for i in range(0, n, 4):
                    b.append((types[i] << 6) | (types[i + 1] << 4) | (types[i + 2] << 2) | types[i + 3])
            for op in ops:
                k, v = op
                if k == 'v':
                    b.append(v)
                elif k == 'c':
                    if optype(op) == 1:
                        b.append(v)
                    else:
                        b += struct.pack('>H', v & 0xFFFF)
                else:
                    self.symfix.append((len(b), v))
                    b += b'\0\0'
        if hs:
            b.append(0 if store is None else store)
        if hb:
            lab, on_true = branch
            self.brfix.append((len(b), lab, on_true))
            b += b'\0\0'

    def jump(self, lab):
        self.b.append(0x8C)
        self.brfix.append((len(self.b), lab, 'jump'))
        self.b += b'\0\0'

    def inline_print(self, text, ret=False):
        self.b.append(0xB3 if ret else 0xB2)
        self.b += encode_string(text)

    # ------------------------------------------------ variables / operands
    def varnum(self, name):
        if name in self.vars:
            return self.vars[name]
        if name in self.story.gvars:
            return self.story.gvars[name]
        raise ValueError('%s: unknown variable %s' % (self.name, name))

    def simple(self, e):
        if isinstance(e, bool):
            return ('c', int(e))
        if isinstance(e, int):
            return ('c', e & 0xFFFF)
        if isinstance(e, str):
            if e in self.story.consts:
                return ('c', self.story.consts[e] & 0xFFFF)
            return ('v', self.varnum(e))
        if isinstance(e, Obj):
            return ('c', e.num)
        if isinstance(e, Sym):
            if isinstance(e, S):
                self.story.strings.setdefault(e.v, len(self.story.strings))
            if isinstance(e, W):
                self.story.words.add(e.v.lower())
            return ('s', e)
        raise ValueError('bad operand %r' % (e,))

    @staticmethod
    def is_complex(e):
        return isinstance(e, tuple)

    def operands(self, es):
        for e in reversed(es):
            if self.is_complex(e):
                self.expr(e, 0)
        return [('v', 0) if self.is_complex(e) else self.simple(e) for e in es]

    # ------------------------------------------------ expressions
    def expr(self, e, target):
        if not self.is_complex(e):
            op = self.simple(e)
            if target == 0:
                self.emit('push', [op])
            else:
                self.emit('store', [('c', target), op])
            return
        h = e[0]
        if h in BINOPS:
            self.emit(BINOPS[h], self.operands(list(e[1:3])), store=target)
        elif h in ('call', 'callv'):
            f = R(e[1]) if h == 'call' else e[1]
            ops = self.operands([f] + list(e[2:]))
            self.emit('call_vs' if len(ops) <= 4 else 'call_vs2', ops, store=target)
        elif h == 'prop':
            self.emit('get_prop', self.operands(list(e[1:3])), store=target)
        elif h == 'propaddr':
            self.emit('get_prop_addr', self.operands(list(e[1:3])), store=target)
        elif h == 'proplen':
            self.emit('get_prop_len', self.operands([e[1]]), store=target)
        elif h == 'parent':
            self.emit('get_parent', self.operands([e[1]]), store=target)
        elif h in ('child', 'sibling'):
            lab = self.label()
            self.emit('get_' + h, self.operands([e[1]]), store=target, branch=(lab, True))
            self.place(lab)
        elif h == 'lw':
            self.emit('loadw', self.operands(list(e[1:3])), store=target)
        elif h == 'lb':
            self.emit('loadb', self.operands(list(e[1:3])), store=target)
        elif h == 'random':
            self.emit('random', self.operands([e[1]]), store=target)
        elif h == 'bnot':
            self.emit('not', self.operands([e[1]]), store=target)
        elif h == 'aread':
            self.emit('aread', self.operands(list(e[1:3])), store=target)
        elif h in ('save', 'restore', 'save_undo', 'restore_undo'):
            self.emit(h, [], store=target)
        elif h == '?':
            lf, le = self.label(), self.label()
            self.cond(e[1], lf, False)
            self.expr(1, target)
            self.jump(le)
            self.place(lf)
            self.expr(0, target)
            self.place(le)
        else:
            raise ValueError('%s: unknown expression %r' % (self.name, e))

    # ------------------------------------------------ conditions
    def cond(self, c, lab, on_true):
        """Branch to lab when c evaluates to on_true."""
        if isinstance(c, tuple):
            h = c[0]
            if h == 'not':
                return self.cond(c[1], lab, not on_true)
            if h in ('and', 'or'):
                parts = c[1:]
                short = (h == 'and') != on_true  # and/false or or/true: any part decides
                if short:
                    for p in parts:
                        self.cond(p, lab, on_true)
                else:
                    skip = self.label()
                    for p in parts[:-1]:
                        self.cond(p, skip, not on_true)
                    self.cond(parts[-1], lab, on_true)
                    self.place(skip)
                return
            if h in ('==', '!='):
                vals = list(c[2:])
                if len(vals) > 3:  # je takes at most 3 values to compare with
                    sub = [('==', c[1], *vals[i:i + 3]) for i in range(0, len(vals), 3)]
                    return self.cond(('or', *sub) if h == '==' else ('not', ('or', *sub)), lab, on_true)
                self.emit('je', self.operands([c[1]] + vals), branch=(lab, on_true == (h == '==')))
                return
            if h in ('<', '>', '<=', '>='):
                op = 'jl' if h in ('<', '>=') else 'jg'
                self.emit(op, self.operands(list(c[1:3])), branch=(lab, on_true == (h in ('<', '>'))))
                return
            if h in ('has', 'hasnt'):
                self.emit('test_attr', self.operands(list(c[1:3])), branch=(lab, on_true == (h == 'has')))
                return
            if h in ('in', 'notin'):
                self.emit('jin', self.operands(list(c[1:3])), branch=(lab, on_true == (h == 'in')))
                return
        self.emit('jz', self.operands([c]), branch=(lab, not on_true))

    # ------------------------------------------------ statements
    def block(self, stmts):
        for s in stmts:
            self.stmt(s)

    def stmt(self, s):
        if isinstance(s, str):
            return self.inline_print(s)
        if isinstance(s, list):
            return self.block(s)
        h = s[0]
        if h == 'pr':
            self.inline_print(s[1], ret=True)
        elif h == 'set':
            self.expr(s[2], self.varnum(s[1]))
        elif h in ('inc', 'dec'):
            self.emit(h, [('c', self.varnum(s[1]))])
        elif h == 'if':
            lelse, lend = self.label(), self.label()
            self.cond(s[1], lelse, False)
            self.block(s[2])
            if len(s) > 3 and s[3]:
                self.jump(lend)
                self.place(lelse)
                self.block(s[3])
                self.place(lend)
            else:
                self.place(lelse)
        elif h == 'while':
            ltop, lend = self.label(), self.label()
            self.place(ltop)
            self.cond(s[1], lend, False)
            self.loops.append(lend)
            self.block(s[2])
            self.loops.pop()
            self.jump(ltop)
            self.place(lend)
        elif h == 'for':
            v, a, b, body = s[1:]
            self.stmt(('set', v, a))
            ltop, lend = self.label(), self.label()
            self.place(ltop)
            self.cond(('>', v, b), lend, True)
            self.loops.append(lend)
            self.block(body)
            self.loops.pop()
            self.stmt(('inc', v))
            self.jump(ltop)
            self.place(lend)
        elif h == 'break':
            self.jump(self.loops[-1])
        elif h == 'switch':
            e, cases = s[1], s[2]
            default = s[3] if len(s) > 3 else []
            lend = self.label()
            for vals, body in cases:
                if not isinstance(vals, tuple):
                    vals = (vals,)
                lnext = self.label()
                self.cond(('==', e, *vals), lnext, False)
                self.block(body)
                self.jump(lend)
                self.place(lnext)
            self.block(default)
            self.place(lend)
        elif h == 'ret':
            v = s[1]
            if v is True or v == 1 and isinstance(v, int):
                self.emit('rtrue', [])
            elif v is False or v == 0 and isinstance(v, int):
                self.emit('rfalse', [])
            else:
                self.emit('ret', self.operands([v]))
        elif h == 'rtrue':
            self.emit('rtrue', [])
        elif h == 'rfalse':
            self.emit('rfalse', [])
        elif h == 'do':
            e = s[1]
            if isinstance(e, tuple) and e[0] in ('call', 'callv'):
                f = R(e[1]) if e[0] == 'call' else e[1]
                ops = self.operands([f] + list(e[2:]))
                self.emit('call_vn' if len(ops) <= 4 else 'call_vn2', ops)
            else:
                self.expr(e, 0)
                self.emit('pull', [('c', 16)])  # discard into a scratch global (g0)
        elif h == 'pnum':
            self.emit('print_num', self.operands([s[1]]))
        elif h == 'pobj':
            self.emit('print_obj', self.operands([s[1]]))
        elif h == 'pchar':
            self.emit('print_char', self.operands([s[1]]))
        elif h == 'ppaddr':
            self.emit('print_paddr', self.operands([s[1]]))
        elif h == 'paddr':
            self.emit('print_addr', self.operands([s[1]]))
        elif h == 'nl':
            self.emit('new_line', [])
        elif h == 'move':
            self.emit('insert_obj', self.operands(list(s[1:3])))
        elif h == 'remove':
            self.emit('remove_obj', self.operands([s[1]]))
        elif h == 'give':
            self.emit('set_attr', self.operands(list(s[1:3])))
        elif h == 'ungive':
            self.emit('clear_attr', self.operands(list(s[1:3])))
        elif h == 'putprop':
            self.emit('put_prop', self.operands(list(s[1:4])))
        elif h == 'sw':
            self.emit('storew', self.operands(list(s[1:4])))
        elif h == 'sb':
            self.emit('storeb', self.operands(list(s[1:4])))
        elif h == 'style':
            self.emit('set_text_style', self.operands([s[1]]))
        elif h == 'split':
            self.emit('split_window', self.operands([s[1]]))
        elif h == 'window':
            self.emit('set_window', self.operands([s[1]]))
        elif h == 'cursor':
            self.emit('set_cursor', self.operands(list(s[1:3])))
        elif h == 'erase':
            self.emit('erase_window', self.operands([s[1]]))
        elif h == 'buffer':
            self.emit('buffer_mode', self.operands([s[1]]))
        elif h == 'tokenise':
            self.emit('tokenise', self.operands(list(s[1:3])))
        elif h == 'quit':
            self.emit('quit', [])
        elif h == 'restart':
            self.emit('restart', [])
        else:
            raise ValueError('%s: unknown statement %r' % (self.name, s))


# ---------------------------------------------------------------- story


class Obj:
    def __init__(self, num, name, parent, attrs, props):
        self.num, self.name, self.parent, self.attrs, self.props = num, name, parent, attrs, props


class Story:
    def __init__(self, serial='261108', release=1):
        self.serial, self.release = serial, release
        self.gvars, self.ginit = {}, {}
        self.consts = {}
        self.arrays = []  # (name, size or bytes)
        self.objs = []
        self.routines = {}
        self.order = []
        self.strings = {}
        self.words = set()
        self.word_data = {}  # word -> bytes of data (3 bytes)
        self.glob('_scratch')

    def glob(self, name, init=0):
        if name not in self.gvars:
            self.gvars[name] = 16 + len(self.gvars)
            if len(self.gvars) > 240:
                raise ValueError('too many globals')
        self.ginit[name] = init
        return name

    def const(self, name, v):
        self.consts[name] = v
        return name

    def array(self, name, data):
        self.arrays.append((name, bytes(data) if not isinstance(data, int) else bytes(data)))
        return A(name)

    def obj(self, name, parent=0, attrs=(), props=None):
        if isinstance(parent, Obj):
            parent = parent.num
        o = Obj(len(self.objs) + 1, name, parent, list(attrs), dict(props or {}))
        self.objs.append(o)
        return o

    def word(self, w, b0=0, b1=0, b2=0):
        w = w.lower()
        self.words.add(w)
        old = self.word_data.get(w, [0, 0, 0])
        new = [b0 or old[0], b1 or old[1], b2 or old[2]]
        self.word_data[w] = new

    def routine(self, name, args=(), locs=(), body=()):
        self.order.append((name, args, locs, body))

    # ------------------------------------------------ linking
    def compile(self):
        comp = {}
        for name, args, locs, body in self.order:
            comp[name] = Routine(self, name, args, locs, body)
        for o in self.objs:
            for v in o.props.values():
                for x in (v if isinstance(v, list) else [v]):
                    if isinstance(x, W):
                        self.words.add(x.v.lower())
                    if isinstance(x, S):
                        self.strings.setdefault(x.v, len(self.strings))

        mem = bytearray(64)
        # abbreviation table: 96 entries all pointing at one empty string
        abbr = len(mem)
        mem += b'\0' * 192
        empty = len(mem)
        mem += pack_zchars([])
        for i in range(96):
            mem[abbr + 2 * i:abbr + 2 * i + 2] = struct.pack('>H', empty // 2)

        # objects
        objtab = len(mem)
        mem += b'\0' * (63 * 2)
        entries = len(mem)
        mem += b'\0' * (14 * len(self.objs))
        prop_fix = []  # (address, symbol)
        children = {}
        for o in self.objs:
            children.setdefault(o.parent, []).append(o.num)
        for o in self.objs:
            e = entries + 14 * (o.num - 1)
            bits = 0
            for a in o.attrs:
                a = self.consts.get(a, a)
                bits |= 1 << (47 - a)
            mem[e:e + 6] = bits.to_bytes(6, 'big')
            sibs = children.get(o.parent, [])
            i = sibs.index(o.num)
            sib = sibs[i + 1] if i + 1 < len(sibs) else 0
            kids = children.get(o.num, [])
            mem[e + 6:e + 12] = struct.pack('>HHH', o.parent, sib, kids[0] if kids else 0)
            mem[e + 12:e + 14] = struct.pack('>H', len(mem))
            nm = encode_string(o.name)
            mem.append(len(nm) // 2)
            mem += nm
            for p in sorted(o.props, key=lambda k: -self.consts.get(k, k)):
                pn = self.consts.get(p, p)
                vals = o.props[p]
                vals = vals if isinstance(vals, list) else [vals]
                size = 2 * len(vals)
                if size == 2:
                    mem.append(0x40 | pn)
                else:
                    mem.append(0x80 | pn)
                    mem.append(0x80 | (size & 63))
                for v in vals:
                    if isinstance(v, Obj):
                        v = v.num
                    if isinstance(v, Sym):
                        prop_fix.append((len(mem), v))
                        mem += b'\0\0'
                    else:
                        if isinstance(v, str):
                            v = self.consts[v]
                        mem += struct.pack('>H', v & 0xFFFF)
            mem.append(0)
        if len(mem) % 2:
            mem.append(0)

        globs = len(mem)
        mem += b'\0' * 480
        for n, v in self.ginit.items():
            if isinstance(v, Sym):
                prop_fix.append((globs + 2 * (self.gvars[n] - 16), v))
            else:
                mem[globs + 2 * (self.gvars[n] - 16):globs + 2 * (self.gvars[n] - 16) + 2] = struct.pack('>H', v & 0xFFFF)

        arr = {}
        for n, data in self.arrays:
            if len(mem) % 2:
                mem.append(0)
            arr[n] = len(mem)
            mem += data
        while len(mem) % 2:
            mem.append(0)
        static = len(mem)

        # dictionary
        dictionary = len(mem)
        seps = b'.,"'
        mem.append(len(seps))
        mem += seps
        mem.append(9)
        words = sorted(self.words | set(self.word_data), key=encode_dict_word)
        enc = {}
        for w in words:  # words truncated to the same 9 Z-characters share one entry
            enc.setdefault(bytes(encode_dict_word(w)), []).append(w)
        mem += struct.pack('>H', len(enc))
        waddr = {}
        for key in sorted(enc):
            a = len(mem)
            data = [0, 0, 0]
            for w in enc[key]:
                waddr[w] = a
                d = self.word_data.get(w, [0, 0, 0])
                data = [x or y for x, y in zip(data, d)]
            mem += key + bytes(data)
        while len(mem) % 4:
            mem.append(0)
        high = len(mem)

        # start stub: call_vn Main ; quit
        start = len(mem)
        stub_fix = len(mem) + 2
        mem += bytes([0xF9, 0x3F, 0, 0, 0xBA])
        raddr = {}
        for name, args, locs, body in self.order:
            while len(mem) % 4:
                mem.append(0)
            raddr[name] = len(mem)
            r = comp[name]
            base = len(mem)
            mem += r.b
            for pos, sym in r.symfix:
                prop_fix.append((base + pos, sym))
        saddr = {}
        for s, _ in sorted(self.strings.items(), key=lambda kv: kv[1]):
            while len(mem) % 4:
                mem.append(0)
            saddr[s] = len(mem)
            mem += encode_string(s)
        while len(mem) % 8:
            mem.append(0)
        prop_fix.append((stub_fix, R('Main')))

        for pos, sym in prop_fix:
            if isinstance(sym, R):
                v = raddr[sym.v] // 4
            elif isinstance(sym, S):
                v = saddr[sym.v] // 4
            elif isinstance(sym, W):
                v = waddr[sym.v.lower()]
            elif isinstance(sym, A):
                v = arr[sym.v]
            mem[pos:pos + 2] = struct.pack('>H', v)

        if len(mem) > 256 * 1024:
            raise ValueError('story too large')
        if static > 0xFFFF:
            raise ValueError('dynamic memory too large')
        h = mem
        h[0] = 5
        struct.pack_into('>H', h, 2, self.release)
        struct.pack_into('>H', h, 4, high)
        struct.pack_into('>H', h, 6, start)
        struct.pack_into('>H', h, 8, dictionary)
        struct.pack_into('>H', h, 0xA, objtab)
        struct.pack_into('>H', h, 0xC, globs)
        struct.pack_into('>H', h, 0xE, static)
        h[0x12:0x18] = self.serial.encode()
        struct.pack_into('>H', h, 0x18, abbr)
        struct.pack_into('>H', h, 0x1A, len(mem) // 4)
        struct.pack_into('>H', h, 0x1C, sum(mem[0x40:]) & 0xFFFF)
        self.addr = {'routines': raddr, 'words': waddr, 'arrays': arr, 'globals': globs}
        return bytes(mem)
