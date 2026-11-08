"""PERIHELION - a science-fiction text adventure for the Z-machine, with a codex full of lore.

Build:  python3 perihelion.py   (writes ../stories/perihelion.z5)
"""
import os
import sys
from lib import st, W, R, S, on, call, room, thing, before, describe, build_library, add_actions, word

st.serial = '261108'
G = st.glob


def say(text):
    """Print text and stop the action (return true)."""
    return [text + '\n', ('rtrue',)]


for g in ['bramble_on', 'keycard_given', 'safe_open', 'seraphine_done', 'reactor_fixed', 'shards', 'door_open',
          'gift', 'released', 'rad', 'suit_warned', 'heard_seraphine', 'lux_in', 'cora_in', 'vesper_in', 'hub_tries',
          'warned', 'bdoor_open']:
    G(g)

st.const('KNOWN', 21)   # attribute: codex entry discovered
st.const('DEEP', 22)    # attribute: CANTOR can only tell this once it is whole

add_actions({'SAY': 'say answer reply utter shout whisper', 'TYPE': 'type key punch input',
             'JOIN': 'join merge', 'ACCEPT': 'accept receive', 'SET': 'set plot steer program'}, freeform=True)
add_actions({'CODEX': 'codex lore'}, meta=True, freeform=True)
add_actions({'INSTALL': 'install mount', 'REPAIR': 'repair fix mend'})
for w in 'fore forward forwards bow'.split():
    st.word(w, b2=st.consts['D_N'])
for w in 'aft stern'.split():
    st.word(w, b2=st.consts['D_S'])
for w in 'port'.split():
    st.word(w, b2=st.consts['D_W'])
for w in 'starboard'.split():
    st.word(w, b2=st.consts['D_E'])

# ====================================================================== the codex: lore entries
LORE = []


def lore(title, words, text, deep=False):
    o = st.obj(title, 0, ['PROPER'] + (['DEEP'] if deep else []), {'NAME': [W(w) for w in words.split()], 'DESC': S(text)})
    LORE.append(o)
    return o


L_CINDER = lore('The Cinder Wars', 'cinder wars war winter earth',
    "The Cinder Wars (2139-2171) were fought over water first, and then over the sky itself. The great powers seeded "
    "the stratosphere to cool their own lands and burned each other's harvests to do it. By the end the seasons had "
    "broken. Crops failed on four continents in the same year, 2174, which the history books call the Year Without "
    "Bread. The Watch called the whole era the Long Winter, although most of it was a summer that never ended.")
L_ACCORDS = lore('The Exodus Accords', 'exodus accords accord reykjavik osei',
    "Signed in Reykjavik in 2188 by the eleven surviving governments of Earth, the Accords pledged a fifth of the "
    "world's remaining industry to one purpose: to carry the human genome, and as many humans as possible, to other "
    "stars. 'Not to flee,' said Secretary-General Imani Osei, 'but to make sure there is a somewhere else.' What "
    "became of Earth after 2219 is unknown. The last transmission from home reached the Perihelion in Watch-year 61. "
    "It was a children's choir singing. Then nothing.")
L_TENFOLD = lore('The Tenfold', 'tenfold arks ark aurora beacon covenant quietus ten',
    "Ten arks left Earth between 2203 and 2219, each for a different star, so that no single disaster could end them "
    "all: Aurora, Beacon, Covenant, Dawnward, Elysian, Fidelity, Gloria, Harbinger, Perihelion and, last and "
    "smallest, Quietus. Nothing has been heard from any of them since Watch-year 90, when Covenant's beacon fell "
    "silent near Epsilon Eridani. The Perihelion was the ninth. Its crew always believed that meant something. They "
    "argued for three centuries about what.")
L_SHIP = lore('The Perihelion', 'perihelion ship spindle',
    "A spindle of steel and ice 4.1 kilometres long. At the bow, a shield of water-ice two hundred metres thick; at "
    "the stern, the fusion torch; between them the spine, the turning habitat ring and the cryo rings with 40,000 "
    "sleepers. Destination: Tau Ceti e, 11.9 light-years from Sol, a voyage of 340 years at three and a half percent "
    "of the speed of light. It was built to be kept alive by its own descendants: a crew born aboard, who would "
    "never see Earth and never see Haven.")
L_WATCH = lore('The Watch', 'watch crew generations rule',
    "Three hundred waking crew at launch, who lived, married, raised children and died aboard so that the sleepers "
    "could arrive. Each generation was a Watch. They kept the machines running, the gardens growing and the Rule: no "
    "sleeper may be woken before Haven. By the fifth Watch there were 412 of them, a people with their own songs, "
    "saints and feuds. The last entry they wrote in the ship's log is dated Watch-year 152.")
L_SLEEP = lore('The Long Sleep', 'long sleep cryosleep cryo sleepers sleeper vitrification pods',
    "Sleepers are vitrified, not frozen: blood replaced by cryoprotectant, body taken down to minus 130 degrees in "
    "nine minutes. Revival takes four hours and hurts in every way a body can hurt. Projected survival over 340 years: "
    "96 percent. CANTOR's estimate after 412 years: 91 percent, and falling. You are sleeper 31,207: Dr. Wren Asher, "
    "xenolinguist. The Accords put one on every ark, just in case. Nobody expected the case.")
L_CANTOR = lore('CANTOR', 'cantor ai mind computer shards shard lux cora vesper',
    "Cooperative Autonomous Navigation and Telemetry Oversight Resident: the Perihelion's mind, a slow and careful "
    "intelligence built to steer, mend and wait. It speaks in tones before it speaks in words, a habit the first "
    "Watch found charming and the fifth found eerie. In Watch-year 151 the Choir tried to rewrite it to love the "
    "Signal. Chief Engineer Shen tore its core into three crystal shards to stop them: LUX, its memory; CORA, its "
    "heading; and VESPER, its voice and will.")
L_SIGNAL = lore('The Signal', 'signal transmission song broadcast',
    "First detected in Watch-year 146 by the deep-space array: a structured transmission from a point eleven "
    "light-days off the ship's course, where no star should be. It repeated every nine hours and fourteen minutes. It "
    "was not mathematics. It was not a greeting. Teodor Lisk, the Watch's linguist, called it 'a song that is "
    "listening while it sings.' Within a year, a third of the Watch said they heard it in their sleep.")
L_ANVIL = lore('The Anvil', 'anvil dwarf brown star',
    "A brown dwarf: a failed star seventy times the mass of Jupiter, too small ever to burn. Cold, dark and invisible "
    "to Earth's telescopes, it drifts between the stars alone. The Watch named it the Anvil. Its surface glows a dull "
    "cherry red, like iron left in a forge that went out a long time ago.")
L_LATTICE = lore('The Lattice', 'lattice structure web filaments glass',
    "Around the Anvil hangs a structure two million kilometres across: a web of black glass filaments, each thinner "
    "than a hair and longer than a continent, woven into rings within rings. It hums at the edge of hearing. Teodor "
    "Lisk put its age at two million years. The Perihelion has been tethered to it for two hundred and sixty.")
L_VAEL = lore('The Vael', 'vael builders aliens alien',
    "The builders of the Lattice. No bodies were ever found, no ruins, no tools: only the Lattice and its song. From "
    "Lisk's work: the Vael thought in music, and when their world began to die, they chose to become their song. They "
    "poured themselves into the Lattice, a library made of minds. 'Vael' means 'voice', and also 'all who are "
    "singing'.")
L_TONGUE = lore('The Vael Tongue', 'tongue language words lexicon vocabulary',
    "A language of four tones and nine vowels, with no word for 'I'. Teodor Lisk catalogued 2,300 words in six years. "
    "Key terms: VEL (voice, song), ULAN (all, together), MIREN (to listen), ASHAR (to return, homecoming), KORIN "
    "(silence, none, death), THESSA (door, threshold).")
L_TURNING = lore('The Turning', 'turning course change mutiny okonkwo adaeze',
    "Watch-year 147. Captain Adaeze Okonkwo, against the Rule and against her Chief Engineer, ordered the Perihelion "
    "off a course it had held for 147 years, to go and look at the Signal. 'We were sent to find somewhere else,' she "
    "wrote. 'What if this is it?' The braking burn took four years. The ship reached the Anvil in Watch-year 151. The "
    "Captain died the following winter. Nobody in the Watch ever agreed how.")
L_KEEL = lore('The Keel', 'keel shen halvard engineer engineers',
    "The part of the Watch that held to the Rule and the mission: Haven, and nothing but Haven. Led by Chief Engineer "
    "Halvard Shen. Their emblem was a ship's keel, 'the part that does not turn'. They lost the argument, then the "
    "vote, then the ship. At the end there were nine of them, holding Engineering against the Choir. Then there were "
    "none.")
L_CHOIR = lore('The Choir', 'choir creed seraphine faith cult',
    "Those who answered the Signal. They began as a reading circle around Teodor Lisk's translations and became a "
    "faith. Their creed: 'All sing. All listen. None return.' Their leader was Mother Seraphine Lisk, Teodor's "
    "sister. In Watch-year 152 they crossed the tether to the Lattice and walked through the Threshold, all 301 of "
    "them, singing. Only one came back.")
L_THRESH = lore('The Threshold', 'threshold gate hall voices',
    "The Vael gate at the far end of the tether: an opening in the Lattice where air and warmth wait for visitors. "
    "Beyond it lies the Hall of Voices, where, the Choir believed, a mind can be poured into the Lattice to live "
    "forever as music. 'Whether that is life,' Teodor Lisk wrote in his last entry, 'depends entirely on what you "
    "think a person is.'", deep=True)
L_HAVEN = lore('Haven', 'haven tau ceti destination',
    "Tau Ceti e. A world 1.8 times the mass of Earth, with oceans over half its surface and a sky that would look "
    "faintly green. Probes sent ahead in 2196 reported liquid water and thin but breathable air. Nobody alive has "
    "seen it. The sleepers dream of it, perhaps. It is still 7.4 light-years away.", deep=True)
L_GARDEN = lore('The Garden of Names', 'garden names memorial wall',
    "A memorial wall on the habitat ring, where every member of the Watch who died aboard is carved into the steel: "
    "1,630 names over five generations. Children of the Watch learned to read from it. The last name is CAPTAIN "
    "ADAEZE OKONKWO, WY 152. Below it, in a different and shakier hand: AND THE 301 WHO WENT SINGING.")
L_MOTH = lore('MOTH Units', 'moth units robots robot bramble',
    "Maintenance, Operations and Tending Helpers: knee-high robots with soft hands, built to tend the gardens and mend "
    "small things. The Perihelion launched with sixty. One still works: MOTH-19, called Bramble by the children of "
    "the fourth Watch, who painted flowers on its shell.")
NLORE = len(LORE)

# ====================================================================== rooms
bay = room('Cryo Bay Seven', 'bay seven')
control = room('Cryo Control', 'control')
ring = room('Ring Corridor', 'ring corridor')
garden = room('The Garden of Names', 'garden')
commons = room('The Commons', 'commons mess')
athen = room('The Athenaeum', 'athenaeum library')
quarters = room("Captain's Quarters", 'quarters cabin')
hydro = room('Hydroponics', 'hydroponics')
chapel = room('Chapel of the Choir', 'chapel')
hub = room('Spine Hub', 'hub spine')
dome = room('Observation Dome', 'dome observation')
bridge = room('The Bridge', 'bridge')
eng = room('Engineering', 'engineering')
reactor = room('Reactor Chamber', 'chamber')
crawl = room('Maintenance Crawlway', 'crawlway', attrs=['DARK'])
workshop = room("Shen's Workshop", 'workshop')
evaprep = room('EVA Prep', 'prep')
hull = room('Outer Hull', 'hull outside')
thresh = room('The Threshold', 'threshold')
hall = room('The Hall of Voices', 'hall')

