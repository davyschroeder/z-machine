"""lib.py - a small adventure library (parser, scope, default verbs, status line) for zcompile.py.

A game imports this, creates its rooms and objects with room()/thing(), adds before-routines with
before(), and calls finish() with its own Main-loop hooks.
"""
from zcompile import Story, W, R, S, A, Obj

st = Story(serial='261108', release=1)

# ---------------------------------------------------------------- attributes and properties
ATTRS = ['LIGHT', 'SCENERY', 'STATIC', 'CONTAINER', 'OPENABLE', 'OPEN', 'LOCKED', 'WORN', 'CLOTHING',
         'SWITCHABLE', 'ON', 'PERSON', 'VISITED', 'MOVED', 'DARK', 'PROPER', 'SUPPORTER', 'TRANSPARENT',
         'FEMALE', 'ROOM', 'CONCEALED']
for i, a in enumerate(ATTRS):
    st.const(a, i)
PROPS = ['NAME', 'DESC', 'BEFORE', 'N_TO', 'S_TO', 'E_TO', 'W_TO', 'NE_TO', 'NW_TO', 'SE_TO', 'SW_TO',
         'U_TO', 'D_TO', 'IN_TO', 'OUT_TO', 'ARTICLE', 'INITIAL', 'DESCRIBE', 'WITH_KEY']
for i, p in enumerate(PROPS):
    st.const(p, i + 1)

# ---------------------------------------------------------------- actions, prepositions, directions
ACTIONS = ['LOOK', 'EXAMINE', 'TAKE', 'DROP', 'INV', 'GO', 'OPEN', 'CLOSE', 'UNLOCK', 'LOCK', 'GIVE', 'SHOW',
           'TALK', 'ASK', 'SHOOT', 'ATTACK', 'CUT', 'FREE', 'SWITCHON', 'SWITCHOFF', 'WEAR', 'REMOVE', 'DRINK',
           'LOAD', 'CALL', 'WAKE', 'RING', 'PUSH', 'PULL', 'SIT', 'READ', 'LISTEN', 'SMELL', 'WAIT', 'SCORE',
           'HELP', 'ABOUT', 'SAVE', 'RESTORE', 'UNDO', 'RESTART', 'QUIT', 'AGAIN', 'SEARCH', 'INSERT', 'CLIMB',
           'ENTER', 'PLAY', 'KISS', 'JUMP', 'SLEEP', 'XYZZY', 'EAT', 'TURN', 'PICK', 'PUT', 'HIDE', 'SING',
           'THINK', 'KNOCK', 'USE', 'HINT', 'PET', 'SMOKE', 'YES', 'NO']
for i, a in enumerate(ACTIONS):
    st.const(a, i + 1)
META = ['SCORE', 'HELP', 'ABOUT', 'SAVE', 'RESTORE', 'UNDO', 'RESTART', 'QUIT', 'HINT']
NEEDNOUN = ['EXAMINE', 'TAKE', 'DROP', 'OPEN', 'CLOSE', 'UNLOCK', 'LOCK', 'GIVE', 'SHOW', 'SHOOT', 'ATTACK', 'CUT',
            'FREE', 'SWITCHON', 'SWITCHOFF', 'WEAR', 'REMOVE', 'DRINK', 'LOAD', 'PUSH', 'PULL', 'READ', 'INSERT',
            'ENTER', 'PLAY', 'EAT', 'PICK', 'PUT', 'USE', 'PET', 'TALK', 'WAKE', 'KISS']
PREPS = ['AT', 'IN', 'ON', 'WITH', 'TO', 'ABOUT', 'UNDER', 'UP', 'DOWN', 'OFF', 'FROM', 'OUT', 'FOR', 'THROUGH']
for i, p in enumerate(PREPS):
    st.const('P_' + p, i + 1)
st.const('NOISE', 99)
DIRS = ['N', 'S', 'E', 'W', 'NE', 'NW', 'SE', 'SW', 'U', 'D', 'IN', 'OUT']
for i, d in enumerate(DIRS):
    st.const('D_' + d, i + 1)

VERBS = {
    'LOOK': 'look l', 'EXAMINE': 'examine x inspect check describe study observe watch',
    'READ': 'read', 'TAKE': 'take get grab steal acquire collect', 'PICK': 'pick',
    'DROP': 'drop discard', 'PUT': 'put place insert stick slip', 'INV': 'inventory i inv',
    'GO': 'go walk run head travel', 'OPEN': 'open', 'CLOSE': 'close shut', 'UNLOCK': 'unlock',
    'LOCK': 'lock', 'GIVE': 'give offer hand pay bribe', 'SHOW': 'show flash present',
    'TALK': 'talk speak chat greet hello hi', 'ASK': 'ask question interrogate query tell',
    'SHOOT': 'shoot fire', 'ATTACK': 'attack hit punch kill fight strike kick slug smack slap murder',
    'CUT': 'cut slice saw slash', 'FREE': 'untie free release rescue', 'TURN': 'turn switch flick',
    'SWITCHON': 'light', 'SWITCHOFF': 'extinguish', 'WEAR': 'wear don', 'REMOVE': 'remove doff',
    'DRINK': 'drink sip swig', 'EAT': 'eat', 'LOAD': 'load reload', 'CALL': 'call phone dial telephone',
    'WAKE': 'wake rouse awaken', 'RING': 'ring', 'PUSH': 'push press shove move', 'PULL': 'pull yank tug',
    'SIT': 'sit', 'CLIMB': 'climb scale', 'ENTER': 'enter', 'PLAY': 'play', 'KISS': 'kiss hug',
    'JUMP': 'jump leap', 'SLEEP': 'sleep nap', 'XYZZY': 'xyzzy plugh', 'LISTEN': 'listen hear',
    'SMELL': 'smell sniff', 'WAIT': 'wait z', 'SCORE': 'score', 'HELP': 'help instructions',
    'HINT': 'hint hints clue', 'ABOUT': 'about credits info', 'SAVE': 'save', 'RESTORE': 'restore',
    'UNDO': 'undo oops', 'RESTART': 'restart', 'QUIT': 'quit q', 'AGAIN': 'again g',
    'SEARCH': 'search frisk rummage', 'HIDE': 'hide', 'SING': 'sing whistle hum', 'THINK': 'think ponder',
    'KNOCK': 'knock', 'USE': 'use', 'PET': 'pet stroke pat', 'SMOKE': 'smoke', 'YES': 'yes y', 'NO': 'no',
}
for act, words in VERBS.items():
    for w in words.split():
        st.word(w, b0=st.consts[act])