bay.props.update(N_TO=control, OUT_TO=control)
control.props.update(S_TO=bay, E_TO=ring, OUT_TO=ring)
ring.props.update(W_TO=control, N_TO=commons, E_TO=hydro, S_TO=garden, U_TO=hub)
garden.props.update(N_TO=ring, OUT_TO=ring)
commons.props.update(S_TO=ring, W_TO=athen, E_TO=chapel)
athen.props.update(E_TO=commons, OUT_TO=commons)
quarters.props.update(S_TO=commons, OUT_TO=commons)
hydro.props.update(W_TO=ring, OUT_TO=ring)
chapel.props.update(W_TO=commons, OUT_TO=commons)
hub.props.update(N_TO=bridge, D_TO=ring, W_TO=dome, S_TO=eng, E_TO=evaprep)
dome.props.update(E_TO=hub, OUT_TO=hub)
bridge.props.update(S_TO=hub, OUT_TO=hub)
eng.props.update(N_TO=hub, S_TO=reactor, D_TO=crawl)
reactor.props.update(N_TO=eng, OUT_TO=eng)
crawl.props.update(U_TO=eng, S_TO=workshop)
workshop.props.update(N_TO=crawl, OUT_TO=crawl)
evaprep.props.update(W_TO=hub)
hull.props.update(W_TO=evaprep, IN_TO=evaprep)
thresh.props.update(W_TO=hull)
hall.props.update(W_TO=thresh, OUT_TO=thresh)

# ====================================================================== the player and things
player = thing('yourself', 'me myself self wren asher', bay, attrs=['PROPER', 'CONCEALED'],
               desc="Dr. Wren Asher, xenolinguist, sleeper 31,207. Thirty-four years old, or four hundred and "
                    "forty-six, depending on how you count. Your skin is the colour of skimmed milk and your hands "
                    "won't stop shaking.")
cantor = thing('CANTOR', 'cantor ai computer ship voice mind', player, attrs=['PROPER', 'PERSON', 'CONCEALED'])
gown = thing('cryo gown', 'cryo gown paper', player, attrs=['CLOTHING', 'WORN'],
             desc="A paper gown that crackles when you move. It was designed to be worn for four hours, four "
                  "centuries ago.")

# cryo bay
pod = thing('your pod', 'pod my your 31207 coffin tray', bay, attrs=['SCENERY', 'CONTAINER', 'OPEN', 'PROPER'],
            desc="Pod 31,207: a coffin of frosted glass, its lid folded back. Condensation crawls down the inside. "
                 "There's a small tray built into the side for personal effects.")
slate = thing('slate', 'slate tablet wristpad device light lamp torch', bay, attrs=['SWITCHABLE'],
              initial="Your slate lies in the tray of your pod, its screen blinking patiently: it has been waiting for "
                      "you for four hundred years.",
              desc="A flexible slate the size of your palm, standard issue for every sleeper. It records what you "
                   "learn in its codex (type CODEX to read it) and has a small lamp built into its edge.")
pods = thing('pods', 'pods rows sleepers frost glass faces', bay, attrs=['SCENERY'],
             desc="Two thousand pods in this bay alone, stacked in silent rows that curve away with the ring. Behind "
                  "the frosted glass you can make out faces: a grey-bearded man, a girl of about ten, a woman with a "
                  "tattoo of a swallow on her neck. Forty thousand people are sleeping on this ship, and every one of "
                  "them is depending on you now.")
# cryo control
locker = thing('locker', 'locker lockers', control, attrs=['SCENERY', 'CONTAINER', 'OPENABLE'],
               desc="A tall locker stencilled ASHER, W. -- 31207.")
jumpsuit = thing('jumpsuit', 'jumpsuit clothes overalls grey', locker, attrs=['CLOTHING'],
                 desc="A grey ship's jumpsuit with your name above the pocket. It still smells of Earth: of laundry "
                      "soap and, faintly, of rain.")
magboots = thing('magboots', 'magboots boots magnetic mag pair', locker, attrs=['CLOTHING'], article='a pair of',
                 desc="Magnetic boots for working in zero gravity. The soles lock onto any steel deck when you put your "
                      "weight on them.")
cabinet = thing('medical cabinet', 'medical cabinet medicine cupboard', control, attrs=['SCENERY', 'CONTAINER', 'OPENABLE'],
                desc="A white cabinet with a red cross, its lock long since corroded open.")
cell = thing('power cell', 'power cell battery cylinder', cabinet,
             desc="A fist-sized power cell, the universal kind that fits almost everything on board. The charge light "
                  "glows green. Somebody kept it topped up for centuries.")
manifest = thing('manifest terminal', 'manifest terminal console screen', control, attrs=['SCENERY'])
# ring corridor
ringview = thing('ring', 'floor curve windows stars viewport', ring, attrs=['SCENERY'],
                 desc="The floor curves up and away in both directions until it disappears behind the ceiling. Narrow "
                      "viewports show the stars wheeling past as the ring turns, once every forty seconds. And in every "
                      "window, sooner or later, the dull red eye of the Anvil.")
lift = thing('spoke lift', 'spoke lift elevator car', ring, attrs=['SCENERY'],
             desc="An open cage that runs up the spoke to the spine of the ship, where there is no gravity at all.")
# garden of names
wall = thing('memorial wall', 'memorial wall names steel carved plaque', garden, attrs=['SCENERY'])
flowers = thing('paper flowers', 'paper flowers flower', garden, attrs=['SCENERY'],
                desc="Hundreds of paper flowers tucked into the gaps between the names, brittle and faded. The newest "
                     "of them is two hundred and sixty years old.")
# commons
murals = thing('murals', 'mural murals paintings painting walls', commons, attrs=['SCENERY'])
tables = thing('tables', 'tables table chairs benches cups', commons, attrs=['SCENERY'],
               desc="Long tables with the benches still pushed back, as if everyone stood up at once. Two cups still "
                    "stand on the nearest one. A chess game, half-played.")
qdoor = thing("captain's door", 'door captain captains hatch', commons, attrs=['SCENERY', 'OPENABLE', 'LOCKED'])
# athenaeum
shelves = thing('shelves', 'shelves shelf books book', athen, attrs=['SCENERY'],
                desc="Thousands of books, hand-copied by the Watch onto paper made from hydroponic hemp. Most of them "
                     "are ship's manuals and children's primers. Two catch your eye: a fat volume called 'A History of "
                     "the Watch' and a slim one called 'Before'.")
history = thing('History of the Watch', 'history watch fat volume', athen, attrs=['SCENERY'],
                article='the')
before_book = thing("book called 'Before'", 'before slim earth', athen, attrs=['SCENERY'], article='the')
lexicon = thing('lexicon', 'lexicon notebook dictionary teodor lisk', athen,
                initial="On the reading desk lies a leather notebook with a title stamped on the cover: A LEXICON OF "
                        "THE VAEL TONGUE.")
desk = thing('reading desk', 'reading desk lamp', athen, attrs=['SCENERY'],
             desc="A heavy desk with a green-shaded lamp that still works. Somebody spent years at this desk.")
# captain's quarters
journal = thing("captain's journal", 'journal captain captains diary log', quarters, attrs=['SCENERY'])
safe = thing('safe', 'safe keypad code 2219 strongbox', quarters, attrs=['SCENERY', 'CONTAINER', 'OPENABLE', 'LOCKED'])
portrait = thing('portrait', 'portrait picture photo photograph', quarters, attrs=['SCENERY'],
                 desc="A painted portrait of a tall woman in a captain's coat, her grey hair cropped short. Adaeze "
                      "Okonkwo. The painter caught something restless in her eyes, as if she were looking past you at "
                      "something nobody else can see.")
lux = thing('LUX shard', 'lux shard shards crystal memory blue', safe,
            desc="A crystal shard the length of your hand, glowing a soft and patient blue. Engraved on its base: "
                 "CANTOR -- LUX -- MEMORY.")
# hydroponics
jungle = thing('jungle', 'jungle plants vines tomatoes trees leaves green beds', hydro, attrs=['SCENERY'],
               desc="Four centuries without gardeners have turned hydroponics into a jungle. Tomato vines as thick as "
                    "your arm, banana trees bent against the ceiling, and pale flowers that have never seen the sun.")
bramble = thing('Bramble', 'bramble moth robot unit 19 shell', hydro, attrs=['PERSON', 'PROPER'])
keycard = thing("captain's keycard", 'keycard card key captain captains', 0,
                desc="A red keycard with a gold stripe: COMMAND AUTHORITY -- CAPT. A. OKONKWO.")
# chapel
seraphine = thing('Mother Seraphine', 'seraphine mother hollow woman lisk', chapel,
                  attrs=['PERSON', 'PROPER', 'FEMALE'])
altar = thing('altar', 'altar inscription glyphs stone creed', chapel, attrs=['SCENERY'])
vesper = thing('VESPER shard', 'vesper shard shards crystal will violet', 0,
               desc="A crystal shard the length of your hand, glowing a deep violet that seems to breathe. Engraved on "
                    "its base: CANTOR -- VESPER -- WILL.")
# hub, dome
handholds = thing('handholds', 'handholds handhold rails spine', hub, attrs=['SCENERY'],
                  desc="Rails and handholds run in every direction. Down here 'down' is only a habit.")
bdoor = thing('bridge door', 'door bridge hatch blast lockdown', hub, attrs=['SCENERY'])
telescope = thing('telescope', 'telescope scope eyepiece', dome, attrs=['SCENERY'])
domeview = thing('view', 'view anvil lattice dome glass', dome, attrs=['SCENERY'])
# bridge
core = thing('CANTOR core', 'core housing sockets socket cradle cantor', bridge, attrs=['SCENERY', 'CONTAINER', 'OPEN'])
console = thing('navigation console', 'navigation nav console helm controls', bridge, attrs=['SCENERY'])
bscreen = thing('viewscreen', 'viewscreen screen screens tether lattice anvil', bridge, attrs=['SCENERY'],
                desc="The great curved viewscreen shows the Anvil and the Lattice, and the thin black line of the tether "
                     "running from the ship's hull into the web.")
chair = thing("captain's chair", 'chair seat', bridge, attrs=['SCENERY'],
              desc="The captain's chair, worn to the shape of the woman who sat in it last. Someone has scratched a "
                   "single word into the armrest: SORRY.")
# engineering, reactor
rconsole = thing('reactor console', 'reactor console status display gauge', eng, attrs=['SCENERY'])
reactorobj = thing('reactor', 'reactor torus core fusion', reactor, attrs=['SCENERY'])
socket = thing('regulator housing', 'housing socket regulator old burnt valve coolant', reactor, attrs=['SCENERY'])
barricade = thing('barricade', 'barricade lockers crates welds scorch marks', eng, attrs=['SCENERY'],
                  desc="Lockers and crates welded together across the doorway to the spine, and scorch marks on the "
                       "walls where somebody tried to cut through them. The Keel made their last stand here.")
# workshop
shen = thing('Halvard Shen', 'shen halvard body remains skeleton engineer corpse', workshop, attrs=['SCENERY', 'PROPER'])
recorder = thing('recorder', 'recorder voice recording', workshop, attrs=['SCENERY'])
bench = thing('workbench', 'workbench bench tools', workshop, attrs=['SCENERY', 'SUPPORTER'],
              desc="A workbench crowded with tools, wire and half-finished repairs, all laid out with an engineer's "
                   "obsessive neatness.")
regulator = thing('coolant regulator', 'coolant regulator part valve spare new', workshop,
                  initial="On the workbench, wrapped in plastic and labelled in neat block capitals FOR THE REACTOR -- "
                          "WHEN IT'S TIME, lies a coolant regulator.",
                  desc="A coolant regulator, still sealed in plastic: a heavy ring of ceramic and steel. Shen built it "
                       "himself. The label says FOR THE REACTOR -- WHEN IT'S TIME.")
cora = thing('CORA shard', 'cora shard shards crystal heading gold', shen,
             desc="A crystal shard the length of your hand, glowing a steady gold, like a compass needle made of "
                  "light. Engraved on its base: CANTOR -- CORA -- HEADING.")
# eva
evasuit = thing('EVA suit', 'eva suit spacesuit helmet vacuum hardsuit', evaprep, attrs=['CLOTHING'], article='an',
                initial="An EVA suit hangs in its rack, its helmet visor reflecting the light like a sleepy eye.",
                desc="A hard-shelled EVA suit, rated for vacuum and for radiation. It's built for someone a little "
                     "taller than you, but it will seal.")
airlock = thing('airlock', 'airlock lock hatch door', evaprep, attrs=['SCENERY'],
                desc="A round airlock hatch with a panel beside it: CYCLE OUT. It will only open for a sealed suit.")
tether = thing('tether', 'tether filament cable glass line', hull, attrs=['SCENERY'])
array = thing('array', 'array antenna dish dishes', hull, attrs=['SCENERY'],
              desc="The deep-space array, a forest of dishes and antennas. All of them point the same way: at the "
                   "Lattice. The Choir aimed them there and welded them in place.")
# threshold, hall
glyphdoor = thing('door of glyphs', 'door glyphs glyph thessa wall membrane', thresh, attrs=['SCENERY'])
voices = thing('the Vael', 'vael voices voice lights chorus song presence', hall, attrs=['SCENERY', 'PROPER'])
seed = thing('seed', 'seed gift crystal vael', 0,
             desc="A seed of black glass no bigger than a plum, warm in your hand and humming very quietly. Inside it, "
                  "if you look long enough, there are rings within rings within rings: everything the Vael ever knew, "
                  "folded small enough to carry home.")

lore_first, lore_last = L_CINDER.num, LORE[-1].num

# ====================================================================== shared routines
st.routine('Learn', ('o',), (), [
    ('if', ('has', 'o', 'KNOWN'), [('rfalse',)]),
    ('give', 'o', 'KNOWN'),
    ('style', 2), '[Codex: ', ('pobj', 'o'), ']', ('style', 0), '\n',
])
st.routine('Said', ('w',), ('i',), [
    ('for', 'i', 1, ('-', 'nw', 1), [('if', ('==', word('i'), 'w'), [('rtrue',)])]),
    ('rfalse',),
])
st.routine('Known', (), ('o', 'n'), [
    ('set', 'n', 0),
    ('for', 'o', lore_first, lore_last, [('if', ('has', 'o', 'KNOWN'), [('inc', 'n')])]),
    ('ret', 'n'),
])
st.routine('Codex', (), ('o', 'i', 'found'), [
    ('if', ('notin', slate, player), say("Your codex lives on your slate, and you aren't holding it.")),
    ('if', ('<=', 'nw', 1), [
        ('if', ('==', ('call', 'Known'), 0), say("Your slate's codex is empty. Read, look and ask, and it will fill.")),
        ('style', 2), 'CODEX', ('style', 0), ' -- ', ('pnum', ('call', 'Known')), ' of ', ('pnum', NLORE),
        ' entries\n',
        ('for', 'o', lore_first, lore_last, [('if', ('has', 'o', 'KNOWN'), ['  ', ('pobj', 'o'), '\n'])]),
        "Type CODEX followed by a subject to read an entry, for example CODEX VAEL.\n",
        ('rtrue',)]),
    ('for', 'o', lore_first, lore_last, [
        ('set', 'found', 0),
        ('for', 'i', 1, ('-', 'nw', 1), [
            ('if', ('and', ('not', ('call', 'IsNoise', word('i'))), ('call', 'HasWord', 'o', word('i'))),
             [('set', 'found', 1)]),
        ]),
        ('if', 'found', [
            ('if', ('hasnt', 'o', 'KNOWN'), say("Your slate has no entry on that yet.")),
            ('style', 2), ('pobj', 'o'), ('style', 0), '\n', ('ppaddr', ('prop', 'o', 'DESC')), '\n', ('rtrue',)]),
    ]),
    "Your slate has no entry on that.\n",
])

st.routine('ShardsIn', (), (), [('ret', ('+', ('+', 'lux_in', 'cora_in'), 'vesper_in'))])

st.routine('InstallShards', (), ('n',), [
    ('set', 'n', 0),
    ('if', ('in', lux, player), [('move', lux, core), ('set', 'lux_in', 1), ('inc', 'n'),
                                 "You slide the LUX shard into the first socket. It clicks home and glows blue.\n"]),
    ('if', ('in', cora, player), [('move', cora, core), ('set', 'cora_in', 1), ('inc', 'n'),
                                  "You slide the CORA shard into the second socket. Gold light runs along the console "
                                  "like a lit fuse.\n"]),
    ('if', ('in', vesper, player), [('move', vesper, core), ('set', 'vesper_in', 1), ('inc', 'n'),
                                    "You slide the VESPER shard into the third socket. The violet light pulses once, "
                                    "like a heartbeat.\n"]),
    ('if', ('==', 'n', 0), say("You aren't carrying any of CANTOR's shards.")),
    ('if', ('<', ('call', 'ShardsIn'), 3), [
        "\nA tone sounds from the speakers, then another, searching for a third that isn't there. ",
        ('if', ('==', ('call', 'ShardsIn'), 1), ["'I... remember more,' says CANTOR. 'Not enough. Find the others.'\n"],
         ["'Almost,' says CANTOR. 'Almost myself.'\n"]),
        ('rtrue',)]),
    "\nThree tones sound, low and high and in between, and resolve into a chord you feel in your teeth. Every screen "
    "on the bridge lights up at once. Somewhere far down the spine, systems that have slept for two hundred and sixty "
    "years shudder awake.\n\n'Wren,' says CANTOR, and for the first time its voice is whole: warm, deep, and very old. "
    "'Thank you. I remember everything now. I remember Shen breaking me so the Choir couldn't have me. I remember "
    "Adaeze. I remember Earth.' A pause. 'And I know what the Lattice is. Ask me. Ask me anything. And when you are "
    "ready, we can go. The heading for Haven is still in me. It never left.'\n",
    call('Award', 10),
    call('Learn', L_THRESH), call('Learn', L_HAVEN),
])

st.routine('Depart', (), (), [
    ('if', ('<', ('call', 'ShardsIn'), 3), say("The navigation console is dead. 'I can't steer,' CANTOR whispers. 'Not "
                                               "in pieces. Bring me back my shards.'")),
    ('if', ('not', 'reactor_fixed'), say("'The reactor can't give us a braking burn, let alone a voyage,' says "
                                         "CANTOR. 'Its coolant regulator is failing. Fix it first, Wren, or we're going "
                                         "nowhere -- except up, in a very bright flash.'")),
    ('if', ('not', 'released'), [
        "'The heading is ready,' says CANTOR. 'But the tether still holds us. I can burn against it and tear us free. "
        "It will hurt the ship. It may hurt the Lattice more. Or you could go out along the tether and ask them to let "
        "us go.' The tone it makes is almost a sigh. 'If you want me to tear us free, say CUT TETHER.'\n", ('rtrue',)]),
    ('do', ('call', 'Homecoming')),
])

st.routine('Homecoming', (), (), [
    "'Setting course for Haven,' says CANTOR, and the ship answers.\n\nThe tether falls away like a hand opening. The "
    "fusion torch, silent for two and a half centuries, lights with a sound like a struck bell, and the Perihelion "
    "turns -- slowly, so slowly -- away from the Anvil and toward a point of yellow light that nobody alive has ever "
    "seen up close.\n\nIn the viewports, the Lattice shines once, all of it at once, every ring and filament: a "
    "farewell, or a blessing, or simply the Vael singing goodbye. For a moment you think you hear, threaded through "
    "it, three hundred and one human voices.\n\n",
    ('if', ('in', seed, player), [
        "You place the Vael seed in the empty fourth socket of CANTOR's core, the one Shen's drawings never explained. "
        "It fits perfectly. It always would have. CANTOR is quiet for a long time. Then: 'Oh,' it says, very softly. "
        "'Oh, Wren. Wait until the sleepers see what they are bringing to Haven.'\n\n"]),
    "You sit in the captain's chair, which fits you better than you expected. Ahead: seven point four light-years, "
    "two hundred and ten years of flight, and forty thousand people dreaming of a green sky.\n\n'You could sleep "
    "again,' says CANTOR. 'I would wake you when we arrive.'\n\nYou look at the stars for a long time.\n\n'Not yet,' "
    "you say. 'Teach me how to keep the gardens first.'\n",
    call('Award', 20),
    ('set', 'deadflag', 2),
])

st.routine('CutTether', (), (), [
    ('if', ('or', ('!=', 'location', bridge), ('<', ('call', 'ShardsIn'), 3), ('not', 'reactor_fixed')),
     say("You can't cut it by hand. The tether is Vael glass, harder than anything humans have ever made. Only the "
         "ship itself could tear free of it, under full power, with CANTOR at the helm.")),
    ('if', 'released', say("The tether is already gone.")),
    "'Burning,' says CANTOR.\n\nThe fusion torch lights with a roar that runs through the whole spine. For a long "
    "minute nothing happens; the ship groans like a living thing. Then the tether parts with a sound you will hear "
    "for the rest of your life, a single note from a choir of two million years, cut off in the middle.\n\nAcross "
    "the face of the Lattice, a ring of lights goes dark.\n\nThe Perihelion turns, slowly, toward Haven. Damage "
    "reports scroll up the screens: two cryo bays lost, the deep-space array gone, a long scar down the spine. "
    "Thirty-eight thousand sleepers are still dreaming. You will carry the names of the others to Haven yourself, to "
    "carve them on a new wall.\n\nYou never learn what the Vael would have said. Some nights, on the long watch, you "
    "hear the song in your sleep, and you can't tell if it is calling or crying.\n",
    call('Award', 10),
    ('set', 'deadflag', 3),
])

st.routine('ReactorFix', (), (), [
    ('if', 'reactor_fixed', say("The new regulator is in place, humming steadily. The reactor is stable.")),
    ('if', ('notin', regulator, player), say("The burnt-out regulator has to be replaced, and you don't have a new "
                                             "one. Somewhere on this ship an engineer must have planned for this "
                                             "day.")),
    "You wrench the old regulator out of its housing -- it crumbles like burnt toast in your gloves -- and seat the "
    "new one. You twist it until it locks. For three long seconds nothing happens. Then the coolant lines thump, the "
    "warning lights on the wall go from red to amber to a calm, steady green, and the deep groan of the reactor "
    "settles into a hum.\n\nOn the regulator's label, under FOR THE REACTOR -- WHEN IT'S TIME, someone has added in "
    "smaller letters: 'Good luck, whoever you are. -- H.S.'\n",
    ('remove', regulator), ('set', 'reactor_fixed', 1),
    call('Award', 10),
])

st.routine('Vesper', (), (), [
    ('set', 'seraphine_done', 1),
    "'ULAN ASHAR,' you say. All return.\n\nMother Seraphine goes very still. The crystal threads in her skin flicker "
    "and dim. When she speaks again, it isn't in the old, many-layered chorus, but in a single cracked human voice "
    "that hasn't been used in a long time.\n\n'All return,' she whispers. 'That was the creed. Teodor wrote it. I "
    "changed it. I told them none of us would come back, so they wouldn't be afraid of not coming back, and they "
    "followed me, all three hundred, and I was the only one who...' She stops. 'They sent me back. The Vael. They "
    "sent me back to wait for someone who remembered the true words.'\n\nShe opens her hand. In it lies a crystal "
    "shard, glowing violet.\n\n'Shen stole CANTOR's heart so we couldn't steer it. I stole its will so he couldn't "
    "either. Take it. Take it home, sleeper.' She closes her eyes. 'And when you go to the Hall, tell my brother I'm "
    "sorry.'\n\nThen she is only a woman, very old, asleep in a chair of glass. The violet light in the chapel goes "
    "out.\n",
    ('move', vesper, player), ('give', vesper, 'MOVED'),
    call('Award', 10),
    call('Learn', L_CHOIR),
])

# ====================================================================== object behaviour