for w in 'exit leave'.split():
    st.word(w, b0=st.consts['GO'], b2=st.consts['D_OUT'])
PREPW = {'AT': 'at', 'IN': 'in into inside', 'ON': 'on onto upon', 'WITH': 'with using', 'TO': 'to toward towards',
         'ABOUT': 'about regarding', 'UNDER': 'under beneath below underneath behind', 'UP': 'up', 'DOWN': 'down',
         'OFF': 'off', 'FROM': 'from', 'OUT': 'out', 'FOR': 'for', 'THROUGH': 'through'}
for p, words in PREPW.items():
    for w in words.split():
        st.word(w, b1=st.consts['P_' + p])
st.word('all')
st.word('everything')
for w in 'the a an my some his her its this that those these your of'.split():
    st.word(w, b1=99)
DIRW = {'N': 'north n', 'S': 'south s', 'E': 'east e', 'W': 'west w', 'NE': 'northeast ne', 'NW': 'northwest nw',
        'SE': 'southeast se', 'SW': 'southwest sw', 'U': 'up u upstairs', 'D': 'down d downstairs',
        'IN': 'in inside', 'OUT': 'out outside'}
for d, words in DIRW.items():
    for w in words.split():
        st.word(w, b2=st.consts['D_' + d])

# ---------------------------------------------------------------- globals and arrays
for g in ['location', 'action', 'noun', 'second', 'particle', 'prep2', 'dir', 'score', 'moves', 'deadflag',
          'nw', 'oldlen', 'lastword']:
    st.glob(g)
TEXT = st.array('text', bytes([120]) + bytes(121))
PARSE = st.array('parse', bytes([30]) + bytes(1 + 4 * 30))
OLD = st.array('oldtext', bytes(122))

# ---------------------------------------------------------------- helpers for writing games


def on(*acts):
    """('if', action is one of acts, body + return true) - use as on('TAKE')(stmts...)."""
    def body(*stmts):
        return ('if', ('==', 'action', *acts), list(stmts) + [('rtrue',)])
    return body


def fail(text):
    return [text + '\n', ('rfalse',)]


def call(name, *args):
    return ('do', ('call', name, *args))


def room(name, words='', desc=None, attrs=(), **props):
    p = {}
    if words:
        p['NAME'] = [W(w) for w in words.split()]
    if desc:
        p['DESC'] = S(desc)
    p.update(props)
    return st.obj(name, 0, ['ROOM', 'PROPER'] + list(attrs), p)


def thing(name, words, parent, desc=None, attrs=(), article=None, initial=None, **props):
    p = {'NAME': [W(w) for w in words.split()]}
    if desc:
        p['DESC'] = S(desc)
    if article:
        p['ARTICLE'] = S(article)
    if initial:
        p['INITIAL'] = S(initial)
    p.update(props)
    return st.obj(name, parent, attrs, p)


def before(obj, *body):
    name = 'B_%d' % obj.num
    st.routine(name, (), ('t',), list(body))
    obj.props['BEFORE'] = R(name)


def describe(obj, *body):
    name = 'D_%d' % obj.num
    st.routine(name, (), ('t',), list(body))
    obj.props['DESCRIBE'] = R(name)


def word(i):
    return ('lw', PARSE, ('+', 1, ('*', 2, i)))


# ---------------------------------------------------------------- library routines