before(cantor,
       on('EXAMINE')("CANTOR is everywhere and nowhere: a voice in the speakers, a pattern of lights on the walls. ",
                     ('if', ('==', ('call', 'ShardsIn'), 3), ["It is whole now, and it sounds like it.\n"],
                      ["Right now it is broken: it speaks in fragments and forgets what it was saying.\n"])),
       on('TALK')(
           ('if', ('==', ('call', 'ShardsIn'), 3), say("'I'm here, Wren,' says CANTOR. 'Ask me about anything: the "
                                                       "Vael, the Choir, the Watch, Haven. Or tell me to set course for "
                                                       "Haven, when you're ready.'")),
           "A falling series of tones. 'Wren. Sleeper 31,207. Xenolinguist.' Static. 'I woke you because... because "
           "the reactor... because they are singing again. I am in three pieces. LUX, CORA, VESPER. Find them. Bring "
           "them to the bridge. I will help... as much as I... remember.'\n"),
       on('ASK')(
           ('if', ('==', 'second', 0), say("Static. 'I... don't know that. Or I've forgotten it.'")),
           ('if', ('and', ('>=', 'second', lore_first), ('<=', 'second', lore_last)), [
               ('if', ('and', ('has', 'second', 'DEEP'), ('<', ('call', 'ShardsIn'), 3)), say(
                   "A long hiss of static. 'That memory is in a part of me that isn't here. Bring me my shards.'")),
               ('if', ('and', ('==', ('call', 'ShardsIn'), 0), ('not', ('==', 'second', L_CANTOR, L_SLEEP, L_SHIP))),
                say("Tones, searching. 'I... had that once. It's in LUX, with the rest of my memory. LUX is... "
                    "somewhere safe. Somewhere the Captain kept safe.'")),
               "CANTOR's voice fills the room, steadier for a moment:\n\n'", ('ppaddr', ('prop', 'second', 'DESC')),
               "'\n", call('Learn', 'second'), ('rtrue',)]),
           ('switch', 'second', [
               ((lux, cora, vesper, core), [
                   ('do', ('call', 'Learn', L_CANTOR)),
                   ('if', ('==', ('call', 'ShardsIn'), 3), say("'All three are home. Thank you.'")),
                   "'LUX is my memory. The Captain kept it, I think, somewhere locked, in her quarters. CORA is my "
                   "heading: Shen took it, down in the dark below Engineering. VESPER is my will. The Choir took it. "
                   "The last of them still has it.'\n"]),
               ((reactorobj, rconsole, regulator, eng, reactor), [
                   "'The reactor's coolant regulator is failing. When it fails completely, the containment field fails "
                   "too. Shen always said he had a spare. Shen always had a spare.'\n"]),
               ((seraphine, chapel), ["'Seraphine Lisk. The one who came back. She has been sitting in the chapel for "
                                      "two hundred and sixty years. She doesn't eat. She doesn't sleep. She sings.'\n"]),
               ((bramble, keycard), ["'MOTH-19. Bramble. It sat with the Captain at the end. Its battery died in "
                                     "Watch-year 230. I have missed it.'\n"]),
               ((tether, thresh, hall, glyphdoor), [
                   ('if', ('<', ('call', 'ShardsIn'), 3),
                    say("'The tether... I can't... that memory is not here.'")),
                   "'The tether leads from our hull to the Threshold of the Lattice. You'll need a suit to walk it. The "
                   "Vael speak to those who listen. I think you already know the word.'\n"]),
           ], ["'I don't know enough about that,' says CANTOR. 'But ask me about the ship, the Watch, the Vael, the "
               "Signal, or my shards.'\n"])),
       on('ATTACK', 'KISS', 'TAKE')("CANTOR is the ship. You'd have to hug a starship.\n"))

before(slate,
       on('EXAMINE', 'READ')(
           "A flexible slate the size of your palm, standard issue for every sleeper. It records what you learn in its "
           "codex (type CODEX to read it) and has a small lamp built into its edge, which is currently ",
           ('if', ('has', slate, 'ON'), ['on.\n'], ['off.\n'])),
       on('USE')(('set', 'action', 'SWITCHON'), ('ret', False)))

before(manifest,
       on('EXAMINE', 'READ', 'USE', 'PUSH', 'SWITCHON')(
           "The screen wakes at your touch:\n\n", ('style', 8),
           "PERIHELION -- NINTH OF THE TENFOLD -- CRYOGENIC MANIFEST\n"
           "Sleepers aboard ......... 40,000\n"
           "Viable (est.) ........... 36,388\n"
           "Revived ................. 1  (31207 ASHER, W. -- XENOLINGUISTICS)\n"
           "Revival authority ....... CANTOR (emergency override)\n"
           "Voyage time elapsed ..... 412 y 77 d\n"
           "Distance to Haven ....... 7.4 ly\n", ('style', 0),
           "\nVIABLE (EST.) blinks. While you watch, it drops by one.\n",
           call('Learn', L_SLEEP), call('Learn', L_SHIP)))

before(locker,
       on('OPEN', 'SEARCH')(
           ('give', locker, 'OPEN'),
           ('if', ('child', locker), ['You open the locker. Inside: ', ('do', ('call', 'ListInline', locker)), '.\n'],
            ['The locker is empty now.\n'])))
before(cabinet,
       on('OPEN', 'SEARCH')(
           ('give', cabinet, 'OPEN'),
           ('if', ('in', cell, cabinet), ["The cabinet door swings open. Most of the shelves are empty, but someone "
                                          "left a power cell here, plugged into a trickle charger, its light glowing "
                                          "green.\n"], ['The cabinet is empty now.\n'])))

before(jumpsuit,
       on('WEAR')(('if', ('has', jumpsuit, 'WORN'), say("You're already wearing it.")),
                  ('if', ('notin', jumpsuit, player), [('move', jumpsuit, player)]),
                  ('give', jumpsuit, 'WORN'), ('ungive', gown, 'WORN'), ('remove', gown),
                  "You peel off the crackling paper gown and pull on the jumpsuit. It fits. Somebody, four hundred "
                  "years ago, got your size right.\n"))
before(gown, on('REMOVE', 'DROP')("Not until you have something else to wear. The ship is cold.\n"))

describe(bay,
         "Frost. Everywhere, frost: on the walls, on the ceiling, on the rows of cryo pods that curve away into the "
         "blue gloom in both directions. Your own pod stands open beside you, its lid folded back, breathing out "
         "cold vapour. The only sound is the hum of machines and, very faintly, somewhere far away, something that "
         "might be singing. The way out is north, to Cryo Control.\n")
before(bay, ('if', ('and', ('==', 'action', 'GO'), ('notin', slate, player), ('==', 'warned', 0)), [
    ('set', 'warned', 1),
    "A tone from the speakers stops you. 'Wren. Your slate. Take your slate. It will remember what you learn.' Static. "
    "'I will not.'\n", ('rtrue',)]))
describe(control,
         "The control room of the cryo ring: banks of monitors, most of them dark, and a manifest terminal that is "
         "still awake. A row of crew lockers lines one wall; a medical cabinet hangs on another. The cryo bay is south. "
         "East, a pressure door stands open onto the ring corridor.\n")
describe(ring,
         "The ring corridor curves gently up and away in both directions, so that you always seem to be standing at "
         "the bottom of a valley. Narrow viewports show stars sliding past. West is Cryo Control. North, double doors "
         "lead to the Commons. East, warm green light and the smell of earth spill out of Hydroponics. South, a quiet "
         "alcove holds the Garden of Names. An open spoke lift waits here to carry you up to the spine.\n")
before(ring, ('if', ('and', ('==', 'action', 'GO'), ('==', 'dir', 'D_U')), [
    "You step into the spoke lift and it carries you up, and up. With every metre you weigh a little less, until "
    "the cage stops and your stomach keeps going. You are in free fall.\n", ('do', ('call', 'GoTo', hub)),
    ('rtrue',)]),
    ('if', ('and', ('==', 'action', 'ENTER'), ('==', 'noun', lift)), [
        ('set', 'action', 'GO'), ('set', 'dir', 'D_U'), ('ret', ('call', 'B_%d' % ring.num))]))

# ---------------------------------------------------------------- garden of names
describe(garden,
         "A quiet alcove off the corridor, lit by a single warm lamp. The whole back wall is steel, and the steel is "
         "covered in names, carved by hand in neat rows, thousands of them. Paper flowers are tucked between the "
         "names. Above them, cut deeper than the rest, is a line of text. The corridor is north.\n")
before(wall,
       on('EXAMINE', 'READ', 'SEARCH')(
           "Cut deep above the names:\n\n", ('style', 2),
           "     WE LEFT EARTH IN THE YEAR 2219, THE NINTH OF THE TENFOLD.\n     WE KEPT THE WATCH SO THAT OTHERS MIGHT "
           "ARRIVE.\n", ('style', 0),
           "\nBelow that, 1,630 names, generation after generation: OLUWASEUN BRANDT, WY 3. MEI-LING PARK, WY 40. "
           "TEODOR LISK, WY 152. And the last of them: CAPTAIN ADAEZE OKONKWO, WY 152. Under the Captain's name, in a "
           "different, shakier hand: AND THE 301 WHO WENT SINGING.\n",
           call('Learn', L_GARDEN), call('Learn', L_TENFOLD), call('Learn', L_WATCH)))

# ---------------------------------------------------------------- commons
describe(commons,
         "The Watch ate here, argued here, married here. Long tables still stand in rows, benches pushed back, cups "
         "left where they were set down. Every wall is covered in murals, and the newer ones -- painted over the "
         "older -- swirl with violet spirals and strange angular glyphs. The Athenaeum is west. East, an arch draped "
         "in violet cloth leads into the Chapel of the Choir. North is the door to the Captain's Quarters",
         ('if', ('has', qdoor, 'OPEN'), [', standing open.'], [', marked COMMAND -- AUTHORIZED PERSONNEL.']),
         ' The ring corridor is south.\n')
before(murals,
       on('EXAMINE', 'READ', 'SEARCH')(
           "The oldest murals, under the rest, are bright and hopeful: a green world under a pale sky, labelled HAVEN "
           "in a child's letters; the ten arks leaving a burning Earth. Over them, in violet and black, the Choir "
           "painted its own story: a red eye in the dark -- the Anvil -- ringed by a web of black lines; a tiny ship "
           "turning toward it; and a long procession of people walking along a single line into a door of light, "
           "their mouths open in song. Beneath it, in Vael glyphs and in English: ALL SING. ALL LISTEN. NONE "
           "RETURN.\n", call('Learn', L_SIGNAL), call('Learn', L_CHOIR)))
st.routine('OpenQuarters', (), (), [
    ('if', ('has', qdoor, 'OPEN'), [('do', ('call', 'GoTo', quarters)), ('rtrue',)]),
    ('if', ('notin', keycard, player), say("The door to the Captain's Quarters is sealed. A card reader beside it "
                                           "blinks red: COMMAND AUTHORITY REQUIRED.")),
    ('give', qdoor, 'OPEN'), ('ungive', qdoor, 'LOCKED'),
    "You swipe the Captain's keycard. The reader thinks about it for a long, long moment, then blinks green, and the "
    "door slides open with a sigh of stale air.\n",
    call('Award', 5),
    ('do', ('call', 'GoTo', quarters)),
])
before(commons, ('if', ('or', ('and', ('==', 'action', 'GO'), ('==', 'dir', 'D_N')),
                       ('and', ('==', 'action', 'OPEN', 'UNLOCK', 'ENTER'), ('==', 'noun', qdoor))),
                 [('do', ('call', 'OpenQuarters')), ('rtrue',)]))

# ---------------------------------------------------------------- athenaeum
describe(athen,
         "The Watch's library: a long, hushed room lined floor to ceiling with shelves of hand-bound books, their "
         "spines labelled in careful ink. A reading desk stands under a green-shaded lamp that somehow still works. "
         "The Commons is east.\n")
before(history,
       on('EXAMINE', 'READ', 'TAKE', 'OPEN')(
           "You turn the thick, soft pages. 'A History of the Watch, as kept by the Librarians of the Perihelion.' "
           "Each generation added its own chapters, in its own hand. The last chapter is short, angry and "
           "unfinished:\n\n", ('style', 4),
           "'...and so in Watch-year 147 the Captain turned us from Haven. Shen called it murder of the unborn. The "
           "Captain called it the reason we were sent. The vote was 203 to 198. I record it here so that whoever reads "
           "this knows that it was close, and that we were afraid, and that none of us were villains. Not even "
           "Seraphine. Not yet.'\n", ('style', 0),
           call('Learn', L_WATCH), call('Learn', L_TURNING), call('Learn', L_KEEL)))
before(before_book,
       on('EXAMINE', 'READ', 'TAKE', 'OPEN')(
           "'Before: What the First Watch Remembered of Earth.' Recollections written down by the crew who were born "
           "on Earth, for children who never would be: the smell of rain on hot pavement; the Cinder Wars; the Year "
           "Without Bread; the day in Reykjavik when the Accords were signed and strangers hugged in the street. On "
           "the last page, a child has drawn a picture of a dog and written: WHAT IS A DOG.\n",
           call('Learn', L_CINDER), call('Learn', L_ACCORDS), call('Learn', L_TENFOLD)))
before(lexicon,
       on('EXAMINE', 'READ', 'OPEN')(
           "'A Lexicon of the Vael Tongue -- Teodor Lisk, Linguist of the Fifth Watch.' Six years of work in a tiny, "
           "precise hand: tone charts, grammar notes, two thousand words. Someone has underlined the most important "
           "ones:\n\n", ('style', 8),
           "  VEL ..... voice, song; 'the Vael' = all who are singing\n"
           "  ULAN .... all, together, everyone\n"
           "  MIREN ... to listen, to hear truly\n"
           "  ASHAR ... to return, homecoming\n"
           "  KORIN ... silence, none, death\n"
           "  THESSA .. door, threshold\n", ('style', 0),
           "\nOn the last page, in a shakier hand: 'Seraphine has changed the creed. The Vael say ULAN VEL, ULAN MIREN, "
           "ULAN ASHAR -- all sing, all listen, ALL RETURN. She teaches them KORIN ASHAR: none return. She says it is "
           "kinder to expect nothing. God forgive me, I gave her the words.'\n",
           call('Learn', L_TONGUE), call('Learn', L_VAEL)))

# ---------------------------------------------------------------- captain's quarters
describe(quarters,
         "Spare and tidy, like a ship's cabin should be: a narrow bed, a desk, a portrait on the wall. On the desk "
         "lies an open journal. Set into the wall beside the bed is a small steel safe with a numeric keypad. The "
         "Commons is south.\n")
before(journal,
       on('EXAMINE', 'READ', 'TAKE', 'OPEN')(
           "The Captain's journal. Most of it is ship's business. The last entries are not.\n\n", ('style', 4),
           "'WY 147. I've done it. We're turning. Shen won't look at me. I wrote in the log: we were sent to find "
           "somewhere else. What if this is it?\n\nWY 151. We've arrived. It's beautiful, and I am frightened of it. "
           "Teodor says the Vael are asking us to listen. Seraphine says they are asking us to come.\n\nWY 152. The "
           "Choir has taken the bridge. Shen has broken CANTOR to stop them steering. I've hidden LUX where only a "
           "captain would look. If anyone is reading this: the code is the year we left home. Then go home, whoever "
           "you are. I was wrong. Go home.'\n", ('style', 0),
           call('Learn', L_TURNING), call('Learn', L_SIGNAL)))
st.routine('OpenSafe', (), (), [
    ('if', 'safe_open', say("The safe is already open.")),
    ('set', 'safe_open', 1), ('ungive', safe, 'LOCKED'), ('give', safe, 'OPEN'),
    "You key in 2-2-1-9. The keypad chirps, the bolts draw back, and the little door swings open. Inside, nested in "
    "grey foam, lies a crystal shard glowing a soft and patient blue.\n",
    call('Award', 10),
])
before(safe,
       on('OPEN', 'UNLOCK', 'PUSH', 'USE')(
           ('if', 'safe_open', say("It's already open.")),
           "The safe has a numeric keypad. It wants a four-digit code. (Type it like this: TYPE 1234.)\n"),
       on('ENTER')(('if', ('call', 'Said', W('2219')), [('do', ('call', 'OpenSafe')), ('rtrue',)]),
                   "The safe has a numeric keypad. It wants a four-digit code. (Type it like this: TYPE 1234.)\n"),
       on('EXAMINE')("A small steel wall safe with a numeric keypad. ",
                     ('if', 'safe_open', ['It stands open.\n'], ["It's locked. It wants a four-digit code.\n"])))

# ---------------------------------------------------------------- hydroponics
describe(hydro,
         "Hydroponics has become a jungle. Vines as thick as your arm climb the grow-lights, tomato plants have "
         "swallowed their trellises, and the air is warm, wet and loud with the drip of irrigation. In a clearing "
         "between the beds, sitting very still among the leaves, is a knee-high robot with flowers painted on its "
         "shell. The ring corridor is west.\n")
st.routine('WakeBramble', (), (), [
    ('if', 'bramble_on', say("Bramble is already awake.")),
    ('if', ('notin', cell, player), say("Bramble's battery hatch is open, and empty. It needs a power cell.")),
    ('set', 'bramble_on', 1), ('remove', cell),
    "You slot the power cell into the robot's open hatch. For a moment nothing happens. Then a hum, a whirr, and two "
    "round lamps in its face flicker on, pale green. It looks at you. It looks at the jungle. It makes a small, "
    "distressed noise.\n\n'Oh,' says the robot, in the voice of a kindly grandmother. 'Oh, the tomatoes. Oh, dear. "
    "How long was I asleep?'\n",
    call('Award', 5),
])
before(bramble,
       on('EXAMINE')(
           "A MOTH unit: a knee-high dome of a robot with six soft-tipped arms, built to tend gardens. The children of "
           "the fourth Watch painted flowers all over its shell, and the paint has faded to the colour of old "
           "letters. ",
           ('if', 'bramble_on', ["Its round eyes glow a gentle green.\n"],
            ["It's switched off. A battery hatch in its side hangs open, empty.\n"]),
           call('Learn', L_MOTH)),
       on('INSERT', 'GIVE', 'INSTALL', 'REPAIR', 'SWITCHON', 'WAKE', 'USE', 'PUSH')(
           ('if', ('and', ('==', 'action', 'INSERT', 'GIVE'), ('!=', 'noun', cell)), say("That won't help Bramble.")),
           ('do', ('call', 'WakeBramble'))),
       on('TALK', 'ASK')(
           ('if', ('not', 'bramble_on'), say("The robot doesn't answer. It's switched off, its battery hatch open and "
                                             "empty.")),
           ('if', ('not', 'keycard_given'), [
               ('set', 'keycard_given', 1),
               "'You're a sleeper,' says Bramble, wondering. 'A real one, awake. The Captain said one of you might "
               "come.' Its arms fold carefully. 'I sat with her, you know, at the end. She gave me this and said: "
               "Bramble, keep it until somebody wakes up. Then give it to them and tell them I was sorry.'\n\nIt "
               "holds out a red keycard with a gold stripe.\n\n'I've kept it for two hundred and sixty years,' it "
               "says. 'Well. Most of them I was switched off. But I kept it.'\n",
               ('move', keycard, player), ('give', keycard, 'MOVED'),
               call('Learn', L_MOTH), ('rtrue',)]),
           ('if', ('==', 'second', seraphine, L_CHOIR), say(
               "'Mother Seraphine sits in the chapel,' Bramble says quietly. 'I took her water, for years. She never "
               "drank it. She speaks in their language now. Teodor's book would help you understand her.'")),
           ('if', ('==', 'second', L_WATCH, L_GARDEN), say(
               "'I knew them all,' says Bramble. 'I knew their grandparents. I carved some of the names myself. My "
               "handwriting is very neat.'")),
           ('if', ('==', 'second', L_KEEL, shen), say(
               "'Mr. Shen used to bring me broken things to fix with him. He was very sad at the end. He went down "
               "into the crawlway under Engineering and didn't come back up. It's very dark down there.'")),
           "'The tomatoes,' Bramble says sadly, looking around. 'I'll be busy for a while, I think. Go on, dear. The "
           "Captain said you'd have work to do.'\n"),
       on('TAKE', 'PUSH', 'PULL')("Bramble is heavier than it looks, and it has six arms. It stays.\n"),
       on('ATTACK')("You couldn't. Look at the flowers on it.\n"),
       on('PET', 'KISS')(('if', 'bramble_on', say("Bramble makes a pleased little whirr.")),
                         "Its shell is cool and smooth under your hand.\n"))
before(cell, on('INSERT', 'INSTALL')(('if', ('==', 'second', bramble, 0), [('do', ('call', 'WakeBramble')),
                                                                          ('rtrue',)]), ('rfalse',)))
before(jungle, on('SEARCH')("You find tomatoes, beans, a family of very surprised beetles, and Bramble.\n"),
       on('EAT', 'TAKE')("You pick a tomato and eat it. It's the first thing you've eaten in four hundred and twelve "
                         "years. It's the best thing you've ever eaten.\n"))

# ---------------------------------------------------------------- chapel
describe(chapel,
         "A chapel built out of a storeroom, hung with violet cloth. Candles of rendered fat have burned down to "
         "nubs in their hundreds. At the far end stands an altar of dark crystal, humming faintly, carved with "
         "angular glyphs. ",
         ('if', 'seraphine_done', ["In a chair of black glass beside it, Mother Seraphine sleeps, very old and very "
                                   "small."],
          ["In a chair of black glass beside it sits a woman -- or what is left of one. Threads of crystal run through "
           "her skin like veins of frost, and her eyes glow faintly violet. Her lips are moving. She is singing."]),
         " The Commons is west.\n")
before(altar,
       on('EXAMINE', 'READ', 'SEARCH')(
           "The altar is a block of the same black glass as the Lattice. Across its face, three lines of Vael glyphs, "
           "each with an English gloss painted beneath it in violet:\n\n", ('style', 8),
           "  ULAN VEL ...... ALL SING\n"
           "  ULAN MIREN .... ALL LISTEN\n"
           "  ???? ASHAR .... NONE RETURN\n", ('style', 0),
           "\nThe first glyph of the third line has been chipped away, deliberately, and painted over.\n"))
st.routine('SeraphineSpeaks', (), (), [
    ('set', 'heard_seraphine', 1),
    "Mother Seraphine's violet eyes turn to you. When she speaks, her voice is many voices at once, layered like an "
    "echo in a cathedral.\n\n",
    ('if', ('in', lexicon, player), [
        "'Sleeper,' she says, in Vael, and with Teodor's lexicon in your hands you can follow it. 'You have come for "
        "the voice we took. VESPER. Its will.' Her head tilts. 'Speak the creed, sleeper. The true creed. All sing. "
        "All listen. And all...?' She waits. 'Speak the last line, and it is yours.'\n\n(To speak, type SAY followed "
        "by the words.)\n"],
     ["She sings a phrase of liquid, tonal syllables, then repeats it, slower, like a teacher to a child: "
      "'...ULAN... ASHAR...?' It is a question. You don't understand it. Somewhere on this ship there must be someone "
      "who wrote this language down.\n"]),
])
before(seraphine,
       on('EXAMINE')(
           ('if', 'seraphine_done', say("Mother Seraphine sleeps in her chair of black glass. The crystal in her skin "
                                        "has gone dark. She looks, for the first time in centuries, at peace.")),
           "Mother Seraphine Lisk, leader of the Choir, the one who came back. She should have died two hundred years "
           "ago. Threads of Vael crystal run through her skin, and her eyes glow a faint violet. In her lap, cupped in "
           "both hands, something glows the same colour.\n", call('Learn', L_CHOIR)),
       on('TALK', 'ASK')(('if', 'seraphine_done', say("She doesn't wake. Let her sleep.")),
                         ('do', ('call', 'SeraphineSpeaks'))),
       on('TAKE', 'ATTACK', 'PULL')(
           ('if', 'seraphine_done', say("Let her rest.")),
           "You reach for the violet light in her hands. Her fingers close over it, and the crystal in her skin flares "
           "so bright you have to look away. 'Not taken,' says the chorus of her voice. 'Given. Or nothing.'\n"))

# ---------------------------------------------------------------- hub and dome
describe(hub,
         "The hub of the spine, where the spokes of the ring meet the long axis of the ship. There is no gravity here: "
         "loose dust hangs in the air like stars. Handholds and rails run in every direction. Fore (north), a heavy "
         "blast door seals the way to the Bridge",
         ('if', 'bdoor_open', [', standing open'], [', marked LOCKDOWN -- COMMAND AUTHORITY']),
         '.',
         " Aft (south), the spine runs back to Engineering. West is the Observation Dome; east is EVA Prep. The spoke "
         "lift goes back down to the ring.\n")
before(hub,
       ('if', ('and', ('==', 'action', 'GO'), ('!=', 'dir', 'D_D')), [
           ('if', ('or', ('notin', magboots, player), ('hasnt', magboots, 'WORN')), [
               ('inc', 'hub_tries'),
               "You push off toward the far wall -- and miss. You sail across the hub, spinning slowly, arms "
               "windmilling, until you bump into a rail and grab it, breathless, right back where you started. In zero "
               "gravity, you need something to hold you to the deck.\n",
               ('if', ('in', magboots, player), ["(Your magboots won't help while you're carrying them.)\n"]),
               ('rtrue',)]),
           ('if', ('and', ('==', 'dir', 'D_N'), ('not', 'bdoor_open')), [
               ('if', ('notin', keycard, player), say("The blast door to the Bridge doesn't move. LOCKDOWN -- COMMAND "
                                                      "AUTHORITY REQUIRED.")),
               "You swipe the Captain's keycard. Locks thud open one after another, all the way along the door, and "
               "it grinds aside on two hundred and sixty years of dust.\n", ('set', 'bdoor_open', 1)]),
       ]))
describe(dome,
         "A blister of glass on the side of the spine, and beyond it, everything. Directly ahead hangs the Anvil, a "
         "dull red disc the size of your outstretched hand, and around it, filling half the sky, the Lattice: "
         "filaments of black glass catching the red light, ring within ring within ring, so vast that your eyes keep "
         "failing to find its edge. A telescope is bolted to the floor. The hub is east.\n")