def build_library(player, flashlight):
    NOBJ = len(st.objs)
    st.routine('Data', ('w', 'k'), (), [('if', ('==', 'w', 0), [('ret', 0)]), ('ret', ('lb', 'w', ('+', 6, 'k')))])
    st.routine('IsNoise', ('w',), (), [('ret', ('?', ('==', ('call', 'Data', 'w', 1), 99)))])
    st.routine('PrintWord', ('i',), ('p', 'n', 'j'), [
        ('set', 'p', ('lb', PARSE, ('+', 5, ('*', 4, 'i')))),
        ('set', 'n', ('lb', PARSE, ('+', 4, ('*', 4, 'i')))),
        ('for', 'j', 'p', ('-', ('+', 'p', 'n'), 1), [('pchar', ('lb', TEXT, 'j'))]),
    ])
    st.routine('HasWord', ('o', 'w'), ('a', 'n', 'k'), [
        ('set', 'a', ('propaddr', 'o', 'NAME')),
        ('if', ('==', 'a', 0), [('rfalse',)]),
        ('set', 'n', ('-', ('/', ('proplen', 'a'), 2), 1)),
        ('for', 'k', 0, 'n', [('if', ('==', ('lw', 'a', 'k'), 'w'), [('rtrue',)])]),
        ('rfalse',),
    ])
    st.routine('Near', ('o',), ('p', 'q'), [
        ('if', ('==', 'o', player), [('rtrue',)]),
        ('set', 'p', 'o'),
        ('while', 1, [
            ('set', 'q', ('parent', 'p')),
            ('if', ('==', 'q', 0), [('rfalse',)]),
            ('if', ('==', 'q', player, 'location'), [('rtrue',)]),
            ('if', ('and', ('has', 'q', 'CONTAINER'), ('hasnt', 'q', 'OPEN'), ('hasnt', 'q', 'TRANSPARENT')), [('rfalse',)]),
            ('set', 'p', 'q'),
        ]),
    ])
    st.routine('Lit', (), (), [
        ('if', ('hasnt', 'location', 'DARK'), [('rtrue',)]),
        ('if', ('and', ('has', flashlight, 'ON'), ('call', 'Near', flashlight)), [('rtrue',)]),
        ('rfalse',),
    ])
    st.routine('InScope', ('o',), (), [
        ('if', ('not', ('call', 'Near', 'o')), [('rfalse',)]),
        ('if', ('call', 'Lit'), [('rtrue',)]),
        ('if', ('or', ('==', 'o', player), ('in', 'o', player)), [('rtrue',)]),
        ('rfalse',),
    ])
    st.routine('Resolve', ('s', 'e', 'wide'), ('o', 'j', 'ok', 'cnt', 'w', 'first'), [
        ('if', ('>=', 's', 'e'), [('ret', 0)]),
        ('set', 'cnt', 0),
        ('for', 'j', 's', ('-', 'e', 1), [('if', ('not', ('call', 'IsNoise', word('j'))), [('inc', 'cnt')])]),
        ('if', ('==', 'cnt', 0), [('ret', 0)]),
        ('for', 'o', 1, NOBJ, [
            ('if', ('or', 'wide', ('call', 'InScope', 'o')), [
                ('set', 'ok', 1),
                ('for', 'j', 's', ('-', 'e', 1), [
                    ('set', 'w', word('j')),
                    ('if', ('and', ('not', ('call', 'IsNoise', 'w')), ('not', ('call', 'HasWord', 'o', 'w'))),
                     [('set', 'ok', 0), ('break',)]),
                ]),
                ('if', 'ok', [
                    # several objects can share a word (two keys, two knives): for TAKE prefer one you
                    # aren't holding, for everything else prefer one you are holding
                    ('if', ('==', 'first', 0), [('set', 'first', 'o')]),
                    ('if', ('==', 'action', 'TAKE', 'PICK'), [('if', ('notin', 'o', player), [('ret', 'o')])],
                     [('if', ('in', 'o', player), [('ret', 'o')])]),
                ]),
            ]),
        ]),
        ('if', 'first', [('ret', 'first')]),
        ('ret', -1),
    ])
    st.routine('FindPerson', (), ('o',), [
        ('set', 'o', ('child', 'location')),
        ('while', 'o', [
            ('if', ('and', ('has', 'o', 'PERSON'), ('!=', 'o', player)), [('ret', 'o')]),
            ('set', 'o', ('sibling', 'o')),
        ]),
        ('ret', 0),
    ])
    st.routine('PrintA', ('o',), ('a',), [
        ('if', ('has', 'o', 'PROPER'), [('pobj', 'o'), ('rtrue',)]),
        ('set', 'a', ('prop', 'o', 'ARTICLE')),
        ('if', 'a', [('ppaddr', 'a'), ' '], ['a ']),
        ('pobj', 'o'),
    ])
    st.routine('PrintThe', ('o',), (), [
        ('if', ('hasnt', 'o', 'PROPER'), ['the ']),
        ('pobj', 'o'),
    ])
    st.routine('CThe', ('o',), (), [
        ('if', ('hasnt', 'o', 'PROPER'), ['The ']),
        ('pobj', 'o'),
    ])
    st.routine('Award', ('n',), (), [
        ('set', 'score', ('+', 'score', 'n')),
        ('style', 2), '\n[Your score just went up by ', ('pnum', 'n'), ' points.]', ('style', 0), '\n',
    ])
    # list the visible children of o: "a, b and c"; returns how many
    st.routine('Listable', ('c',), (), [
        ('ret', ('?', ('and', ('hasnt', 'c', 'SCENERY'), ('hasnt', 'c', 'CONCEALED'), ('hasnt', 'c', 'PERSON'),
                       ('!=', 'c', player)))),
    ])
    st.routine('ListInline', ('o',), ('c', 'n', 'k', 'i'), [
        ('set', 'n', 0),
        ('set', 'c', ('child', 'o')),
        ('while', 'c', [('if', ('call', 'Listable', 'c'), [('inc', 'n')]), ('set', 'c', ('sibling', 'c'))]),
        ('set', 'c', ('child', 'o')), ('set', 'i', 0),
        ('while', 'c', [
            ('if', ('call', 'Listable', 'c'), [
                ('inc', 'i'),
                ('do', ('call', 'PrintA', 'c')),
                ('if', ('==', 'i', ('-', 'n', 1)), [' and '], [('if', ('<', 'i', ('-', 'n', 1)), [', '])]),
            ]),
            ('set', 'c', ('sibling', 'c')),
        ]),
        ('ret', 'n'),
    ])
    st.routine('LookRoom', (), ('d', 'c', 'n'), [
        ('nl',),
        ('if', ('not', ('call', 'Lit')), [
            ('style', 2), 'Darkness', ('style', 0), '\n',
            "It's as black as a banker's heart in here. You can't see a thing.\n", ('rtrue',)]),
        ('style', 2), ('pobj', 'location'), ('style', 0), '\n',
        ('set', 'd', ('prop', 'location', 'DESCRIBE')),
        ('if', 'd', [('do', ('callv', 'd'))], [('ppaddr', ('prop', 'location', 'DESC')), '\n']),
        ('give', 'location', 'VISITED'),
        # objects with an initial description first, then the rest in one sentence
        ('set', 'n', 0),
        ('set', 'c', ('child', 'location')),
        ('while', 'c', [
            ('if', ('call', 'Listable', 'c'), [
                ('if', ('and', ('hasnt', 'c', 'MOVED'), ('prop', 'c', 'INITIAL')),
                 [('nl',), ('ppaddr', ('prop', 'c', 'INITIAL')), '\n', ('give', 'c', 'CONCEALED'), ('inc', 'n')]),
            ]),
            ('set', 'c', ('sibling', 'c')),
        ]),
        ('set', 'c', ('child', 'location')),
        ('set', 'n', 0),
        ('while', 'c', [('if', ('call', 'Listable', 'c'), [('inc', 'n')]), ('set', 'c', ('sibling', 'c'))]),
        ('if', 'n', ['\nYou can also see ', ('do', ('call', 'ListInline', 'location')), ' here.\n']),
        # un-hide the objects that were described by their initial text
        ('set', 'c', ('child', 'location')),
        ('while', 'c', [
            ('if', ('and', ('hasnt', 'c', 'MOVED'), ('prop', 'c', 'INITIAL'), ('hasnt', 'c', 'SCENERY')),
             [('ungive', 'c', 'CONCEALED')]),
            ('set', 'c', ('sibling', 'c')),
        ]),
    ])
    st.routine('GoTo', ('r',), (), [
        ('set', 'location', 'r'),
        ('move', player, 'r'),
        ('do', ('call', 'LookRoom')),
    ])
    st.routine('Pad', ('n',), ('i',), [('for', 'i', 1, 'n', [' '])])
    st.routine('DrawStatus', (), ('cols', 'm', 'h', 'x'), [
        ('set', 'cols', ('lb', 0, 0x21)),
        ('if', ('<', 'cols', 20), [('set', 'cols', 20)]),
        ('split', 1), ('window', 1), ('style', 1), ('cursor', 1, 1),
        ('do', ('call', 'Pad', 'cols')),
        ('cursor', 1, 2),
        ('if', ('call', 'Lit'), [('pobj', 'location')], ['Darkness']),
        ('set', 'm', ('%', ('+', 1420, 'moves'), 1440)),
        ('set', 'h', ('/', 'm', 60)),
        ('set', 'x', ('-', 'cols', 9)),
        ('if', ('>=', 'cols', 44), [('set', 'x', ('-', 'cols', 22)), ('cursor', 1, 'x'), 'Score: ', ('pnum', 'score'),
                                    ('set', 'x', ('-', 'cols', 9))]),
        ('cursor', 1, 'x'),
        ('set', 'x', ('%', 'h', 12)),
        ('if', ('==', 'x', 0), [('set', 'x', 12)]),
        ('if', ('<', 'x', 10), [' ']),
        ('pnum', 'x'), ':',
        ('if', ('<', ('%', 'm', 60), 10), ['0']),
        ('pnum', ('%', 'm', 60)),
        ('if', ('<', 'h', 12), [' AM'], [' PM']),
        ('style', 0), ('window', 0),
    ])
    st.routine('YesNo', (), ('w',), [
        ('while', 1, [
            '> ', ('do', ('aread', TEXT, PARSE)),
            ('set', 'w', word(0)),
            ('if', ('==', 'w', W('yes'), W('y')), [('rtrue',)]),
            ('if', ('==', 'w', W('no'), W('n')), [('rfalse',)]),
            'Please answer yes or no.\n',
        ]),
    ])

    # ------------------------------------------------ the parser
    st.routine('Parse', (), ('w', 'v', 'd', 'i', 'p', 'n1s', 'n1e', 'n2s', 'n2e', 'j'), [
        ('set', 'nw', ('lb', PARSE, 1)),
        ('if', ('==', 'nw', 0), fail('I beg your pardon?')),
        ('set', 'w', word(0)),
        ('if', ('==', 'w', W('again'), W('g')), [
            ('if', ('==', 'oldlen', 0), fail("You can't very well repeat what you haven't done.")),
            ('for', 'j', 1, 121, [('sb', TEXT, 'j', ('lb', OLD, 'j'))]),
            ('tokenise', TEXT, PARSE),
            ('set', 'nw', ('lb', PARSE, 1)),
        ], [
            ('for', 'j', 1, 121, [('sb', OLD, 'j', ('lb', TEXT, 'j'))]),
            ('set', 'oldlen', ('lb', TEXT, 1)),
        ]),
        ('for', 'i', 0, ('-', 'nw', 1), [
            ('if', ('==', word('i'), 0), [
                'I don\'t know the word "', ('do', ('call', 'PrintWord', 'i')), '".\n', ('rfalse',)]),
        ]),
        ('set', 'action', 0), ('set', 'noun', 0), ('set', 'second', 0), ('set', 'particle', 0),
        ('set', 'prep2', 0), ('set', 'dir', 0),
        ('set', 'w', word(0)),
        ('set', 'v', ('call', 'Data', 'w', 0)),
        ('set', 'd', ('call', 'Data', 'w', 2)),
        ('if', ('==', 'v', 0), [
            ('if', 'd', [('set', 'action', 'GO'), ('set', 'dir', 'd'), ('rtrue',)]),
            ('if', ('call', 'FindPerson'), fail("You'll have to start with a verb. To talk to someone, try TALK TO them, or ASK them ABOUT something.")),
            *fail("That's not a verb I recognise."),
        ]),
        ('set', 'action', 'v'),
        ('set', 'i', 1),
        ('if', ('==', 'action', 'GO'), [
            ('if', 'd', [('set', 'dir', 'd')]),
            ('if', ('<', 'i', 'nw'), [
                ('set', 'd', ('call', 'Data', word('i'), 2)),
                ('if', 'd', [('set', 'dir', 'd'), ('inc', 'i')]),
            ]),
            ('if', 'dir', [('rtrue',)]),
            ('if', ('>=', 'i', 'nw'), fail('Which way do you want to go?')),
            ('set', 'action', 'ENTER'),
        ]),
        ('if', ('<', 'i', 'nw'), [
            ('set', 'p', ('call', 'Data', word('i'), 1)),
            ('if', ('and', 'p', ('!=', 'p', 'NOISE')), [('set', 'particle', 'p'), ('inc', 'i')]),
        ]),
        ('set', 'n1s', 'i'),
        ('while', ('<', 'i', 'nw'), [
            ('set', 'p', ('call', 'Data', word('i'), 1)),
            ('if', ('and', 'p', ('!=', 'p', 'NOISE')), [('break',)]),
            ('inc', 'i'),
        ]),
        ('set', 'n1e', 'i'),
        ('if', ('<', 'i', 'nw'), [('set', 'prep2', ('call', 'Data', word('i'), 1)), ('inc', 'i')]),
        ('set', 'n2s', 'i'), ('set', 'n2e', 'nw'),
        # ------------------------------------------ verb + particle combinations
        ('switch', 'action', [
            ('LOOK', [
                ('if', ('==', 'particle', 'P_AT'), [('set', 'action', 'EXAMINE')],
                 [('if', ('==', 'particle', 'P_IN', 'P_UNDER', 'P_THROUGH'), [('set', 'action', 'SEARCH')],
                   [('if', ('>', 'n1e', 'n1s'), [('set', 'action', 'EXAMINE')])])]),
            ]),
            ('PICK', [('set', 'action', 'TAKE')]),
            ('TAKE', [
                ('if', ('or', ('==', 'particle', 'P_OFF'), ('and', ('==', 'prep2', 'P_OFF'), ('>=', 'n2s', 'n2e'))),
                 [('set', 'action', 'REMOVE')]),
                ('if', ('and', ('==', 'particle', 'P_IN', 'P_OUT'), ('>=', 'n1s', 'n1e')), [
                    ('set', 'action', 'GO'),
                    ('if', ('==', 'particle', 'P_IN'), [('set', 'dir', 'D_IN')], [('set', 'dir', 'D_OUT')]),
                    ('rtrue',)]),
            ]),
            ('PUT', [
                ('if', ('or', ('==', 'particle', 'P_DOWN'), ('==', 'prep2', 'P_DOWN')), [('set', 'action', 'DROP')],
                 [('if', ('or', ('and', ('==', 'particle', 'P_ON'), ('==', 'prep2', 0)),
                             ('and', ('==', 'prep2', 'P_ON'), ('>=', 'n2s', 'n2e'))), [('set', 'action', 'WEAR')],
                   [('if', ('==', 'prep2', 'P_IN', 'P_ON', 'P_UNDER'), [('set', 'action', 'INSERT')],
                     fail('Where do you want to put it?'))])]),
            ]),
            ('TURN', [
                ('if', ('or', ('==', 'particle', 'P_ON'), ('==', 'prep2', 'P_ON')), [('set', 'action', 'SWITCHON')],
                 [('if', ('or', ('==', 'particle', 'P_OFF'), ('==', 'prep2', 'P_OFF')), [('set', 'action', 'SWITCHOFF')],
                   fail('Do you want to turn it on or off?'))]),
            ]),
            ('CLIMB', [
                ('if', ('>=', 'n1s', 'n1e'), [
                    ('if', ('==', 'particle', 'P_UP'), [('set', 'action', 'GO'), ('set', 'dir', 'D_U'), ('rtrue',)]),
                    ('if', ('==', 'particle', 'P_DOWN'), [('set', 'action', 'GO'), ('set', 'dir', 'D_D'), ('rtrue',)]),
                    ('if', ('==', 'particle', 'P_OUT'), [('set', 'action', 'GO'), ('set', 'dir', 'D_OUT'), ('rtrue',)]),
                    ('if', ('==', 'particle', 'P_IN', 'P_THROUGH'), [('set', 'action', 'GO'), ('set', 'dir', 'D_IN'), ('rtrue',)]),
                ]),
            ]),
            ('ENTER', [
                ('if', ('>=', 'n1s', 'n1e'), [('set', 'action', 'GO'), ('set', 'dir', 'D_IN'), ('rtrue',)]),
            ]),
        ]),
        # ------------------------------------------ TAKE ALL / DROP ALL
        ('if', ('and', ('==', 'action', 'TAKE', 'DROP'), ('<', 'n1s', 'nw'),
                ('==', word('n1s'), W('all'), W('everything'))), [('set', 'noun', -2), ('rtrue',)]),
        # ------------------------------------------ objects
        ('if', ('==', 'action', 'ASK'), [
            ('if', ('==', 'particle', 'P_ABOUT', 'P_FOR'), [
                ('set', 'n2s', 'n1s'), ('set', 'n2e', 'n1e'), ('set', 'n1e', 'n1s')]),
            ('set', 'noun', ('call', 'Resolve', 'n1s', 'n1e', 0)),
            ('if', ('==', 'noun', -1), fail("You can't see any such person.")),
            ('if', ('==', 'noun', 0), [('set', 'noun', ('call', 'FindPerson'))]),
            ('if', ('==', 'noun', 0), fail("There's nobody here to ask.")),
            ('if', ('>=', 'n2s', 'n2e'), [
                ('if', ('has', 'noun', 'PERSON'), [('set', 'action', 'TALK'), ('rtrue',)]),
                *fail('Ask about what?')]),
            ('set', 'second', ('call', 'Resolve', 'n2s', 'n2e', 1)),
            ('if', ('==', 'second', -1), [('set', 'second', 0)]),
            ('rtrue',),
        ]),
        ('if', ('==', 'action', 'CALL'), [
            ('set', 'noun', ('call', 'Resolve', 'n1s', 'n1e', 1)),
            ('if', ('==', 'noun', -1), [('set', 'noun', 0)]),
            ('rtrue',),
        ]),
        ('set', 'noun', ('call', 'Resolve', 'n1s', 'n1e', 0)),
        ('if', ('and', ('==', 'noun', -1), ('==', 'action', 'GIVE', 'SHOW'), ('==', 'prep2', 0),
                ('>=', ('-', 'n1e', 'n1s'), 2)), [
            ('set', 'second', ('call', 'Resolve', 'n1s', ('+', 'n1s', 1), 0)),
            ('if', ('>', 'second', 0), [('set', 'noun', ('call', 'Resolve', ('+', 'n1s', 1), 'n1e', 0))]),
        ]),
        ('if', ('==', 'noun', -1), fail("You can't see any such thing.")),
        ('if', ('==', 'second', 0), [('set', 'second', ('call', 'Resolve', 'n2s', 'n2e', 0))]),
        ('if', ('==', 'second', -1), fail("You can't see any such thing.")),
        ('if', ('and', ('==', 'noun', 0), ('==', 'action', 'TALK', 'WAKE', 'KISS')), [('set', 'noun', ('call', 'FindPerson'))]),
        ('if', ('and', ('==', 'second', 0), ('==', 'action', 'GIVE', 'SHOW')), [('set', 'second', ('call', 'FindPerson'))]),
        ('if', ('and', ('==', 'noun', 0), ('==', 'action', *NEEDNOUN)), [
            'What do you want to ', ('do', ('call', 'PrintWord', 0)),
            ('if', ('and', 'particle', ('>', 'nw', 1)), [' ', ('do', ('call', 'PrintWord', 1))]),
            '?\n', ('rfalse',)]),
        ('rtrue',),
    ])

    # ------------------------------------------------ default actions
    st.routine('DoAllIn', ('o',), ('c', 'n', 'k'), [
        ('set', 'k', 0),
        ('set', 'c', ('child', 'o')),
        ('while', 'c', [
            ('set', 'n', ('sibling', 'c')),
            ('if', ('and', ('call', 'Listable', 'c'), ('hasnt', 'c', 'STATIC'), ('hasnt', 'c', 'WORN')), [
                ('inc', 'k'),
                ('pobj', 'c'), ': ', ('set', 'noun', 'c'), ('do', ('call', 'Perform'))]),
            ('if', ('and', ('==', 'action', 'TAKE'), ('has', 'c', 'CONTAINER'), ('has', 'c', 'OPEN')),
             [('set', 'k', ('+', 'k', ('call', 'DoAllIn', 'c')))]),
            ('set', 'c', 'n'),
        ]),
        ('ret', 'k'),
    ])
    st.routine('DoAll', (), ('k',), [
        ('if', ('==', 'action', 'TAKE'), [('set', 'k', ('call', 'DoAllIn', 'location'))],
         [('set', 'k', ('call', 'DoAllIn', player))]),
        ('if', ('==', 'k', 0), ['There is nothing to ', ('if', ('==', 'action', 'TAKE'), ['take'], ['drop']), '.\n']),
    ])
    st.routine('Perform', (), ('b',), [
        ('if', ('==', 'noun', -2), [('do', ('call', 'DoAll')), ('rtrue',)]),
        ('set', 'b', ('prop', 'location', 'BEFORE')),
        ('if', 'b', [('if', ('callv', 'b'), [('rtrue',)])]),
        ('if', ('and', 'second', ('!=', 'second', 'noun'), ('!=', 'action', 'ASK')), [
            ('set', 'b', ('prop', 'second', 'BEFORE')),
            ('if', 'b', [('if', ('callv', 'b'), [('rtrue',)])]),
        ]),
        ('if', 'noun', [
            ('set', 'b', ('prop', 'noun', 'BEFORE')),
            ('if', 'b', [('if', ('callv', 'b'), [('rtrue',)])]),
        ]),
        ('do', ('call', 'Default')),
    ])

    st.routine('Default', (), ('d', 'c', 'r'), [('switch', 'action', [
        ('LOOK', [('do', ('call', 'LookRoom'))]),
        (('EXAMINE', 'READ'), [
            ('set', 'd', ('prop', 'noun', 'DESC')),
            ('if', 'd', [('ppaddr', 'd'), '\n'],
             ['You see nothing special about ', ('do', ('call', 'PrintThe', 'noun')), '.\n']),
            ('if', ('has', 'noun', 'SWITCHABLE'), [
                'It is switched ', ('if', ('has', 'noun', 'ON'), ['on'], ['off']), '.\n']),
            ('if', ('and', ('has', 'noun', 'CONTAINER'), ('or', ('has', 'noun', 'OPEN'), ('has', 'noun', 'TRANSPARENT')),
                    ('child', 'noun')), [
                'In ', ('do', ('call', 'PrintThe', 'noun')), ' you can see ',
                ('do', ('call', 'ListInline', 'noun')), '.\n']),
        ]),
        ('TAKE', [
            ('if', ('==', 'noun', player), fail("You've been trying to get a grip on yourself for years.")),
            ('if', ('in', 'noun', player), fail('You already have that.')),
            ('if', ('has', 'noun', 'PERSON'), [
                'I don\'t think ', ('do', ('call', 'PrintThe', 'noun')), ' would appreciate that.\n', ('rtrue',)]),
            ('if', ('or', ('has', 'noun', 'SCENERY'), ('has', 'noun', 'STATIC')), fail("That isn't going anywhere.")),
            ('move', 'noun', player), ('give', 'noun', 'MOVED'), ('ungive', 'noun', 'CONCEALED'),
            'Taken.\n',
        ]),
        ('DROP', [
            ('if', ('notin', 'noun', player), fail("You aren't holding that.")),
            ('ungive', 'noun', 'WORN'), ('move', 'noun', 'location'), 'Dropped.\n',
        ]),
        ('INV', [
            ('if', ('==', ('child', player), 0), fail('Your pockets hold nothing but lint and regret.')),
            'You are carrying:\n',
            ('set', 'c', ('child', player)),
            ('while', 'c', [
                '  ', ('do', ('call', 'PrintA', 'c')),
                ('if', ('has', 'c', 'WORN'), [' (being worn)']),
                ('if', ('and', ('has', 'c', 'SWITCHABLE'), ('has', 'c', 'ON')), [' (switched on)']),
                '\n',
                ('set', 'c', ('sibling', 'c')),
            ]),
        ]),
        ('GO', [
            ('set', 'd', ('prop', 'location', ('+', 'dir', 3))),
            ('if', ('==', 'd', 0), fail("You can't go that way.")),
            ('do', ('call', 'GoTo', 'd')),
        ]),
        ('OPEN', [
            ('if', ('hasnt', 'noun', 'OPENABLE'), fail("That's not something you can open.")),
            ('if', ('has', 'noun', 'OPEN'), fail("It's already open.")),
            ('if', ('has', 'noun', 'LOCKED'), fail("It's locked.")),
            ('give', 'noun', 'OPEN'),
            'You open ', ('do', ('call', 'PrintThe', 'noun')),
            ('if', ('and', ('child', 'noun'), ('has', 'noun', 'CONTAINER')), [
                ', revealing ', ('do', ('call', 'ListInline', 'noun'))]),
            '.\n',
        ]),
        ('CLOSE', [
            ('if', ('hasnt', 'noun', 'OPENABLE'), fail("That's not something you can close.")),
            ('if', ('hasnt', 'noun', 'OPEN'), fail("It's already closed.")),
            ('ungive', 'noun', 'OPEN'), 'You close ', ('do', ('call', 'PrintThe', 'noun')), '.\n',
        ]),
        ('UNLOCK', [
            ('if', ('hasnt', 'noun', 'LOCKED'), fail("It isn't locked.")),
            ('set', 'd', ('prop', 'noun', 'WITH_KEY')),
            ('if', ('and', 'd', ('in', 'd', player)), [
                ('ungive', 'noun', 'LOCKED'), 'You unlock ', ('do', ('call', 'PrintThe', 'noun')), ' with ',
                ('do', ('call', 'PrintThe', 'd')), '.\n', ('rtrue',)]),
            "You don't have anything that fits that lock.\n",
        ]),
        ('LOCK', ['You see no reason to lock anything tonight.\n']),
        ('GIVE', [
            ('if', ('==', 'second', 0), fail('Give it to whom?')),
            ('if', ('notin', 'noun', player), fail("You'd need to be holding it first.")),
            ('do', ('call', 'CThe', 'second')), " doesn't seem interested.\n",
        ]),
        ('SHOW', [
            ('if', ('==', 'second', 0), fail('Show it to whom?')),
            ('do', ('call', 'CThe', 'second')), ' glances at it and shrugs.\n',
        ]),
        ('TALK', [
            ('if', ('hasnt', 'noun', 'PERSON'), fail("You've been alone too long, Sam. It doesn't talk back.")),
            ('do', ('call', 'CThe', 'noun')), ' has nothing to say to you right now.\n',
        ]),
        ('ASK', [
            ('if', ('hasnt', 'noun', 'PERSON'), fail("You'd get more out of a lamppost.")),
            ('do', ('call', 'CThe', 'noun')), ' shrugs.\n',
        ]),
        ('SHOOT', [
            ('if', ('notin', 'revolver', player), fail("You'd need a gun in your hand for that.")),
            ('if', ('==', 'loaded', 0), fail('Click. The revolver is empty. You forgot to load it, genius.')),
            "You've only got six bullets. Save them for something that deserves it.\n",
        ]),
        ('ATTACK', [
            ('if', ('has', 'noun', 'PERSON'), fail("Violence is the last refuge of the private eye, and you're not there yet.")),
            "Hitting things won't solve this case.\n",
        ]),
        ('CUT', ["You'd need a good reason, and something sharp.\n"]),
        ('FREE', ["There's nobody here who needs setting free. Except maybe you.\n"]),
        ('SWITCHON', [
            ('if', ('hasnt', 'noun', 'SWITCHABLE'), fail("That's not something you can switch on.")),
            ('if', ('has', 'noun', 'ON'), fail("It's already on.")),
            ('set', 'r', ('call', 'Lit')),
            ('give', 'noun', 'ON'), 'You switch on ', ('do', ('call', 'PrintThe', 'noun')), '.\n',
            ('if', ('and', ('not', 'r'), ('call', 'Lit')), [('do', ('call', 'LookRoom'))]),
        ]),
        ('SWITCHOFF', [
            ('if', ('hasnt', 'noun', 'SWITCHABLE'), fail("That's not something you can switch off.")),
            ('if', ('hasnt', 'noun', 'ON'), fail("It's already off.")),
            ('ungive', 'noun', 'ON'), 'You switch off ', ('do', ('call', 'PrintThe', 'noun')), '.\n',
        ]),
        ('WEAR', [
            ('if', ('hasnt', 'noun', 'CLOTHING'), fail("You can't wear that.")),
            ('if', ('has', 'noun', 'WORN'), fail("You're already wearing it.")),
            ('if', ('notin', 'noun', player), fail("You'll need to pick it up first.")),
            ('give', 'noun', 'WORN'), 'You put on ', ('do', ('call', 'PrintThe', 'noun')), '.\n',
        ]),
        ('REMOVE', [
            ('if', ('and', ('has', 'noun', 'WORN'), ('in', 'noun', player)), [
                ('ungive', 'noun', 'WORN'), 'You take off ', ('do', ('call', 'PrintThe', 'noun')), '.\n', ('rtrue',)]),
            ('set', 'action', 'TAKE'), ('do', ('call', 'Perform')),
        ]),
        ('DRINK', ["That's not something you can drink.\n"]),
        ('EAT', ["You're not that hungry. You're not that desperate, either.\n"]),
        ('LOAD', ["You can't load that.\n"]),
        ('CALL', ["There's no telephone here.\n"]),
        ('WAKE', ["You're wide awake. Unfortunately.\n"]),
        (('RING', 'PUSH', 'PULL'), ['Nothing happens.\n']),
        ('SIT', ["There's no time to sit down. Eddie doesn't have time.\n"]),
        ('LISTEN', ['Rain. Always the rain.\n']),
        ('SMELL', ['Wet city: tar, cigarette smoke and the sea.\n']),
        ('WAIT', ["Time passes. The rain doesn't.\n"]),
        ('SCORE', ['You have scored ', ('pnum', 'score'), ' out of a possible 100, in ', ('pnum', 'moves'), ' turns.\n']),
        ('SAVE', [
            ('set', 'r', ('save',)),
            ('if', ('==', 'r', 0), fail('Saving failed.')),
            ('if', ('==', 'r', 1), fail('Game saved in this browser. Type RESTORE to come back to this moment.')),
            'Game restored.\n', ('do', ('call', 'LookRoom')),
        ]),
        ('RESTORE', [('do', ('restore',)), "Restoring failed: there's no saved game in this browser yet.\n"]),
        ('UNDO', [('do', ('restore_undo',)), "You can't undo any further.\n"]),
        ('RESTART', ['Are you sure you want to start over?\n', ('if', ('call', 'YesNo'), [('restart',)]), 'Okay.\n']),
        ('QUIT', ['Are you sure you want to quit?\n', ('if', ('call', 'YesNo'), [('quit',)]), 'Okay.\n']),
        ('SEARCH', [
            ('if', ('==', 'noun', 0), [('do', ('call', 'LookRoom')), ('rtrue',)]),
            ('if', ('and', ('has', 'noun', 'CONTAINER'), ('or', ('has', 'noun', 'OPEN'), ('has', 'noun', 'TRANSPARENT')),
                    ('child', 'noun')), [
                'In ', ('do', ('call', 'PrintThe', 'noun')), ' you can see ', ('do', ('call', 'ListInline', 'noun')),
                '.\n', ('rtrue',)]),
            ('if', ('and', ('has', 'noun', 'CONTAINER'), ('hasnt', 'noun', 'OPEN')), fail("You'd have to open it first.")),
            'You find nothing of interest.\n',
        ]),
        ('INSERT', [
            ('if', ('==', 'second', 0), fail('Put it where?')),
            ('if', ('notin', 'noun', player), fail("You're not holding that.")),
            ('if', ('and', ('has', 'second', 'CONTAINER'), ('has', 'second', 'OPEN')), [
                ('move', 'noun', 'second'), 'You put ', ('do', ('call', 'PrintThe', 'noun')), ' in ',
                ('do', ('call', 'PrintThe', 'second')), '.\n', ('rtrue',)]),
            'You can\'t put things in ', ('do', ('call', 'PrintThe', 'second')), '.\n',
        ]),
        ('CLIMB', ["There's nothing here worth climbing.\n"]),
        ('ENTER', ["You can't get into that.\n"]),
        ('PLAY', ["You've got no ear for it.\n"]),
        ('KISS', ['This is no time for romance, Sam.\n']),
        ('JUMP', ['You jump on the spot. Your knees file a complaint.\n']),
        ('SLEEP', ['You can sleep when you\'re dead. At this rate, that might be soon.\n']),
        ('XYZZY', ["A hollow voice says: 'Wrong genre, gumshoe.'\n"]),
        ('SING', ["You hum a few bars of 'Stormy Weather'. The rain seems to agree with every word.\n"]),
        ('THINK', ['You think hard. Your head hurts. Maybe try HINT.\n']),
        ('KNOCK', ['Nobody answers.\n']),
        ('USE', ["You'll need to be more specific. Try a verb like OPEN, UNLOCK, SHOOT, CALL or TURN ON.\n"]),
        ('HIDE', ['There\'s nowhere to hide that a professional wouldn\'t look.\n']),
        ('PET', ["That's not the kind of thing you pet.\n"]),
        ('SMOKE', ['You quit in 1946. Mostly.\n']),
        (('YES', 'NO'), ['That was a rhetorical question.\n']),
    ], ["You can't do that here.\n"])])