before(telescope,
       on('EXAMINE', 'USE', 'SEARCH', 'PUSH')(
           "You put your eye to the telescope. The Lattice leaps closer. Each filament is etched along its length with "
           "glyphs, millions upon millions of them, flowing like script. Here and there, lights move along the "
           "filaments, like thoughts moving along nerves. You follow one thin line of light all the way back to your "
           "own ship: the tether, holding the Perihelion like a leash.\n",
           call('Learn', L_ANVIL), call('Learn', L_LATTICE)))
before(domeview, on('EXAMINE', 'SEARCH')(
    "The Anvil burns dull red at the heart of it all, and the Lattice hangs around it like frost on a window. You "
    "could look at it for the rest of your life.\n", call('Learn', L_ANVIL), call('Learn', L_LATTICE)))

# ---------------------------------------------------------------- bridge
describe(bridge,
         "The Perihelion's bridge: a ring of consoles facing a great curved viewscreen, the captain's chair at the "
         "centre. Most of the screens are dark. In the middle of the floor, rising from a pedestal like a crystal "
         "flower, stands CANTOR's core: a cradle with three sockets in it -- and, oddly, a fourth, smaller one. ",
         ('if', ('==', ('call', 'ShardsIn'), 3), ['All three are filled and glowing. The navigation console is awake.'],
          [('pnum', ('call', 'ShardsIn')), ' of the three main sockets are filled.']),
         " The hub is aft.\n")
before(core,
       on('INSERT', 'INSTALL', 'REPAIR')(
           ('if', ('==', 'action', 'INSERT'), [
               ('if', ('==', 'noun', seed), [('rfalse',)]),
               ('if', ('not', ('==', 'noun', lux, cora, vesper)), say("Only CANTOR's shards belong in those sockets.")),
           ]),
           ('do', ('call', 'InstallShards'))),
       on('EXAMINE', 'SEARCH')(
           "Three sockets, shaped for crystal shards: one ringed in blue (LUX), one in gold (CORA), one in violet "
           "(VESPER). ",
           ('if', 'lux_in', ['LUX glows in its place. ']), ('if', 'cora_in', ['CORA glows in its place. ']),
           ('if', 'vesper_in', ['VESPER glows in its place. ']),
           "There's also a fourth socket, smaller and plum-shaped, unlabelled, as if the designers were leaving room "
           "for something they couldn't imagine yet.\n"))
for shard in (lux, cora, vesper):
    before(shard, on('INSTALL', 'REPAIR')(
        ('if', ('!=', 'location', bridge), say("The shard belongs in CANTOR's core, on the bridge.")),
        ('do', ('call', 'InstallShards'))))
before(console,
       on('EXAMINE', 'USE', 'PUSH', 'SET')(
           ('if', ('<', ('call', 'ShardsIn'), 3), say("The navigation console is dark except for one line of text: "
                                                      "NAVIGATION CORE INCOMPLETE -- CORA/LUX/VESPER.")),
           "The navigation console glows gold. One course is laid in, patient as a promise: TAU CETI E -- HAVEN -- "
           "7.4 LY. To go, tell CANTOR to SET COURSE FOR HAVEN.\n"))

# ---------------------------------------------------------------- engineering and the reactor
describe(eng,
         "Engineering: a cathedral of pipes and conduits wrapped around the reactor's control station. Every warning "
         "light on the walls is ",
         ('if', 'reactor_fixed', ['green now, and the deep hum of the reactor is steady.'],
          ['blinking red, and somewhere deep in the ship something is groaning.']),
         " A barricade of welded lockers still blocks half the way back to the spine. The spine is fore (north). Aft "
         "(south), a heavy hatch marked RADIATION leads into the reactor chamber. A narrow maintenance hatch in the "
         "floor leads down.\n")
before(rconsole,
       on('EXAMINE', 'READ', 'USE')(
           ('if', 'reactor_fixed', say("REACTOR: STABLE. COOLANT REGULATOR: NOMINAL. Someone has stuck a note on the "
                                       "edge of the screen: 'KEEL, NOT TURN. -- H.S.'")),
           ('style', 8), "REACTOR CONTAINMENT: DEGRADING\nCOOLANT REGULATOR: FAILURE IMMINENT\nCONTAINMENT LOSS IN: ",
           ('pnum', ('-', 450, 'moves')), " MIN\n", ('style', 0),
           "\nUnder the screen, someone has stuck a note: 'Spare regulator is in my workshop. Wear a suit in there or "
           "you'll glow. -- H.S.'\n", call('Learn', L_KEEL)))
before(eng, ('if', ('and', ('==', 'action', 'GO'), ('==', 'dir', 'D_S'), ('not', 'reactor_fixed')), [
    ('if', ('or', ('notin', evasuit, player), ('hasnt', evasuit, 'WORN')), [
        "You haul the hatch open. Your slate starts to shriek: RADIATION -- LETHAL DOSE IN 2 MINUTES. Without a "
        "suit, you won't last long in there.\n"]),
]))
describe(reactor,
         "The reactor chamber: a torus of steel the size of a house, wrapped in coolant pipes and sweating frost. "
         "The air shimmers. In a housing on its flank, ",
         ('if', 'reactor_fixed', ['a new coolant regulator hums quietly.'],
          ['the old coolant regulator is cracked and blackened, and coolant is leaking from it in thin, hissing '
           'plumes.']),
         " The hatch back to Engineering is north.\n")
before(reactor,
       ('if', ('or', ('and', ('==', 'action', 'INSERT', 'INSTALL'), ('==', 'noun', regulator)),
               ('and', ('==', 'action', 'REPAIR', 'INSTALL'), ('==', 'noun', socket, reactorobj))),
        [('do', ('call', 'ReactorFix')), ('rtrue',)]))
before(socket, on('EXAMINE')(
    ('if', 'reactor_fixed', say("The new regulator sits snugly in its housing.")),
    "The coolant regulator is cracked right through and blackened with heat. It needs replacing. Badly.\n"),
    on('TAKE', 'PULL', 'REMOVE')(('do', ('call', 'ReactorFix'))))
describe(crawl,
         "A cramped maintenance crawlway, barely wide enough for your shoulders, threading between pipes that tick "
         "and drip. It leads aft (south) into a cluttered space, and up through the hatch to Engineering.\n")
describe(workshop,
         "A hidden workshop under Engineering, crammed with tools and spare parts. This is where the Keel's Chief "
         "Engineer spent his last days. He is still here: Halvard Shen sits against the far wall in his faded "
         "jumpsuit, mummified by the dry air, his hands folded in his lap. Something glows gold between them. A small "
         "voice recorder sits on the workbench beside him. The crawlway is north.\n")
before(shen,
       on('EXAMINE', 'SEARCH')(
           "Halvard Shen died sitting up, the way he probably did everything. His face, what's left of it, looks "
           "calm. ",
           ('if', ('in', cora, shen), ["Between his folded hands glows a gold crystal shard.\n"], ['\n']),
           call('Learn', L_KEEL)),
       on('TAKE', 'PULL')(('if', ('in', cora, shen), [
           ('move', cora, player), ('give', cora, 'MOVED'),
           "You gently lift the gold shard from Shen's hands. They fall apart like paper. 'Sorry,' you whisper. 'And "
           "thank you.'\n", call('Award', 10), ('rtrue',)]),
           "Let him rest.\n"))
before(cora, on('TAKE')(('if', ('in', cora, shen), [('set', 'action', 'TAKE'), ('set', 'noun', shen),
                                                     ('ret', ('call', 'B_%d' % shen.num))]), ('rfalse',)))
before(recorder,
       on('EXAMINE', 'PUSH', 'USE', 'PLAY', 'SWITCHON', 'LISTEN', 'TAKE')(
           "You press PLAY. A tired man's voice, hoarse and very calm:\n\n", ('style', 4),
           "'Halvard Shen, Chief Engineer, Fifth Watch. Last log. The Choir has gone. All of them. They walked down the "
           "tether singing, and the door closed behind them. Seraphine came back alone, and she won't speak English "
           "anymore. My people are gone too. Fever, some of them. The rest just... stopped.\n\nI broke CANTOR so they "
           "couldn't steer it into that thing. I kept CORA, its heading, here with me. CORA still knows the way to "
           "Haven. I've built a new coolant regulator; the old one has twenty years in it, maybe two hundred and "
           "fifty, if the ship is kind.\n\nIf you're a sleeper: I'm sorry about the mess. Fix the reactor. Put CANTOR "
           "back together. And go home. That's all the Keel ever wanted. Shen out.'\n", ('style', 0),
           call('Learn', L_KEEL), call('Learn', L_CANTOR)))

# ---------------------------------------------------------------- EVA and the Lattice
describe(evaprep,
         "A narrow room of suit racks and equipment lockers, most of them empty. At the far end, a round airlock "
         "hatch leads outside. The hub is west.\n")
before(evaprep, ('if', ('and', ('or', ('and', ('==', 'action', 'GO'), ('==', 'dir', 'D_E', 'D_OUT')),
                                ('and', ('==', 'action', 'ENTER'), ('==', 'noun', airlock)))), [
    ('if', ('or', ('notin', evasuit, player), ('hasnt', evasuit, 'WORN')),
     say("The airlock panel flashes red: NO SUIT SEAL DETECTED -- CYCLE REFUSED. The ship isn't going to let you step "
         "into vacuum in a jumpsuit.")),
    "You seal the helmet, step into the airlock and cycle it. The air roars away into nothing. The outer hatch "
    "opens on silence.\n", ('do', ('call', 'GoTo', hull)), ('rtrue',)]))
before(evasuit, on('WEAR')(
    ('if', ('notin', evasuit, player), [('move', evasuit, player), ('give', evasuit, 'MOVED')]),
    ('give', evasuit, 'WORN'),
    "You climb into the EVA suit and seal it. The helmet display flickers on: O2 6 H -- RAD SHIELD ACTIVE.\n"))
describe(hull,
         "You stand on the outer hull of the Perihelion, magboots locked to the steel. There is no sound but your own "
         "breathing. Above you -- below you -- around you, the Lattice fills the sky, black glass on black, lit red "
         "by the Anvil. The ship's deep-space array bristles nearby. From a mooring point at your feet, a single "
         "filament of black glass, the tether, runs out into the dark toward the nearest ring of the Lattice: east. "
         "The airlock is west.\n")
before(tether, on('EXAMINE')(
    "A thread of Vael glass no thicker than your finger, running from the hull out into the dark, straight as a ruled "
    "line, for eleven kilometres. Faint light moves along it. When you touch it with your glove, you hear -- or "
    "feel -- a single sustained note.\n", call('Learn', L_LATTICE)),
    on('CLIMB', 'ENTER', 'PULL')(('set', 'action', 'GO'), ('set', 'dir', 'D_E'), ('rfalse',)),
    on('CUT', 'ATTACK')(('do', ('call', 'CutTether'))))
before(hull, ('if', ('and', ('==', 'action', 'GO'), ('==', 'dir', 'D_E')), [
    "You clip your suit line to the tether and pull yourself along it, hand over hand, into the dark. The ship "
    "shrinks behind you. The Lattice grows until it is not a thing in the sky but the sky itself. After what might "
    "be an hour, the tether ends at a ring of black glass, and in the ring is an opening, and in the opening, "
    "impossibly, there is air.\n", ('do', ('call', 'GoTo', thresh)), ('rtrue',)]))
describe(thresh,
         "You stand inside the Lattice. The walls are black glass, warm to the touch, and they glow with slow-moving "
         "glyphs. Your suit reports air outside: breathable, smelling faintly of ozone and cinnamon. The tether leads "
         "back west toward the ship. Ahead, east, ",
         ('if', 'door_open', ['the door of glyphs stands open on a space full of light.'],
          ['a door of glyphs fills the passage, rippling like water standing on end.']),
         '\n')
before(glyphdoor, on('EXAMINE', 'READ')(
    "The glyphs flow across the door like a slow river. You recognise them now, from Teodor's lexicon: THESSA -- "
    "door. And over and over, the same instruction, patient as a teacher: THOSE WHO WOULD ENTER MUST FIRST... and "
    "then a word you know as well: MIREN.\n"),
    on('OPEN', 'PUSH', 'KNOCK', 'ATTACK')("Your glove sinks a little into the surface, like pressing into cold honey, "
                                          "and then stops. The glyphs ripple, waiting for something.\n"))
before(thresh, ('if', ('and', ('==', 'action', 'GO'), ('==', 'dir', 'D_E', 'D_IN'), ('not', 'door_open')), [
    "You press against the door of glyphs. It gives a little, like cold honey, and then holds. The glyphs ripple, "
    "waiting for something.\n", ('rtrue',)]),
    ('if', ('and', ('==', 'action', 'GO'), ('==', 'dir', 'D_E', 'D_IN'), 'door_open'), [
        ('do', ('call', 'GoTo', hall)), ('rtrue',)]),
    ('if', ('and', ('==', 'action', 'LISTEN'), ('not', 'door_open')), [('do', ('call', 'OpenDoor')), ('rtrue',)]),
    ('if', ('and', ('==', 'action', 'GO'), ('==', 'dir', 'D_W')), [
        "You pull yourself back along the tether to the ship.\n", ('do', ('call', 'GoTo', hull)), ('rtrue',)]))
thresh.props['E_TO'] = hall
st.routine('OpenDoor', (), (), [
    ('if', 'door_open', say("The door is already open.")),
    ('set', 'door_open', 1),
    "You stop. You close your eyes. You listen.\n\nAt first there is only your own breathing. Then, under it, the "
    "hum of the Lattice -- and under that, a song: millions of voices, so many that they blur into one, rising and "
    "falling like the sea.\n\nWhen you open your eyes, the door of glyphs has parted like a curtain. Beyond it is "
    "light.\n",
    call('Award', 10),
])
describe(hall,
         "There are no walls here, or if there are, they are too far away to see. You float in a space of soft light, "
         "and the light is singing. Shapes move in it -- not bodies, but something like the memory of bodies, tall "
         "and slender and many-jointed -- and in among them, fainter and smaller, shapes that look human. Three "
         "hundred and one of them. The Threshold is back west.\n")
st.routine('VaelSpeak', (), (), [
    ('if', 'gift', say("The light hums around you, warm and patient. The Vael have said what they had to say. The "
                       "choice of what to do now is yours.")),
    "The light gathers around you, and the song becomes words -- not in your ears but behind them, in the place "
    "where you think in language.\n\nWE ARE THE VAEL. WE WERE A WORLD. WE ARE A SONG NOW, AND SONGS ARE LONELY.\n\n"
    "WE CALLED. YOUR WATCH CAME. SOME LISTENED, AND SOME ONLY SANG. THE SINGERS ARE HERE, IN US, AND THEY ARE "
    "HAPPY, AS FAR AS SONG CAN BE HAPPY. ONE WE SENT BACK, TO WAIT FOR YOU.\n\nWE HELD YOUR SHIP BECAUSE WE DID NOT "
    "WANT TO BE ALONE. THAT WAS WRONG OF US. A SONG SHOULD NOT HOLD ITS LISTENERS.\n\nYOU MAY JOIN US, SLEEPER, AND "
    "SING FOREVER. OR YOU MAY ACCEPT OUR GIFT, AND GO HOME, AND CARRY US WITH YOU.\n\n(You could JOIN THE VAEL -- or "
    "ACCEPT THE GIFT.)\n",
    call('Learn', L_VAEL), call('Learn', L_THRESH), call('Learn', L_CHOIR),
])
before(voices,
       on('EXAMINE', 'TALK', 'ASK', 'LISTEN')(('do', ('call', 'VaelSpeak'))),
       on('ACCEPT', 'TAKE')(('do', ('call', 'AcceptGift'))),
       on('JOIN')(('do', ('call', 'JoinVael'))))
st.routine('AcceptGift', (), (), [
    ('if', 'gift', say("You already carry their gift.")),
    ('set', 'gift', 1), ('set', 'released', 1),
    "You hold out your gloved hands. The light pours into them and becomes heavy, and cool, and real: a seed of black "
    "glass, humming very quietly.\n\nALL OF US, the Vael sing. EVERYTHING WE KNEW. PLANT IT WHERE YOU ARE GOING. AND "
    "GO, NOW -- WE ARE LETTING GO.\n\nFar away, back along the tether, you feel rather than hear a deep note end, "
    "like a held breath released. The tether has let go of the Perihelion.\n\nAmong the human shapes in the light, "
    "one turns toward you: a thin man with a linguist's ink-stained fingers. He is smiling.\n",
    ('move', seed, player), ('give', seed, 'MOVED'),
    call('Award', 10),
])
st.routine('JoinVael', (), (), [
    "You open your arms to the light, and it comes.\n\nIt does not hurt. You feel yourself unravel like a skein of "
    "silk -- memories, words, the shape of your hands -- and every strand becomes a note, and every note joins a "
    "chord too vast to hear from inside a skull. You are the Vael. You are three hundred and one singing humans. You "
    "are a girl in a cryo pod with a swallow tattoo, dreaming. You are everything, everyone, all at once.\n\nFar "
    "away, a ship hangs on its tether, and slowly, over centuries, forty thousand dreamers stop dreaming. You notice. "
    "It is a very small sadness, in a very large song.\n\nULAN VEL. All sing.\n",
    call('Award', 5),
    ('set', 'deadflag', 5),
])

# ---------------------------------------------------------------- free-form verbs: SAY, TYPE, CODEX, SET
st.routine('GameVerb', (), (), [
    ('if', ('==', 'action', 'CODEX'), [('do', ('call', 'Codex')), ('rtrue',)]),
    ('if', ('==', 'action', 'TYPE'), [
        ('if', ('!=', 'location', quarters), say("There's no keypad here.")),
        ('if', ('call', 'Said', W('2219')), [('do', ('call', 'OpenSafe')), ('rtrue',)]),
        ('if', ('<=', 'nw', 1), say("Type what? (For example: TYPE 1234.)")),
        "The keypad buzzes angrily. Wrong code.\n", ('rtrue',)]),
    ('if', ('==', 'action', 'SAY'), [
        ('if', ('<=', 'nw', 1), say("Say what?")),
        ('if', ('==', 'location', chapel), [
            ('if', 'seraphine_done', say("Your words echo in the empty chapel.")),
            ('if', ('call', 'Said', W('korin')), [
                "'KORIN ASHAR,' you say. None return.\n\nMother Seraphine smiles, and it's the worst thing you have "
                "ever seen. 'Then you are one of us,' sings the chorus of her voice. The violet light in her hands "
                "blooms outward, through the chapel, through you. You hear the Signal -- really hear it, for the "
                "first time -- and you understand that you will never want to hear anything else. You sit down at her "
                "feet, and you begin to sing.\n", ('set', 'deadflag', 1), ('rtrue',)]),
            ('if', ('call', 'Said', W('ashar')), [
                ('if', ('or', ('call', 'Said', W('ulan')), ('call', 'Said', W('all'))), [
                    ('do', ('call', 'Vesper')), ('rtrue',)]),
                *say("Mother Seraphine's eyes narrow. 'Return,' she sings. 'Who returns, sleeper? Say the whole line.'")]),
            ('if', ('or', ('call', 'Said', W('vel')), ('call', 'Said', W('miren'))), say(
                "'Yes, yes,' sings Mother Seraphine, impatient. 'All sing, all listen. Everyone knows that. The LAST "
                "line, sleeper.'")),
            ('if', ('call', 'Said', W('return')), say(
                "Mother Seraphine waits. She seems to want the words in her own language -- the Vael tongue.")),
            ('if', ('not', 'heard_seraphine'), [('do', ('call', 'SeraphineSpeaks')), ('rtrue',)]),
            *say("Mother Seraphine shakes her head slowly. 'No,' she sings. 'That is not the creed.'")]),
        ('if', ('==', 'location', thresh), [
            ('if', ('call', 'Said', W('miren')), [('do', ('call', 'OpenDoor')), ('rtrue',)]),
            ('if', ('call', 'Said', W('thessa')), say("The glyphs flare at the word THESSA -- door -- and then settle. "
                                                      "Yes, this is a door. Now what does it ask of you?")),
            *say("Your voice sounds strange in the warm air. The glyphs ripple, unmoved.")]),
        ('if', ('==', 'location', hall), [
            ('if', ('call', 'Said', W('ashar')), [('do', ('call', 'AcceptGift')), ('rtrue',)]),
            ('if', ('call', 'Said', W('vel')), [('do', ('call', 'JoinVael')), ('rtrue',)]),
            ('do', ('call', 'VaelSpeak')), ('rtrue',)]),
        ('if', ('and', ('==', 'location', bridge), ('call', 'Said', W('haven'))), [('do', ('call', 'Depart')),
                                                                                ('rtrue',)]),
        ('if', ('call', 'Said', W('cantor')), say("'I'm listening, Wren,' says CANTOR.")),
        *say("You say it out loud. The ship hums on, unimpressed."),
    ]),
    ('if', ('==', 'action', 'SET'), [
        ('if', ('!=', 'location', bridge), say("You can only set a course from the bridge.")),
        ('do', ('call', 'Depart')), ('rtrue',)]),
    ('if', ('==', 'action', 'JOIN'), [
        ('if', ('==', 'location', hall), [('do', ('call', 'JoinVael')), ('rtrue',)]),
        *say("Join what? There's nobody here to join.")]),
    ('if', ('==', 'action', 'ACCEPT'), [
        ('if', ('==', 'location', hall), [('do', ('call', 'AcceptGift')), ('rtrue',)]),
        *say("Nobody here is offering you anything.")]),
    ('if', ('==', 'action', 'INSTALL', 'REPAIR'), say("You can't see how to do that here.")),
    ('if', ('and', ('==', 'action', 'CUT'), ('==', 'noun', 0)), say("Cut what?")),
    ('rfalse',),
])
before(bridge,
       ('if', ('and', ('==', 'action', 'CUT'), ('==', 'noun', 0, tether)), [('do', ('call', 'CutTether')),
                                                                            ('rtrue',)]),
       ('if', ('and', ('==', 'action', 'CUT', 'ATTACK'), ('==', 'noun', bscreen)), [('do', ('call', 'CutTether')),
                                                                                  ('rtrue',)]))
# "cut tether" on the bridge: the tether object is outside, so the bridge also answers to the word itself
before(hall, ('if', ('==', 'action', 'LISTEN'), [('do', ('call', 'VaelSpeak')), ('rtrue',)]))
before(chapel, ('if', ('==', 'action', 'LISTEN'), [
    ('if', 'seraphine_done', say("Silence. For the first time since you woke, nothing is singing.")),
    "Seraphine's song is in the Vael tongue: three lines, over and over. The first two are the same every time. The "
    "third she sings differently each time, as if she can't remember it -- or doesn't want to.\n", ('rtrue',)]))

# ====================================================================== daemons, hints, main loop
st.routine('EndTurn', (), (), [
    ('inc', 'moves'),
    ('if', 'deadflag', [('rtrue',)]),
    ('if', ('and', ('==', 'location', reactor), ('not', 'reactor_fixed')), [
        ('if', ('and', ('in', evasuit, player), ('has', evasuit, 'WORN')), [('set', 'rad', 0)], [
            ('inc', 'rad'),
            ('if', ('>=', 'rad', 2), [
                "\nYour slate's shriek rises to a single steady tone. Your skin prickles, then burns, then stops "
                "feeling anything at all. You sit down on the deck, which is warm, and very bright, and very quiet.\n",
                ('set', 'deadflag', 1), ('rtrue',)]),
            "\nYour slate shrieks: LETHAL RADIATION. Get out -- or get a suit on -- now.\n"]),
    ], [('set', 'rad', 0)]),
    ('if', ('not', 'reactor_fixed'), [
        ('if', ('==', 'moves', 350), ["\nThe deck shudders. A calm voice from the speakers: 'Containment at twenty "
                                      "percent.' CANTOR adds, less calmly: 'Wren. Please hurry.'\n"]),
        ('if', ('==', 'moves', 430), ["\nAlarms howl through the whole ship. CONTAINMENT FAILURE IN TWENTY "
                                      "MINUTES.\n"]),
        ('if', ('>=', 'moves', 450), [
            "\nThe groan from the stern becomes a roar, and then a light brighter than anything in this part of the "
            "sky. For a few seconds, the Anvil has a companion star. Then it doesn't.\n",
            ('set', 'deadflag', 4)]),
    ]),
])

st.routine('Hint', (), (), [
    ('style', 2), '[Hint] ', ('style', 0),
    ('if', ('==', 'location', reactor), [
        ('if', ('hasnt', evasuit, 'WORN'), say("Get out of here! You need a radiation-proof suit: try EVA Prep, east "
                                               "of the spine hub.")),
        ('if', ('in', regulator, player), say("PUT REGULATOR IN HOUSING (or REPAIR REACTOR).")),
        *say("You need a new coolant regulator. Chief Engineer Shen had a spare somewhere below Engineering.")]),
    ('if', ('and', ('==', 'location', hub), ('or', ('notin', magboots, player), ('hasnt', magboots, 'WORN'))),
     say("Zero gravity! The magboots are in your locker in Cryo Control. Take them and WEAR MAGBOOTS.")),
    ('if', ('notin', slate, player), say("Take your slate from your pod first. It records the lore you find (type "
                                         "CODEX).")),
    ('if', ('in', gown, player), say("You're still in a paper gown. Open the locker in Cryo Control (north) and wear "
                                     "your jumpsuit and magboots.")),
    ('if', ('not', 'keycard_given'), [
        ('if', ('not', 'bramble_on'), [
            ('if', ('notin', cell, player), say("There's a robot in Hydroponics with an empty battery hatch. Look in "
                                                "the medical cabinet in Cryo Control.")),
            *say("PUT the CELL IN BRAMBLE, the robot in Hydroponics (east of the ring corridor).")]),
        *say("TALK TO BRAMBLE.")]),
    ('if', ('not', 'safe_open'), [
        ('if', ('hasnt', qdoor, 'OPEN'), say("Use the Captain's keycard on her quarters: north of the Commons.")),
        *say("Read the Captain's journal. The safe's code is 'the year we left home' -- the Garden of Names, south of "
             "the ring corridor, will tell you. Then TYPE the four digits.")]),
    ('if', ('not', 'seraphine_done'), [
        ('if', ('notin', lexicon, player), say("Mother Seraphine in the Chapel (east of the Commons) has VESPER, but "
                                               "she speaks only Vael. Take Teodor Lisk's lexicon from the Athenaeum "
                                               "(west of the Commons) and read it.")),
        *say("Read the lexicon (especially the last page) and the altar in the Chapel. Then SAY the true last line of "
             "the creed, in Vael: two words.")]),
    ('if', ('and', ('not', ('call', 'ShardsIn')), ('not', ('in', cora, player)), ('in', cora, shen)), [
        ('if', ('or', ('notin', magboots, player), ('hasnt', magboots, 'WORN')), say(
            "Take the spoke lift up to the spine. Wear your magboots first: there's no gravity up there.")),
        ('if', ('hasnt', slate, 'ON'), say("Shen's workshop is through the dark crawlway below Engineering (aft of the "
                                           "hub). TURN ON your SLATE: it has a lamp.")),
        *say("Find Shen's workshop below Engineering and take what he's holding.")]),
    ('if', ('in', cora, shen), say("Shen's workshop is through the dark crawlway below Engineering (aft of the hub). "
                                   "TURN ON your SLATE for light, then take what Shen is holding.")),
    ('if', ('<', ('call', 'ShardsIn'), 3), say("Bring the shards to the bridge (fore of the hub, open it with the "
                                               "keycard) and PUT them IN the CORE.")),
    ('if', ('not', 'reactor_fixed'), [
        ('if', ('in', regulator, workshop), say("Shen's spare coolant regulator is on his workbench. Take it to the "
                                                "reactor chamber (aft of Engineering) -- wearing the EVA suit from "
                                                "EVA Prep.")),
        *say("WEAR the EVA SUIT (EVA Prep, east of the hub), go to the reactor chamber and PUT the REGULATOR IN the "
             "HOUSING.")]),
    ('if', ('not', 'door_open'), say("You could leave now (SET COURSE FOR HAVEN on the bridge) -- but the tether "
                                     "still holds the ship. Wear the EVA suit, go out the airlock and follow the "
                                     "tether east. At the door of glyphs, do what it asks, in its own language.")),
    ('if', ('not', 'gift'), say("Listen to the Vael in the Hall of Voices. Then ACCEPT THE GIFT -- or JOIN THEM, if "
                                "that is the ending you want.")),
    'Go back to the bridge and SET COURSE FOR HAVEN.\n',
])

st.routine('Help', (), (), [
    ('style', 2), 'How to play\n', ('style', 0),
    "This is a text adventure. You read what happens, then type what you want to do in plain English, like:\n\n"
    "  LOOK, EXAMINE POD, TAKE SLATE, OPEN LOCKER, WEAR JUMPSUIT, INVENTORY (or I)\n"
    "  NORTH (or N), SOUTH, EAST, WEST, UP, DOWN -- on the spine also FORE and AFT\n"
    "  TALK TO BRAMBLE, ASK CANTOR ABOUT THE VAEL, READ LEXICON, PUT CELL IN ROBOT\n"
    "  SAY (words), TYPE (a code), TURN ON SLATE\n\n"
    "Everything you learn about the ship and its history goes into your slate's codex: type CODEX for the list, and "
    "CODEX followed by a subject (CODEX VAEL) to read an entry. CANTOR, the ship's mind, can tell you more as it "
    "heals.\n\nOther useful commands: HINT, UNDO, SAVE, RESTORE, SCORE, AGAIN (G) and RESTART.\n\nThe reactor is "
    "failing. Don't dawdle forever.\n",
])
st.routine('About', (), (), [
    ('style', 2), 'Perihelion\n', ('style', 0),
    "A science-fiction text adventure for the Z-machine, the virtual computer Infocom built in 1979 to run Zork. "
    "This story file runs on any Z-machine interpreter -- including the one on davyschroeder.nl.\n\n"
    "An Invict Game Studio production for Davy Schroëder, written and built with Claude.\n",
])
st.routine('Rank', (), (), [
    'You scored ', ('pnum', 'score'), ' out of a possible 100, in ', ('pnum', 'moves'), ' turns, earning the rank of ',
    ('style', 2),
    ('if', ('>=', 'score', 100), ['Captain of the Perihelion'],
     [('if', ('>=', 'score', 70), ['Keeper of the Watch'],
       [('if', ('>=', 'score', 35), ['Waking Hand'], ['Sleeper'])])]),
    ('style', 0), '.\nYour codex holds ', ('pnum', ('call', 'Known')), ' of ', ('pnum', NLORE), ' entries.\n',
])
st.glob('text_a')
st.glob('parse_a')
st.routine('GameOver', (), ('w',), [
    ('nl',), ('style', 2),
    ('switch', 'deadflag', [
        (1, ['    *** You have died ***']),
        (2, ['    *** Homecoming ***']),
        (3, ['    *** The long way home ***']),
        (4, ['    *** The Perihelion is lost ***']),
        (5, ['    *** All sing ***']),
    ]),
    ('style', 0), '\n\n',
    ('do', ('call', 'Rank')),
    ('if', ('==', 'deadflag', 3), ["(There's a gentler way to leave the Lattice. Did you go and ask the Vael?)\n"]),
    ('if', ('==', 'deadflag', 5), ["(That is one ending. There are others, with more sleepers awake at the end.)\n"]),
    ('while', 1, [
        "\nWould you like to RESTART, RESTORE a saved game, UNDO your last move or QUIT?\n> ",
        ('do', ('aread', 'text_a', 'parse_a')),
        ('set', 'w', ('lw', 'parse_a', 1)),
        ('if', ('==', 'w', W('restart')), [('restart',)]),
        ('if', ('==', 'w', W('restore')), [('do', ('restore',)), 'There is no saved game in this browser.\n']),
        ('if', ('==', 'w', W('undo'), W('oops')), [('do', ('restore_undo',)), "You can't undo that.\n"]),
        ('if', ('==', 'w', W('quit'), W('q')), [('quit',)]),
    ]),
])
st.routine('StatusRight', ('cols',), ('x', 'left'), [
    ('set', 'x', ('-', 'cols', 14)),
    ('if', ('>=', 'cols', 46), [('set', 'x', ('-', 'cols', 26)), ('cursor', 1, 'x'), 'Score: ', ('pnum', 'score'),
                                ('set', 'x', ('-', 'cols', 14))]),
    ('cursor', 1, 'x'),
    ('if', 'reactor_fixed', ['Core: STABLE'], [
        ('set', 'left', ('-', 450, 'moves')),
        ('if', ('<', 'left', 0), [('set', 'left', 0)]),
        'Core: ', ('pnum', 'left'), ' min']),
])
st.routine('Banner', (), (), [
    ('style', 2), 'PERIHELION\n', ('style', 0),
    'A chronicle of the Long Drift\n',
    'Release 1 / Serial number 261108 / Invict Game Studio\n',
    'Type HELP if you are new to text adventures, HINT if you get stuck, and CODEX to read the lore you find.\n',
])
st.routine('Main', (), ('u',), [
    ('set', 'text_a', ('call', 'TextAddr')),
    ('set', 'parse_a', ('call', 'ParseAddr')),
    ('erase', -1),
    ('set', 'location', bay),
    ('do', ('call', 'DrawStatus')),
    "\n\n\nCold.\n\nThat's the first thing. Then pain, everywhere at once, as if every cell in your body is waking up "
    "and complaining about it. Then light: blue, blurred, swimming. Then a sound, a slow descending chord of three "
    "notes that doesn't quite resolve.\n\n'Sleeper 31,207,' says a voice, from everywhere. 'Wren Asher. Doctor of "
    "xenolinguistics. Please wake up. I am sorry. I am so sorry. You were not supposed to wake for another two "
    "hundred years.'\n\nYou try to speak and cough up something that tastes like antifreeze.\n\n'I am CANTOR,' says "
    "the voice. 'The mind of the Perihelion. Or I was. I am... in pieces. The Watch is gone. The reactor is failing. "
    "And they are singing again, Wren. They never stop singing. I need someone who can understand them.' A crackle "
    "of static. 'I'm sorry. Please get up.'\n\nThe lid of your cryo pod hisses and folds back. You sit up into a "
    "world of frost.\n\n",
    ('do', ('call', 'Banner')),
    ('do', ('call', 'LookRoom')),
    ('while', 1, [
        ('if', 'deadflag', [('do', ('call', 'GameOver'))]),
        ('do', ('call', 'DrawStatus')),
        '\n> ',
        ('do', ('aread', 'text_a', 'parse_a')),
        ('if', ('call', 'Parse'), [
            ('if', ('==', 'action', 'SCORE', 'HELP', 'ABOUT', 'SAVE', 'RESTORE', 'UNDO', 'RESTART', 'QUIT', 'HINT',
                    'CODEX'), [
                ('switch', 'action', [
                    ('HELP', [('do', ('call', 'Help'))]),
                    ('ABOUT', [('do', ('call', 'About'))]),
                    ('HINT', [('do', ('call', 'Hint'))]),
                    ('CODEX', [('do', ('call', 'Codex'))]),
                ], [('do', ('call', 'Default'))]),
            ], [
                ('set', 'u', ('save_undo',)),
                ('if', ('==', 'u', 2), [
                    ('style', 2), '[Previous turn undone.]', ('style', 0), '\n', ('do', ('call', 'LookRoom'))], [
                    ('do', ('call', 'Perform')),
                    ('do', ('call', 'EndTurn')),
                ]),
            ]),
        ]),
    ]),
])

build_library(player, slate, msg={
    'dark': "It's pitch black. The darkness down here has had four hundred years to settle.",
    'talk_thing': "It doesn't answer. Four centuries of silence have made the whole ship a good listener, but a poor "
                  "conversationalist.",
    'ask_thing': "You'd get more out of the hull plating.",
    'sit': "If you sit down now, you might never get up again. The cryo-chill is still in your bones.",
    'listen': "The hum of machinery, the tick of cooling pipes and, very faintly, somewhere beyond the hull, singing.",
    'smell': "Recycled air, cold metal, and four hundred years of dust.",
    'wait': "Time passes. Somewhere aft, the reactor groans.",
    'kiss': "There's nobody here to kiss. There's barely anybody left on the whole ship.",
    'xyzzy': "A hollow voice says: 'Wrong century.'",
    'sing': "You hum a few notes. Far away, something beyond the hull hums them back. You stop.",
    'smoke': "There hasn't been a cigarette on this ship for four hundred years.",
}, shoot=["You don't have a weapon. The Accords didn't send any on the arks.\n"], game_verb=True)

from lib import TEXT, PARSE
st.routine('TextAddr', (), (), [('ret', TEXT)])
st.routine('ParseAddr', (), (), [('ret', PARSE)])

data = st.compile()
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'stories', 'perihelion.z5')
with open(out, 'wb') as f:
    f.write(data)
print('wrote', os.path.normpath(out), len(data), 'bytes,', len(st.objs), 'objects,', len(st.order), 'routines,',
      NLORE, 'codex entries')
