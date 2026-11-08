"""The Blue Lantern Affair - a noir text adventure for the Z-machine.

Build:  python3 blue_lantern.py   (writes ../stories/blue-lantern.z5)
"""
import os
from lib import st, W, R, S, on, call, room, thing, before, describe, build_library

G = st.glob


def say(text):
    """Print text and stop the action (return true)."""
    return [text + '\n', ('rtrue',)]


for g in ['loaded', 'gus_paid', 'moose_ok', 'mirror_read', 'letter_read', 'key_found', 'got_roomkey', 'pruitt_awake',
          'piano_open', 'ledger_taken', 'rico_timer', 'rico_done', 'police_called', 'silas_ok', 'wh_seen',
          'eddie_free', 'climax', 'cat_petted']:
    G(g)

# ====================================================================== rooms
office = room('Decker Investigations', 'office',
              "Your office is two rooms' worth of trouble squeezed into one: a scarred oak desk with a single drawer, a "
              "filing cabinet that has seen better decades, a bentwood coat rack and a window streaked with rain. "
              "Across the street, a pawnshop's neon sign stutters PAWN... PAWN... PAWN, painting the room the colour "
              "of a fresh bruise. A telephone squats on the desk next to a bottle of rye. Your license hangs on the "
              "wall. The door leads out and down the stairs to Mercer Street.")
street = room('Mercer Street', 'mercer street',
              "Mercer Street at midnight: wet asphalt, overflowing gutters and neon bleeding into the puddles. The "
              "narrow door up to your office is here. East, blue light spills from beneath the striped awning of the "
              "Blue Lantern, along with the sound of a muted trumpet. West, the shabby front of the Calloway Hotel "
              "promises ROOMS BY THE NIGHT, WEEK OR REGRET. Harbor Road runs south toward the docks, and a narrow "
              "alley slips north between the buildings. Across the street, an oil stain and a cigarette butt mark "
              "where a car was idling a minute ago.")
club = room('The Blue Lantern', 'blue lantern club nightclub',
            )
dressing = room("Vivian's Dressing Room", 'dressing room backstage')
lobby = room('Calloway Hotel Lobby', 'calloway hotel lobby')
hallway = room('Third-Floor Hallway', 'hallway corridor')
room6 = room('Room 6', 'room 6 six')
fireesc = room('Fire Escape')
alley = room('Back Alley', 'alley')
harbor = room('Harbor Road', 'harbor road docks harbour')
gate = room('Pier 9 Gate')
pier = room('Pier 9', 'pier 9 nine')
warehouse = room('Warehouse 13', 'warehouse 13 thirteen', attrs=['DARK'])

office.props.update(D_TO=street, OUT_TO=street)
street.props.update(U_TO=office, IN_TO=office, E_TO=club, W_TO=lobby, S_TO=harbor, N_TO=alley)
club.props.update(W_TO=street, OUT_TO=street, N_TO=dressing)
dressing.props.update(S_TO=club, OUT_TO=club)
lobby.props.update(E_TO=street, OUT_TO=street, U_TO=hallway)
hallway.props.update(D_TO=lobby)
room6.props.update(W_TO=hallway, OUT_TO=fireesc)
fireesc.props.update(IN_TO=room6, W_TO=room6, D_TO=alley)
alley.props.update(S_TO=street, U_TO=fireesc, OUT_TO=street)
harbor.props.update(N_TO=street, E_TO=gate)
gate.props.update(W_TO=harbor, E_TO=pier)
pier.props.update(W_TO=gate, N_TO=warehouse, IN_TO=warehouse)
warehouse.props.update(S_TO=pier, OUT_TO=pier)

# ====================================================================== the player and props
player = thing('yourself', 'me myself self sam decker', office, attrs=['PROPER', 'CONCEALED'],
               desc="Sam Decker: forty-one years old, a nose that healed crooked and eyes that have seen too much of "
                    "Port Halcyon. You've looked better. You've also looked worse, usually on a Saturday.")
locket = thing('silver locket', 'silver locket chain', player)
brasskey = thing('tiny brass key', 'tiny brass key small', 0,
                 desc="A tiny brass key, no longer than a matchstick, with a curly bow. Too small for any door. Just "
                      "right for something delicate.")
nickel = thing('nickel', 'nickel coin change', player,
               desc="A buffalo nickel, worn smooth. Your lucky nickel. It hasn't been lucky since 1944, but you're a "
                    "loyal man.")
coat = thing('trench coat', 'trench coat trenchcoat raincoat', player, attrs=['CLOTHING', 'WORN'],
             desc="Your trench coat: tan once, now the colour of a rainy Tuesday. It has kept you dry through four "
                  "winters and two shootouts.")
fedora = thing('fedora', 'fedora hat', player, attrs=['CLOTHING', 'WORN'],
               desc="A grey fedora with a sweat-stained band. Rain drips from the brim like a slow clock.")
money = thing('twenty-dollar bill', 'twenty dollar dollars bill money cash buck bucks 20 debt', 0,
              desc="Twenty dollars, folded twice. Andrew Jackson looks like he's had a long night too.")

# office
desk = thing('desk', 'desk oak', office, attrs=['SCENERY', 'SUPPORTER'],
             desc="The desk is older than your career and in better shape. It has one drawer, a telephone, and a ring "
                  "from every glass of rye you never should have poured.")
drawer = thing('desk drawer', 'drawer desk', office, attrs=['SCENERY', 'CONTAINER', 'OPENABLE'],
               desc="A shallow drawer that sticks in wet weather. Which, in Port Halcyon, is always.")
revolver = thing('revolver', 'revolver gun pistol 38 piece rod heater', drawer)
flashlight = thing('flashlight', 'flashlight torch light battered', drawer, attrs=['SWITCHABLE'],
                   desc="A battered chrome flashlight. The batteries are new, which makes them the newest thing you own.")
cabinet = thing('filing cabinet', 'filing cabinet file files', office, attrs=['SCENERY', 'CONTAINER', 'OPENABLE'],
                desc="Three drawers, labelled A-H, I-P and Q-Z in your own careless hand. The 'B' section is "
                     "suspiciously fat.")
cartridges = thing('box of cartridges', 'box cartridges bullets ammo ammunition rounds shells cartridge bullet', cabinet,
                   desc="A cardboard box of .38 Special cartridges. Filed under B, for Bullets. You are a "
                        "professional.")
phone = thing('telephone', 'telephone phone receiver', office, attrs=['SCENERY'],
              desc="A black Bakelite telephone. It mostly rings with bad news and bill collectors.")
window = thing('window', 'window glass rain', office, attrs=['SCENERY'],
               desc="Rain crawls down the glass. Across the street, the neon PAWN sign stutters on and off. Below, "
                    "Mercer Street shines like an oil slick.")
rye = thing('bottle of rye', 'bottle rye whiskey whisky booze', office, attrs=['SCENERY'],
            desc="Old Grand-Dad, a third full. Or two-thirds empty, depending on how the night goes.")
rack = thing('coat rack', 'coat rack hook', office, attrs=['SCENERY'],
             desc="A bentwood coat rack, currently holding nothing but the memory of better coats.")
license_ = thing('license', 'license licence certificate wall frame', office, attrs=['SCENERY'],
                 desc="'SAMUEL J. DECKER -- LICENSED PRIVATE INVESTIGATOR -- CITY OF PORT HALCYON.' The photo makes you "
                      "look honest. Photos lie.")

# street
neon = thing('neon signs', 'neon sign signs pawn pawnshop shop awning', street, attrs=['SCENERY'],
             desc="Mr. Feldman's pawnshop is dark; his sign says BACK AT 9 and has said so since 1946. The Blue "
                  "Lantern's sign glows a cold, pretty blue, the colour of a drowned girl's lips.")
puddles = thing('puddles', 'puddle puddles rain gutter gutters asphalt street', street, attrs=['SCENERY'],
                desc="Neon bleeds into the puddles, red and blue, like a crime scene painted by a jazz musician.")
butt = thing('cigarette butt', 'cigarette butt stub oil stain sedan car', street, attrs=['SCENERY'],
             desc="Somebody parked across the street not long ago -- there's an oil stain and a cigarette butt still "
                  "smoking in the rain. Expensive brand. Turkish.")

# club
gus = thing('Gus', 'gus bartender barman barkeep', club, attrs=['PERSON', 'PROPER'],
            desc="Gus has been polishing the same glass since 1938. He has a face like a closed fist and the soul of "
                 "a bad poet. He also owes you twenty bucks.")
moose = thing('Moose', 'moose bouncer doorman goon', club, attrs=['PERSON', 'PROPER'],
              desc="Moose is what would happen if a refrigerator learned to wear a suit. His knuckles have knuckles.")
band = thing('band', 'band stage musicians trumpet trumpeter music bass drums', club, attrs=['SCENERY'],
             desc="Four tired men in white jackets playing 'Blue Moon' slow enough to cry to. The piano on the stage "
                  "is silent; the stool in front of it is empty. Eddie's stool.")
bar = thing('bar', 'bar counter till glass', club, attrs=['SCENERY'],
            desc="A long mahogany bar. Behind it, bottles stand in rows like witnesses who won't talk.")
tables = thing('tables', 'tables table couples crowd dancers', club, attrs=['SCENERY'],
               desc="Couples sway between little round tables, holding each other like the floor might give way.")

# dressing room
mirror = thing('mirror', 'mirror bulbs glass lipstick message writing', dressing, attrs=['SCENERY'])
vanity = thing('vanity table', 'vanity table jars brushes powder puff cream', dressing, attrs=['SCENERY', 'SUPPORTER'])
letter = thing('letter', 'letter paper note envelope', dressing, attrs=['CONCEALED'])
gown = thing('gown', 'gown dress sequins sequined', dressing, attrs=['SCENERY'],
             desc="Midnight-blue sequins. It probably costs more than your car. Then again, so does a good sandwich.")
velvet = thing('velvet case', 'velvet case box', dressing, attrs=['SCENERY'],
               desc="A little velvet-lined case on the vanity, empty. The hollow inside is shaped for a very small "
                    "pistol. A derringer, maybe. The kind a lady keeps in her purse. You file that away.")

# hotel
pruitt = thing('Mr. Pruitt', 'pruitt clerk mr night', lobby, attrs=['PERSON', 'PROPER'])
bell = thing('brass bell', 'bell brass', lobby, attrs=['SCENERY'],
             desc="A brass bell with a sign: RING FOR SERVICE. Underneath, smaller: DON'T.")
keyrack = thing('key rack', 'rack hooks', lobby, attrs=['SCENERY'])
roomkey = thing('room key', 'room key 6 six wooden tag', 0,
                desc="A heavy brass key on a wooden tag with a burnt-in 6.")
palm = thing('potted palm', 'palm plant chandelier carpet', lobby, attrs=['SCENERY'],
             desc="The palm has given up. The chandelier is thinking about it.")
door6 = thing('door to room 6', 'door 6 six', hallway, attrs=['SCENERY', 'OPENABLE', 'LOCKED'], WITH_KEY=roomkey)
bulb = thing('bulb', 'bulb light wallpaper', hallway, attrs=['SCENERY'],
             desc="A bare bulb, buzzing like an angry wasp. The wallpaper is peeling in long, sad tongues.")

# room 6
piano = thing('piano', 'piano upright fallboard lid keys hammers keyhole', room6,
              attrs=['SCENERY', 'CONTAINER', 'OPENABLE', 'LOCKED'], WITH_KEY=brasskey)
sheet = thing('sheet music', 'sheet music nocturne score stand', room6, attrs=['SCENERY'],
              desc="Handwritten sheet music: 'Nocturne for a Rainy Pier' by E. Lark. In the margin, in pencil, "
                   "someone has written: 'Hide the important things under the hammers.'")
ledger = thing('ledger', 'ledger book black leather accounts', piano)
hpass = thing('harbor pass', 'harbor harbour pass card permit', piano,
              desc="A Harbor Commission pass, stamped and signed: 'BEARER PERMITTED ACCESS TO PIER 9 AT ALL HOURS.' "
                   "Eddie's photo is pasted on it. In the dark, you could pass for his much older, much uglier "
                   "brother.")
mess = thing('mess', 'dresser drawers mattress feathers bed mess', room6, attrs=['SCENERY'],
             desc="Whoever tossed this room was thorough and angry. They slit the mattress, emptied the drawers and "
                  "even pulled up a floorboard. The only thing they didn't touch was the piano. Amateurs.")
window6 = thing('window', 'window', room6, attrs=['SCENERY'],
                desc="The window is open a crack. Beyond it, the rusty fire escape clings to the wall.")
rico = thing('Rico', 'rico salvatore knife thug scar', 0, attrs=['PERSON', 'PROPER'],
             desc="Rico Salvatore, called 'the Knife' by people who were careful to say it behind his back. A white "
                  "scar runs from his ear to the corner of his mouth, so he always looks like he's smiling. He isn't.")
switchblade = thing('switchblade', 'switchblade knife blade', 0,
                    desc="Rico's switchblade: six inches of Italian steel with a pearl handle. Sharp enough to shave a "
                         "rumour.")

# fire escape and alley
ladder = thing('ladder', 'ladder fire escape slats', fireesc, attrs=['SCENERY'],
               desc="Rusted iron, slick with rain. It holds your weight, but it complains about it.")
ladder2 = thing('fire escape', 'fire escape ladder', alley, attrs=['SCENERY'],
                desc="The fire escape zigzags up the side of the Calloway. Its bottom ladder hangs within reach.")
cans = thing('trash cans', 'trash cans can garbage bins crate', alley, attrs=['SCENERY'],
             desc="Dented trash cans, overflowing. You've been in this business long enough to know the difference "
                  "between garbage and evidence. Mostly.")
cat = thing('black cat', 'black cat kitty skinny', alley, attrs=['PERSON'],
            desc="A skinny black cat with one torn ear and an expression of total contempt for you and your "
                 "profession.")

# harbor
payphone = thing('payphone', 'payphone phone telephone booth slot', harbor, attrs=['SCENERY'],
                 desc="A payphone under a gas lamp. A sign says: LOCAL CALLS 5 CENTS. Somebody has scratched 'CRANE "
                      "OWNS THIS TOWN' into the metal.")
fog = thing('fog', 'fog mist lamp mission chandleries', harbor, attrs=['SCENERY'],
            desc="The fog rolls in from the bay, thick and grey, swallowing the gas lamps one by one.")

# pier gate
silas = thing('Old Silas', 'silas watchman guard old man', gate, attrs=['PERSON', 'PROPER'],
              desc="Old Silas has been watching this pier since ships had sails. His eyes are watery, but they don't "
                   "miss much. He's wrapped in a blanket, reading a racing form by lamplight.")
fence = thing('gate', 'gate fence guardhouse wire barbed', gate, attrs=['SCENERY'],
              desc="Chain-link and barbed wire, and a gate that only opens for people Silas likes. Silas doesn't like "
                   "many people.")

# pier
salamander = thing('Salamander', 'salamander freighter ship boat gangway gangplank sailors', pier,
                   attrs=['SCENERY', 'PROPER'],
                   desc="Three hundred feet of rust held together by bad intentions. Two sailors with shoulders like "
                        "anchors guard her gangway. Her stack is smoking: she's getting ready to sail.")
crates = thing('crates', 'crates crate straw rifles barrels', pier, attrs=['SCENERY'],
               desc="Stencilled MACHINE PARTS -- HANDLE WITH CARE. One has been pried open. Under the straw lies "
                    "the oily gleam of rifle barrels. Machine parts. Sure.")
bucket = thing("fisherman's bucket", 'bucket fisherman fishermans bait', pier, attrs=['SCENERY'],
               desc="A bucket that smells of last week's bait.")
knife = thing('gutting knife', 'gutting fishing knife blade', pier,
              initial="A fisherman's gutting knife is stuck in the rim of a bait bucket by one of the pilings.",
              desc="A thin, wicked fisherman's knife, the kind they use to open up fish. Rusty, but sharp.")
whdoor = thing('warehouse', 'warehouse 13 thirteen door doors chain', pier, attrs=['SCENERY'],
               desc="Warehouse 13 is a corrugated-iron barn the size of a cathedral. The big doors are chained, but a "
                    "small side door stands ajar. Inside, only darkness.")

# warehouse
eddie = thing('Eddie Lark', 'eddie lark brother pianist man', warehouse, attrs=['PERSON', 'PROPER'])
ropes = thing('ropes', 'ropes rope knots bonds chair gag', warehouse, attrs=['SCENERY'])
forklift = thing('forklift', 'forklift crates boxes rafters', warehouse, attrs=['SCENERY'],
                 desc="Crates stacked to the rafters, every one stencilled MACHINE PARTS. A forklift sleeps in the "
                      "shadows.")
crane = thing('Augustus Crane', 'augustus crane commissioner a.c. ac boss suit', 0, attrs=['PERSON', 'PROPER'],
              desc="Augustus Crane, Harbor Commissioner: silver hair, white suit, a carnation in the lapel and a "
                   "pearl-handled pistol in his manicured hand. He looks like a man who has never once been wet.")
vivian = thing('Vivian Lark', 'vivian viv lark miss singer woman sister', 0, attrs=['PERSON', 'PROPER', 'FEMALE'],
               desc="Vivian Lark, wrapped in silver fox, a tiny derringer glinting in her gloved hand. Even now, she's "
                    "the most beautiful thing in the room. Snakes usually are.")
junction = thing('junction box', 'junction box fuse fusebox lamps lamp lights wires switch', 0, attrs=['SCENERY'],
                 desc="A big grey junction box by the side door. Every lamp in the warehouse hangs off the thick "
                      "cables running out of it.")
police = thing('police', "police cops o'rourke orourke captain precinct", 0, attrs=['PROPER'])

st.const('revolver', revolver.num)

# ====================================================================== shared routines


def held(o):
    return ('in', o, player)


st.routine('Die', ('t',), (), [('set', 'deadflag', 1)])

st.routine('LoadGun', (), (), [
    ('if', 'loaded', say("It's already loaded. Six chances to be wrong.")),
    ('if', ('notin', revolver, player), say("You'll need to be holding the revolver.")),
    ('if', ('not', ('call', 'InScope', cartridges)), say("You don't have any ammunition. Somewhere in this office "
                                                           "there's a box of it, filed under something clever.")),
    ('set', 'loaded', 1),
    "You thumb six .38 rounds into the cylinder and snap it shut. The weight feels right in your hand -- like an old "
    "argument you know you can win.\n",
    call('Award', 5),
])

st.routine('PoliceCall', (), (), [
    ('if', 'police_called', say("You've already called the cavalry. Now you just have to stay alive until it gets "
                                 "there.")),
    ('if', ('notin', ledger, player), [
        "You dial Central and ask for Captain O'Rourke. It takes a while.\n\n'Decker,' he growls, 'it's the middle "
        "of the night. Unless you've got proof of something, call me in the morning. Or never. Never works too.'\n\n"
        "Click.\n", ('rtrue',)]),
    ('set', 'police_called', 1),
    "You get O'Rourke on the line and read him a few choice pages of the ledger. There's a long silence. When he "
    "speaks again, his voice has changed.\n\n'Crane. Holy Mother of God.' A pause. 'Decker, where are you going "
    "with that?'\n\n'Pier 9. Warehouse 13. Eddie Lark is in there, and the Salamander sails at four.'\n\n'Don't do "
    "anything stupid until I get there.'\n\n'Captain,' you say, 'stupid is the only thing I'm good at.'\n\nYou hang "
    "up.\n",
    call('Award', 10),
])

# Unlock and open the piano
st.routine('OpenPiano', (), (), [
    ('ungive', piano, 'LOCKED'), ('give', piano, 'OPEN'),
    "The tiny brass key slides into the keyhole like it was waiting for you. Click. You lift the fallboard, then the "
    "heavy lid, and shine your eyes down into the guts of the piano.\n\nUnder the hammers, wrapped in oilcloth, lies "
    "a thick ledger bound in black leather. Clipped to it is a harbor pass.\n\nThe key is in the music. Eddie, you "
    "clever kid.\n",
    ('set', 'piano_open', 1),
    call('Award', 10),
])

st.routine('FreeEddie', (), ('k',), [
    ('if', 'eddie_free', say("Eddie's already free. Now you just have to get him out of here.")),
    ('set', 'k', 0),
    ('if', ('in', switchblade, player), [('set', 'k', switchblade)]),
    ('if', ('in', knife, player), [('set', 'k', knife)]),
    ('if', ('==', 'k', 0), say("The knots are wet and pulled tight as a banker's purse strings. You'll need something "
                                "sharp.")),
    'You saw through the ropes with ', ('do', ('call', 'PrintThe', 'k')),
    ". They part one by one: ankles, then wrists. Eddie sags forward and claws the gag from his mouth.\n",
    ('set', 'eddie_free', 1), ('set', 'climax', 1),
    call('Award', 10),
])

st.routine('BestEnding', (), (), [
    "\nThen the night splits wide open.\n\nSirens -- a whole choir of them -- and headlights blazing through every "
    "crack in the walls. 'POLICE! NOBODY MOVE!' Captain O'Rourke comes through the side door with a shotgun and half "
    "the precinct behind him.\n\nCrane's pistol wavers. For a moment he looks old. Then he very carefully lays the "
    "pistol down on a crate, the way a gentleman sets down his fork at a dinner party.\n\nVivian doesn't. She bolts "
    "for the dark at the back of the warehouse -- and runs straight into a patrolman roughly the size of Moose. The "
    "derringer skitters across the concrete and comes to rest at your feet.\n\nLater, out on the pier, wrapped in a "
    "police blanket, Eddie Lark watches the Salamander's crew being marched off in handcuffs. O'Rourke weighs the "
    "ledger in his hand like a brick of gold.\n\n'This is going to bring down half of City Hall, Decker.'\n\n'Only "
    "half?'\n\n'Give it time.'\n\nThe rain has stopped. Over the bay, the sky is turning the colour of weak coffee. "
    "You light a cigarette -- you quit in 1946, but some nights don't count -- and for once, it tastes like "
    "victory.\n",
    call('Award', 15),
    ('set', 'deadflag', 2),
])

# ====================================================================== object behaviour

before(locket,
       on('EXAMINE', 'READ', 'OPEN', 'SEARCH')(
           "A silver locket on a fine chain, still warm from her hand. Inside is a photograph of a grinning young man "
           "with Vivian's eyes -- Eddie, it must be. Engraved on the back: 'For E. -- the key is in the music. -- V.'\n",
           ('if', ('not', 'key_found'), [
               ('set', 'key_found', 1), ('move', brasskey, player),
               "\nThe photo sits a little crooked. You pry it loose with a thumbnail, and something falls into your "
               "palm: a tiny brass key.\n"]),
       ),
       on('WEAR')("It's not your style. Your style is 'rained on'.\n"))

before(revolver,
       on('EXAMINE')(
           "Your .38 Police Positive. Snub-nosed, ugly and honest -- three things you have in common with it. ",
           ('if', 'loaded', ['The cylinder is full.\n'],
            ["The cylinder is empty. You never did get around to buying bullets. Or did you?\n"])),
       on('LOAD')(('do', ('call', 'LoadGun'))),
       ('if', ('and', ('==', 'action', 'INSERT'), ('==', 'noun', cartridges)), [('do', ('call', 'LoadGun')), ('rtrue',)]),
       on('SHOOT')(('if', ('==', 'noun', revolver), say('Shoot at what, exactly?'))))

before(cartridges,
       on('INSERT', 'LOAD')(('do', ('call', 'LoadGun'))),
       on('EAT')("They're .38s, not jellybeans.\n"))

before(drawer,
       on('OPEN', 'SEARCH')(
           ('if', ('has', drawer, 'OPEN'), [('if', ('==', 'action', 'OPEN'), say("It's already open."))]),
           ('give', drawer, 'OPEN'),
           ('if', ('child', drawer), [
               'The drawer sticks, then gives. Inside: ', ('do', ('call', 'ListInline', drawer)), '.\n'],
            ['The drawer is empty, apart from a few paperclips and a lot of regret.\n'])),
       on('EXAMINE')(
           "A shallow drawer that sticks in wet weather. Which, in Port Halcyon, is always.",
           ('if', ('has', drawer, 'OPEN'), [
               ('if', ('child', drawer), [' Inside: ', ('do', ('call', 'ListInline', drawer)), '.'], [' It is empty.'])],
            [' It is closed.']), '\n'))

before(cabinet,
       on('OPEN', 'SEARCH')(
           ('if', ('in', cartridges, cabinet), [
               ('give', cabinet, 'OPEN'),
               "You haul open the cabinet. Under B, between 'Bancroft Divorce' and 'Bills, Unpaid', sits a box of .38 "
               "cartridges. Filed under B, for Bullets. You are a professional.\n"],
            ["Nothing in there but old cases and older bills.\n"])))

before(desk,
       on('OPEN', 'SEARCH', 'CLOSE')(('set', 'noun', drawer), ('ret', ('call', 'B_%d' % drawer.num))))

before(phone,
       on('CALL', 'USE', 'TAKE', 'PUSH')(('do', ('call', 'PoliceCall'))))

before(window,
       on('OPEN')("It's been painted shut since Truman was a senator.\n"),
       on('SEARCH')("You look down at the street. The black sedan that was idling there is gone, leaving an oil stain "
                    "and a cigarette butt still smoking in the rain.\n"))

before(rye,
       on('DRINK', 'TAKE')(
           "You take a pull of rye. It burns all the way down and lights a small fire of courage. Small. Very "
           "small.\n"))

before(coat,
       on('SEARCH')("Lint, a book of matches from a bar that closed in 1947, and a hole where your luck used to be.\n"))

before(money,
       on('EXAMINE')("Twenty dollars, folded twice. Andrew Jackson looks like he's had a long night too.\n"))

before(flashlight,
       on('USE')(('set', 'action', 'SWITCHON'), ('ret', False)))

before(nickel,
       on('INSERT')(('if', ('==', 'second', payphone), [('do', ('call', 'PayPhone')), ('rtrue',)]), ('ret', False)))

before(butt, on('TAKE')("It's evidence of nothing, and it's wet.\n"))

# ---------------------------------------------------------------- the Blue Lantern
st.routine('GusTalk', (), (), [
    ('if', ('not', 'gus_paid'), [
        "'Sam.' Gus sets down the glass with the sigh of a man who's been expecting you since 1946. 'I know, I know. "
        "Twenty bucks. The Hennessy job.' He counts a twenty out of the till like each bill is a member of his "
        "family, and pushes it across the bar.\n\n'Now we're square. And Sam?' He leans in. 'Eddie didn't just miss "
        "his set. Two goons came asking for him Tuesday. One of 'em had a scar, ear to mouth. That's Rico Salvatore. "
        "Rico works for Commissioner Crane, the way I hear it, and I hear it from nobody.'\n",
        ('set', 'gus_paid', 1), ('move', money, player), ('give', money, 'MOVED'),
        call('Award', 5), ('rtrue',)]),
    "'We're square, Sam. Square as a checkerboard.' Gus polishes the glass. 'Ask me about something useful. Eddie. "
    "Miss Lark. The Commissioner. Moose.'\n",
])

before(gus,
       on('TALK')(('do', ('call', 'GusTalk'))),
       on('ASK')(('switch', 'second', [
           ((money, gus), [('do', ('call', 'GusTalk'))]),
           (eddie, ["'Kid plays like an angel and gambles like a fool. Last week he kept going on about the Salamander. "
                    "Some freighter tied up at Pier 9. Said he'd seen what she was loading.'\n"]),
           (vivian, ["Gus lowers his voice. 'Miss Lark's been keeping company above her station, if you know what I "
                     "mean. Fancy cars. A man in a white suit. You didn't hear it from me.'\n"]),
           (crane, ["'Augustus Crane. Harbor Commissioner. Owns the docks, the cops and half the judges in this town. "
                    "The other half he rents.'\n"]),
           (moose, ["'Moose takes orders from Miss Lark and nobody else. Show him something of hers, maybe he'll let "
                    "you through.'\n"]),
           (rico, ["'Rico the Knife. If you ever see him, Sam, walk the other way. Fast. Faster than that.'\n"]),
           (salamander, ["'A rust-bucket freighter at Pier 9. Sails under a Panama flag and asks no questions.'\n"]),
           (ledger, ["'A ledger?' Gus goes pale. 'Sam, I don't want to know. I really, truly don't want to know.'\n"]),
           (locket, ["'That's Viv's locket. She never takes it off. If she gave it to you, she's either scared or "
                     "she's up to something. Maybe both.'\n"]),
           ((lobby, roomkey, room6, pruitt), ["'Eddie rents a room at the Calloway, across the street. Number 6. "
                                              "Pruitt runs the desk. He's a man of principle, and his principle is "
                                              "cash.'\n"]),
           (police, ["'O'Rourke's straight. Maybe the only straight cop left. But he won't move without proof.'\n"]),
           ((pier, warehouse, silas), ["'Pier 9's locked up tight at night. Old Silas won't let you near it without a "
                                       "Harbor Commission pass.'\n"]),
       ], ["Gus shrugs. 'Ask me about something I know, Sam. Eddie, Miss Lark, the Commissioner... or that twenty bucks "
           "you keep staring at me about.'\n"])),
       on('GIVE')(('if', ('==', 'noun', nickel), say("'Keep your nickel, Sam. Buy yourself some luck.'")),
                  ('if', ('==', 'noun', money), say("'Don't tempt me.'")),
                  "Gus looks at it, then at you. 'What am I, a pawnshop?'\n"),
       on('ATTACK')("Gus has a baseball bat under the bar and twenty years of practice. You let it go.\n"))

before(moose,
       on('TALK', 'ASK')("Moose looks down at you from a great height. 'Backstage is private. Nobody goes back without "
                         "Miss Lark's say-so.'\n"),
       on('SHOW', 'GIVE')(
           ('if', ('==', 'noun', locket), [
               ('if', 'moose_ok', say("Moose nods. 'I said go on back.'")),
               "Moose squints at the locket. Something moves behind his face -- the look of a big dog catching its "
               "owner's scent. 'That's Miss Lark's.' He steps aside, which takes a while. 'Go on back. Make it "
               "quick.'\n",
               ('set', 'moose_ok', 1), call('Award', 5), ('rtrue',)]),
           ('if', ('==', 'noun', money), say("Moose looks at the money like it's a bug. 'I ain't for sale.' He thinks. "
                                              "'Not that cheap.'")),
           "Moose isn't impressed. Moose was born not impressed.\n"),
       on('ATTACK', 'SHOOT')("You consider it. Moose considers you considering it. You both agree it would end badly for "
                             "one of you, and it isn't Moose.\n"))

before(club,
       ('if', ('and', ('==', 'action', 'GO'), ('==', 'dir', 'D_N'), ('not', 'moose_ok')), [
           "Moose plants a hand the size of a hubcap on your chest. 'Uh-uh. Nobody goes backstage without Miss Lark's "
           "say-so.'\n", ('rtrue',)]),
       on('PLAY')("You're not going up on that stage. Not tonight, not ever.\n"))
describe(club,
         "Smoke hangs under the low ceiling like a second, lazier ceiling. A tired band on a little stage is playing "
         "something slow enough to cry to, but the piano stool is empty. A long bar runs along one wall, where Gus "
         "the bartender polishes a glass.",
         ('if', 'moose_ok', [" Moose leans against the wall beside the backstage door to the north."],
          [" Moose the bouncer stands in front of the backstage door to the north like a wall with a pulse."]),
         " The street is back west.\n")

# ---------------------------------------------------------------- dressing room
before(mirror,
       on('EXAMINE', 'READ', 'SEARCH')(
           "Someone has written on the glass in dark red lipstick, the letters jagged and hurried:\n\n",
           ('style', 2), '     PIER 9 -- THE SALAMANDER -- SAILS AT FOUR\n', ('style', 0),
           "\nUnderneath, smaller: 'Ask Silas. Show him the pass.'\n\nIt's Eddie's handwriting. You've seen it on the "
           "sheet music at the Lantern. He was here, and he was scared.\n",
           ('if', ('not', 'mirror_read'), [('set', 'mirror_read', 1), call('Award', 5)])))
before(vanity,
       on('EXAMINE', 'SEARCH')(
           "Cold cream, rouge, a silver hairbrush, an empty velvet case",
           ('if', ('has', letter, 'CONCEALED'), [
               "... and, tucked under a powder puff, a folded letter.\n", ('ungive', letter, 'CONCEALED')],
            ['.\n'])))
before(letter,
       on('EXAMINE', 'READ')(
           "Heavy cream paper engraved with the seal of the Port Halcyon Harbor Commission. The handwriting is elegant "
           "and cruel:\n\n",
           ('style', 4), "     'V. -- The boy has the ledger and a big mouth. Find the one, and I'll close the "
                         "other. The Salamander sails at four. Don't be late, my dear. -- A.C.'\n", ('style', 0),
           "\nYou read it twice. Then a third time, because you don't like what it's telling you about the woman who "
           "hired you.\n",
           ('if', ('not', 'letter_read'), [('set', 'letter_read', 1), call('Award', 5)])))
describe(dressing,
         "A narrow room that smells of gardenias and gun oil -- an odd perfume for a singer. A vanity table crowded "
         "with jars and brushes faces a big mirror ringed with bulbs, half of them dead. Something is written across "
         "the mirror in red. A sequined gown hangs from a hook. The only way out is south, back to the club.\n")

# ---------------------------------------------------------------- hotel
st.routine('WakePruitt', (), (), [
    ('if', 'pruitt_awake', [('rfalse',)]),
    ('set', 'pruitt_awake', 1),
    "Pruitt jerks awake with a snort, knocks his spectacles askew and glares at you over them. 'We're full,' he "
    "says. 'We're always full. Especially for gumshoes.'\n",
    ('rtrue',),
])
st.routine('BribePruitt', (), (), [
    ('if', 'got_roomkey', say("'You already got your key, mister. Don't push your luck.'")),
    ('if', ('notin', money, player), say("You pat your pockets. Lint and regret. Pruitt's principles are not for sale "
                                          "that cheap.")),
    ('set', 'pruitt_awake', 1),
    "You lay the twenty on the desk. Pruitt makes it disappear with the speed of a stage magician. He unhooks a key "
    "from the rack and slides it across to you without looking.\n\n'Room 6, third floor. Mr. Lark's account is now "
    "settled. I was asleep the whole time.'\n",
    ('remove', money), ('move', roomkey, player), ('give', roomkey, 'MOVED'), ('set', 'got_roomkey', 1),
    call('Award', 5),
])
before(pruitt,
       on('EXAMINE')(
           "A thin man with thin hair and thinner patience, in a cardigan that has seen the Great Depression and "
           "never recovered. ",
           ('if', 'pruitt_awake', ['He watches you over his spectacles like you might steal the potted palm.\n'],
            ['He is asleep in his chair, snoring like a foghorn.\n'])),
       on('WAKE', 'ATTACK', 'PUSH')(('if', ('not', ('call', 'WakePruitt')), ["He's awake. Unfortunately for both of "
                                                                             "you.\n"])),
       on('TALK', 'ASK')(
           ('if', ('call', 'WakePruitt'), [('rtrue',)]),
           ('if', 'got_roomkey', say("'I was asleep,' Pruitt says firmly. 'I'm still asleep. Go away.'")),
           "'Mr. Lark in number 6 is not receiving visitors. Mr. Lark is not, in fact, receiving anybody, on account "
           "of not having paid his rent since September.' He taps the key rack meaningfully. 'Of course, if someone "
           "were to settle his account...'\n"),
       on('GIVE')(
           ('if', ('==', 'noun', money), [('do', ('call', 'BribePruitt')), ('rtrue',)]),
           ('if', ('==', 'noun', nickel), say("'A nickel?' Pruitt looks at it like it's a dead fly. 'Mister, for a "
                                               "nickel I don't even wake up.'")),
           "'This is a hotel, not a swap meet.'\n"),
       on('SHOW')(
           ('if', ('==', 'noun', locket), say("'Very pretty. Doesn't pay Mr. Lark's rent.'")),
           "Pruitt is not impressed. Pruitt has seen everything twice, mostly at three in the morning.\n"))
before(bell,
       on('RING', 'PUSH', 'USE', 'TAKE')(
           'Ding!\n', ('if', ('not', ('call', 'WakePruitt')), ["Pruitt glares at you. 'I heard you the first "
                                                                "time.'\n"])))
before(keyrack,
       on('EXAMINE', 'SEARCH')("Rows of brass hooks, most of them empty. ",
                               ('if', 'got_roomkey', ['The hook marked 6 is empty now.\n'],
                                ['The hook marked 6 holds a key on a heavy wooden tag.\n'])),
       on('TAKE')("Pruitt's hand comes down on yours like a guillotine. 'Ah-ah-ah.'\n"))
before(lobby,
       ('if', ('and', ('==', 'action', 'TAKE'), ('==', 'noun', roomkey), ('not', 'got_roomkey')), [
           "Pruitt's hand comes down on yours like a guillotine. 'Ah-ah-ah.'\n", ('rtrue',)]))
describe(lobby,
         "The Calloway's lobby has the faded grandeur of a widow's ballgown: threadbare carpet, a dusty potted palm "
         "and a chandelier with more cobwebs than crystals. ",
         ('if', 'pruitt_awake', ["Behind the front desk, Mr. Pruitt the night clerk eyes you over his spectacles."],
          ["Behind the front desk, Mr. Pruitt the night clerk is asleep in his chair, snoring like a foghorn."]),
         " A brass bell sits on the desk beside a rack of keys. Stairs climb into the gloom, and the street door is "
         "east.\n")

st.routine('EnterRoom6', (), (), [
    ('if', ('has', door6, 'OPEN'), [('do', ('call', 'GoTo', room6)), ('rtrue',)]),
    ('if', ('has', door6, 'LOCKED'), [
        ('if', ('notin', roomkey, player), say('The door to room 6 is locked.')),
        ('ungive', door6, 'LOCKED'),
        'You unlock the door with the room key and push it open.\n']),
    ('give', door6, 'OPEN'),
    ('do', ('call', 'GoTo', room6)),
])
before(hallway,
       ('if', ('or', ('and', ('==', 'action', 'GO'), ('==', 'dir', 'D_E', 'D_IN')),
                ('and', ('==', 'action', 'ENTER'), ('==', 'noun', door6))), [('do', ('call', 'EnterRoom6')), ('rtrue',)]))
before(door6,
       on('EXAMINE')("A cheap pine door with a tarnished brass 6. ",
                     ('if', ('has', door6, 'OPEN'), ['It stands open.\n'],
                      [('if', ('has', door6, 'LOCKED'), ["It's locked.\n"], ["It's closed.\n"])])),
       on('OPEN')(('if', ('and', ('has', door6, 'LOCKED'), ('in', roomkey, player)), [
           ('ungive', door6, 'LOCKED'), ('give', door6, 'OPEN'), 'You unlock the door with the room key and push it '
                                                                 'open.\n', ('rtrue',)]), ('rfalse',)),
       on('KNOCK')("You knock. Nobody answers. Nobody's been answering in there for days.\n"))
describe(hallway,
         "A long, crooked hallway lit by a single bare bulb that buzzes like an angry wasp. Wallpaper peels from the "
         "walls in long tongues. At the east end, the door to room 6 ",
         ('if', ('has', door6, 'OPEN'), ['stands open.'], ['is closed.']),
         ' The stairs lead back down.\n')

# ---------------------------------------------------------------- room 6
describe(room6,
         "Somebody has been here before you, and they weren't looking for the bathroom. Drawers hang out of the "
         "dresser like tongues, the mattress has been slit open, and feathers lie everywhere like dirty snow. Against "
         "one wall stands an old upright piano, the only thing in the room nobody bothered to smash. A sheet of music "
         "is propped on its stand. A window opens onto the fire escape. The door is west.\n",
         ('if', ('in', rico, room6), ["\nRico 'the Knife' Salvatore stands in the doorway, a switchblade dancing in "
                                      "his hand.\n"]))
st.routine('PianoAct', (), (), [
    ('if', ('has', piano, 'LOCKED'), [
        ('if', ('in', brasskey, player), [('do', ('call', 'OpenPiano')), ('rtrue',)]),
        "The fallboard over the keys is locked. In the middle of it there's a tiny brass keyhole, much too small for "
        "any ordinary key.\n", ('rtrue',)]),
    ('if', ('==', 'action', 'OPEN'), say("It's already open.")),
    "You've already unlocked it.\n",
])
before(piano,
       on('EXAMINE', 'SEARCH')(
           "A battered upright with yellowed keys. Somebody has scratched 'E.L.' into the varnish. ",
           ('if', ('has', piano, 'LOCKED'), [
               "The fallboard over the keys is closed and locked; there's a tiny brass keyhole in the middle of it. "
               "Above it, on the music stand, sits a sheet of music.\n"],
            ["The fallboard and lid are open.",
             ('if', ('child', piano), [' Under the hammers you can see ', ('do', ('call', 'ListInline', piano)), '.\n'],
              [' There is nothing left inside but hammers and strings.\n'])])),
       on('UNLOCK', 'OPEN')(('do', ('call', 'PianoAct'))),
       on('CLOSE', 'LOCK')("Better leave it open. It's not like Eddie's coming back for it tonight.\n"),
       on('PLAY')(
           ('if', ('has', piano, 'LOCKED'), say('The fallboard is locked over the keys.')),
           "You pick out the first bars of 'Nocturne for a Rainy Pier' with two fingers. It sounds like a cat walking "
           "across a typewriter. Somewhere, Eddie is weeping.\n"))
before(sheet, on('TAKE')("Leave it. You've got what you need from it: 'under the hammers'.\n"),
       on('PLAY')(('set', 'action', 'PLAY'), ('set', 'noun', piano), ('ret', ('call', 'B_%d' % piano.num))))

before(ledger,
       on('EXAMINE', 'READ')(
           "A ledger bound in black leather, swollen with damp. Page after page of dates, ship names and dollar "
           "amounts in a neat accountant's hand: shipments of 'machine parts' through Pier 9, and payments -- to "
           "police captains, to judges, to a city councilman with a famous smile. At the bottom of every page, the "
           "same initials: A.C.\n\nWith this book, you could hang Augustus Crane from the tallest crane in his own "
           "harbor.\n"),
       on('TAKE')(('do', ('call', 'TakeLedger'))),
       on('GIVE')(('if', ('==', 'second', rico), [('rfalse',)]),
                  ('if', ('==', 'second', crane, vivian), [('rfalse',)]),
                  "You're not handing that to anybody but a judge.\n"),
       on('DROP')("You'd sooner drop your own head.\n"))

st.routine('TakeLedger', (), (), [
    ('if', ('in', ledger, player), say('You already have it. You are not letting go of it.')),
    ('move', ledger, player), ('give', ledger, 'MOVED'),
    "You lift out the ledger, with the harbor pass still clipped to its cover. It's heavier than it looks. The truth "
    "usually is.\n",
    ('if', ('in', hpass, piano), [('move', hpass, player), ('give', hpass, 'MOVED')]),
    ('if', ('not', 'ledger_taken'), [('set', 'ledger_taken', 1), ('set', 'rico_timer', 1)]),
])
before(hpass, on('TAKE')(('if', ('in', hpass, piano), [('do', ('call', 'TakeLedger'))], [('rfalse',)])))

before(rico,
       on('SHOOT')(
           ('if', ('notin', revolver, player), say("You reach for your gun, but you're not holding it. Rico smiles.")),
           ('if', ('not', 'loaded'), say("You aim the .38 at Rico and squeeze. Click. Rico smiles. It's the worst "
                                          "thing you've ever seen.")),
           "You don't think. Your hand does it for you. The .38 bucks once, loud as the end of the world in the little "
           "room. Rico spins, clutching his shoulder, and his switchblade clatters to the floor. He stares at you with "
           "pure, cold hate -- then staggers back out the door. You hear him crash down the stairs and out into the "
           "night.\n",
           ('remove', rico), ('move', switchblade, room6), ('set', 'rico_done', 1), call('Award', 10)),
       on('ATTACK')("You throw your best punch. Rico catches your fist like a man catching a tossed apple, and "
                    "smiles.\n"),
       on('TALK', 'ASK')("'Rico. Let's talk this over.'\n\n'Sure,' says Rico. 'We're talking.' The knife never stops "
                         "moving.\n"),
       on('GIVE')(('if', ('==', 'noun', ledger), [
           "Rico takes the ledger, tucks it into his coat and says, 'Thanks, shamus.' Then he gives you something in "
           "return. It's six inches long.\n", ('remove', ledger), ('remove', rico), ('set', 'deadflag', 1), ('rtrue',)]),
           "Rico isn't interested in anything you've got. Except the ledger. And your life.\n"))

before(room6,
       ('if', ('in', rico, room6), [
           ('if', ('or', ('and', ('==', 'action', 'GO'), ('==', 'dir', 'D_OUT')),
                   ('and', ('==', 'action', 'ENTER', 'CLIMB'), ('==', 'noun', window6))), [
               "You dive for the window, and Rico's knife hisses through the air where your neck was a moment ago. "
               "You scramble out onto the fire escape. Behind you, Rico curses in two languages, but he doesn't "
               "follow -- a man his size doesn't fit through a window that small.\n",
               ('remove', rico), ('set', 'rico_done', 1), call('Award', 10),
               ('do', ('call', 'GoTo', fireesc)), ('rtrue',)]),
           ('if', ('==', 'action', 'GO'), say("Rico is between you and the door. He'd like you to try.")),
       ]),
       ('if', ('or', ('and', ('==', 'action', 'ENTER', 'CLIMB'), ('==', 'noun', window6))), [
           ('do', ('call', 'GoTo', fireesc)), ('rtrue',)]))
before(window6, on('OPEN')("It's already open a crack. Wide enough for a man in a hurry.\n"))

# ---------------------------------------------------------------- fire escape and alley
describe(fireesc,
         "A rusted iron fire escape clinging to the side of the Calloway like a drowning man to a rope. Rain drums on "
         "the slats. Through the window you can see into room 6. A ladder leads down to the alley below.\n")
before(ladder, on('CLIMB')(('do', ('call', 'GoTo', alley))))
before(ladder2, on('CLIMB')(('do', ('call', 'GoTo', fireesc))))
before(cat,
       on('PET', 'TAKE', 'KISS')(
           ('if', ('not', 'cat_petted'), [
               ('set', 'cat_petted', 1),
               "The cat permits this, briefly, with the air of a duchess accepting a peasant's tribute. Then it bites "
               "you. Fair enough.\n", ('rtrue',)]),
           "The cat has made its position clear.\n"),
       on('TALK', 'ASK')("The cat says nothing. It has seen everything that happens in this alley, and it isn't "
                         "impressed by any of it.\n"),
       on('ATTACK', 'SHOOT')("You'd never forgive yourself. Neither would the cat. Cats don't forgive.\n"))
before(cans, on('SEARCH', 'OPEN')("You dig through the garbage and find more garbage. The cat watches, judging.\n"))
describe(alley,
         "A dead-end alley that smells of wet garbage and old sins. Trash cans huddle against the wall. Above, the "
         "Calloway's fire escape zigzags up into the rain; its bottom ladder hangs within reach. A skinny black cat "
         "watches you from a crate with an expression of total contempt. Mercer Street is south.\n")

# ---------------------------------------------------------------- harbor road, gate, pier
st.routine('PayPhone', (), (), [
    ('if', ('notin', nickel, player), say('The payphone wants a nickel. Payphones always want something.')),
    ('if', ('and', ('in', ledger, player), ('not', 'police_called')), [
        'You drop your lucky nickel in the slot. It was never lucky anyway. Maybe this time.\n\n']),
    ('do', ('call', 'PoliceCall')),
])
before(payphone, on('CALL', 'USE', 'TAKE', 'PUSH')(('do', ('call', 'PayPhone'))))
before(harbor, on('CALL')(('do', ('call', 'PayPhone'))))
before(office, on('CALL')(('do', ('call', 'PoliceCall'))))
describe(harbor,
         "Harbor Road slopes down toward the water, past shuttered ship chandlers and a seamen's mission with a broken "
         "neon cross. Fog rolls in off the bay, thick enough to lean on. A lonely payphone glows under a gas lamp. "
         "Mercer Street is back north; the gates of Pier 9 loom to the east.\n")

before(silas,
       on('TALK', 'ASK')(
           ('if', 'silas_ok', say("'Whatever's going on in Thirteen tonight, son, I didn't see you. And I'd like to "
                                   "keep it that way.'")),
           ('if', ('==', 'second', salamander), say("'The Salamander? Bad ship. Bad crew. Sails at four, and she "
                                                     "don't come back with what she leaves with.'")),
           ('if', ('==', 'second', crane), say("'The Commissioner's been down here twice this week. Never in my "
                                                "life seen that man on a pier at night.'")),
           "Silas doesn't look up from his racing form. 'Pier's closed, son. Commission's orders. Unless you got a "
           "pass.'\n"),
       on('SHOW', 'GIVE')(
           ('if', ('==', 'noun', hpass), [
               ('if', 'silas_ok', say("'I seen it already, son. Go on.'")),
               "Silas holds the pass up to his lamp, then up to your face, then back to the lamp. 'Don't look much "
               "like you.' He hands it back. 'Then again, nobody looks like their picture at this hour.' He works the "
               "gate open with a long screech. 'Go on. And son -- whatever's going on in Thirteen tonight, I didn't "
               "see you.'\n",
               ('set', 'silas_ok', 1), call('Award', 10), ('rtrue',)]),
           ('if', ('==', 'noun', money, nickel), say("'Put that away. I'm sixty-eight years old. There's nothing "
                                                       "left I want to buy.'")),
           "Silas glances at it. 'That ain't a pass.'\n"))
before(gate,
       ('if', ('and', ('==', 'action', 'GO'), ('==', 'dir', 'D_E', 'D_IN'), ('not', 'silas_ok')), [
           "Silas raises a hand without looking up from his racing form. 'Pier's closed, son. You got a pass?'\n",
           ('rtrue',)]))
before(fence, on('CLIMB')("Barbed wire, a bad back and a watchman with a shotgun under his blanket. No.\n"),
       on('OPEN')(('if', 'silas_ok', say("It's open.")), "Only Silas opens that gate.\n"))
describe(gate,
         "A chain-link fence topped with barbed wire, and a gate beside a guardhouse the size of a phone booth. ",
         ('if', 'silas_ok', ["The gate stands open. Old Silas sits in the guardhouse, pointedly not seeing you."],
          ["Old Silas the night watchman sits in the guardhouse, wrapped in a blanket and reading a racing form."]),
         " Beyond the fence: the black shapes of warehouses and the masts of ships. Harbor Road is west.\n")

before(pier,
       ('if', ('and', ('==', 'action', 'GO'), ('==', 'dir', 'D_E')), [
           "Two sailors step in front of the Salamander's gangway. 'Crew only, pal.' One of them cracks his knuckles, "
           "which sounds like a tree falling over. You decide you're not crew.\n", ('rtrue',)]),
       ('if', ('and', ('==', 'action', 'ENTER'), ('==', 'noun', salamander)), [
           "The sailors at the gangway would toss you in the bay without spilling their coffee.\n", ('rtrue',)]),
       ('if', ('and', ('==', 'action', 'ENTER'), ('==', 'noun', whdoor)), [('do', ('call', 'GoTo', warehouse)),
                                                                        ('rtrue',)]))
before(bucket, on('SEARCH', 'EXAMINE')("A bucket that smells of last week's bait.",
                                       ('if', ('in', knife, pier), [' A gutting knife is stuck in its rim.']), '\n'))
describe(pier,
         "The pier stretches out into the fog on tarred pilings. Crates are stacked in leaning towers, and the black "
         "water slaps restlessly underneath. To the north looms Warehouse 13, its big doors chained, but a small side "
         "door stands ajar. East, at the end of the pier, a rust-streaked freighter wallows at her moorings -- the "
         "SALAMANDER, smoke already curling from her stack. The gate is west.\n")

# ---------------------------------------------------------------- warehouse and the finale
describe(warehouse,
         ('if', ('>=', 'climax', 2), [
             "Every lamp in the warehouse is blazing. Crates stacked to the rafters, a forklift, a puddle of oil -- "
             "and in the middle of it all, Augustus Crane with his pistol and Vivian Lark with her derringer, standing "
             "between you and the side door to the south. Eddie Lark is beside you, rubbing his wrists.\n"],
          [
              "A cavernous warehouse that smells of tar and rot. Your flashlight beam picks out crates stacked to the "
              "rafters, a forklift asleep in the shadows and lamps hanging dead from the beams.",
              ('if', 'eddie_free', [" Eddie Lark stands beside you, rubbing his wrists."],
               [" And in the middle of the floor, tied to a wooden chair and gagged, his tuxedo torn: a young man with "
                "Vivian's eyes. Eddie Lark."]),
              " The side door is south.\n",
              ('if', ('not', 'wh_seen'), [('set', 'wh_seen', 1), call('Award', 5)]),
          ]))
before(eddie,
       on('EXAMINE')(
           ('if', 'eddie_free', say("Eddie is shaking, but he's on his feet. He looks at you like you're Christmas "
                                     "morning.")),
           "Eddie Lark: Vivian's eyes in a younger, more frightened face. He's been worked over -- a split lip, a "
           "bruise blooming on one cheek. Ropes bind him to the chair at the wrists and ankles, and a gag is knotted "
           "over his mouth.\n"),
       on('FREE', 'CUT', 'TAKE')(('do', ('call', 'FreeEddie'))),
       on('TALK', 'ASK')(
           ('if', ('not', 'eddie_free'), say("Eddie's eyes go wide above the gag. 'Mmmph! Mmmph-mmph!' Which you take "
                                              "to mean: 'Untie me, you idiot.'")),
           "Eddie is too scared to speak. He just shakes his head at his sister, over and over.\n"),
       on('ATTACK', 'SHOOT')("You came here to save him, Sam. Focus.\n"))
before(ropes, on('CUT', 'FREE', 'TAKE', 'PULL', 'OPEN')(('do', ('call', 'FreeEddie'))),
       on('EXAMINE')(('if', 'eddie_free', say('Cut ropes lie around the chair like dead snakes.')),
                     "Wet, thick ropes, knotted tight. Eddie isn't going anywhere without help -- and something "
                     "sharp.\n"))

st.routine('CraneKills', (), (), [
    "Crane sighs, like a man who has been kept waiting by a waiter. 'I'm afraid we've run out of time, Mr. Decker.' "
    "He glances at Vivian. She doesn't hesitate.\n\nThe derringer is very small. It doesn't need to be big.\n\nThe "
    "last thing you hear is the Salamander's horn, calling across the water like a lonely trumpet.\n",
    ('set', 'deadflag', 1),
])
before(crane,
       on('SHOOT')(
           ('if', ('notin', revolver, player), say("Your gun is somewhere else. Crane is right here.")),
           ('if', ('not', 'loaded'), [
               "You pull the .38 and squeeze. Click. Crane laughs, a warm, delighted laugh. Vivian doesn't.\n",
               ('rtrue',)]),
           ('if', 'police_called', [
               "Your .38 speaks before Crane's pistol can. The pearl-handled gun goes flying, and Crane goes down "
               "clutching a ruined hand, screaming like a teakettle.\n", ('rtrue',)]),
           "Your .38 speaks before Crane's pistol can. The pearl-handled gun goes flying, and Crane goes down "
           "clutching a ruined hand, screaming like a teakettle. Vivian's derringer barks -- a bullet whines past "
           "your ear -- and then she's gone through the side door in a flash of silver fox.\n\nBy the time you've "
           "hauled Eddie out onto the pier, the Salamander is already sliding away into the fog, her running lights "
           "winking out one by one. Somewhere on her deck, Vivian Lark is watching you go. You'd bet your license on "
           "it.\n\nCaptain O'Rourke arrives an hour later, pale and furious, to find the Harbor Commissioner tied up "
           "with his own necktie, and a ledger that will keep the courts busy until 1960.\n\nIt's a win. Mostly. But "
           "some nights, when it rains, you'll still hear that voice of smoke and honey.\n",
           call('Award', 10), ('set', 'deadflag', 3)),
       on('GIVE')(('if', ('==', 'noun', ledger), [
           ('if', 'police_called', [
               "Crane takes the ledger, tucks it under his arm and smiles at you with genuine warmth. 'Thank you, Mr. "
               "Decker. You've been a great help.' He raises the pistol.\n", ('rtrue',)]),
           "Crane takes the ledger, tucks it under his arm and smiles at you with genuine warmth. 'Thank you, Mr. "
           "Decker. You've been a great help.' He nods to Vivian.\n\nThe derringer is very small. It doesn't need to "
           "be big.\n", ('remove', ledger), ('set', 'deadflag', 1), ('rtrue',)]),
           "Crane doesn't even look at it. 'The ledger, Mr. Decker.'\n"),
       on('TALK', 'ASK')(
           ('if', ('==', 'second', vivian), say("'Vivian?' Crane smiles. 'Vivian understands that a voice like hers "
                                                 "deserves a bigger stage than the Blue Lantern. I'm giving her the "
                                                 "whole harbor.'")),
           ('if', ('==', 'second', ledger), say("'Names, numbers, a little honest graft. Nothing a reasonable man "
                                                 "couldn't forgive. Unfortunately, judges aren't reasonable men.'")),
           "'You could have stayed home tonight, Mr. Decker,' Crane says pleasantly. 'Most men in your profession "
           "do. That's why they live to be old men in your profession.'\n"),
       on('ATTACK')(
           ('if', 'police_called', say("You take one step toward Crane. Vivian's derringer follows you like a compass "
                                        "needle. You stop.")),
           "You lunge for Crane. You almost make it.\n\nThe derringer is very small. It doesn't need to be big.\n",
           ('set', 'deadflag', 1)))
before(vivian,
       on('SHOOT')(
           ('if', ('or', ('notin', revolver, player), ('not', 'loaded')), [('set', 'noun', crane),
                                                                          ('ret', ('call', 'B_%d' % crane.num))]),
           "You swing the .38 toward her. Her eyes meet yours over the barrel, and for a second it's just the two of "
           "you and the rain on the roof. You can't make your finger move. Not at her.\n",
           ('if', ('not', 'police_called'), [
               "\nThat half-second is all Crane needs.\n", ('set', 'deadflag', 1)])),
       on('TALK', 'ASK')(
           "'Why, Viv?'\n\nShe shrugs, and the silver fox shrugs with her. 'A girl gets tired of singing for tips, "
           "Sam. Augustus offered me the whole harbor. And Eddie --' Her voice catches, just for a moment. 'Eddie "
           "was supposed to keep his mouth shut.'\n"),
       on('KISS')("'Not now, Sam,' she says softly, and the derringer doesn't waver an inch.\n"),
       on('GIVE')(('if', ('==', 'noun', ledger), [('set', 'second', crane), ('ret', ('call', 'B_%d' % crane.num))]),
                  "She doesn't take her eyes off you.\n"),
       on('ATTACK')(('set', 'noun', crane), ('ret', ('call', 'B_%d' % crane.num))))
before(junction,
       on('SHOOT')(
           ('if', ('or', ('notin', revolver, player), ('not', 'loaded')), [('set', 'noun', crane),
                                                                          ('ret', ('call', 'B_%d' % crane.num))]),
           ('if', 'police_called', [
               "You put a bullet into the junction box. Sparks, a bang, and every lamp in the warehouse dies at once. "
               "In the dark, Crane is swearing and Vivian is calling your name.\n", ('rtrue',)]),
           "You swing the .38 away from Crane and put a bullet into the junction box. Sparks, a flash, a bang -- and "
           "every lamp in the warehouse dies at once.\n\nIn the sudden black, you grab Eddie by the collar and run. "
           "Crane's pistol flashes twice behind you, punching holes in the dark. Then you're out through the side "
           "door, down the pier, past the gate, past Old Silas -- who doesn't see a thing -- and into the fog.\n\nAt "
           "dawn you walk into Central with Eddie Lark and the ledger. By then the Salamander is a smudge on the "
           "horizon, and Augustus Crane and Vivian Lark are on it, toasting each other with champagne paid for by the "
           "taxpayers of Port Halcyon.\n\nYou saved the kid. You saved the book. The rest will have to wait for "
           "another rainy night.\n",
           call('Award', 5), ('set', 'deadflag', 3)),
       on('ATTACK', 'PUSH', 'PULL', 'SWITCHOFF')("It's behind Vivian. You'd never reach it. A bullet would.\n"))
before(warehouse,
       ('if', ('and', ('>=', 'climax', 2), ('==', 'action', 'GO')), [
           "Vivian steps into your path, the derringer level with your heart. 'Don't, Sam.'\n", ('rtrue',)]),
       ('if', ('and', ('>=', 'climax', 2), ('==', 'action', 'WAIT', 'TALK', 'THINK', 'SING')), [
           ('if', ('==', 'action', 'TALK'), [('rfalse',)]),
           "You stall. You talk about the weather, the rain, the Dodgers' bullpen. Crane listens with a polite "
           "patience that you can see running out, grain by grain.\n", ('rtrue',)]),
       ('if', ('and', ('>=', 'climax', 2), ('==', 'action', 'SWITCHOFF'), ('==', 'noun', flashlight)), [
           "Switching off your flashlight doesn't do much now that every lamp in the place is on.\n", ('rtrue',)]))

# ====================================================================== daemons, help, main loop

st.routine('EndTurn', (), (), [
    ('inc', 'moves'),
    ('if', 'deadflag', [('rtrue',)]),
    # Rico arrives the turn after the ledger is taken, and strikes the turn after that
    ('if', ('==', 'rico_timer', 2), [
        ('set', 'rico_timer', 3),
        ('if', ('and', ('in', rico, room6), ('==', 'location', room6)), [
            "\nRico moves faster than a man his size has any right to. There's a flash of steel, a sudden cold "
            "feeling, and then you're lying on the floor of room 6, looking up at the ceiling. The feathers drift down "
            "around you like snow.\n",
            ('set', 'deadflag', 1), ('rtrue',)]),
        ('remove', rico),
    ]),
    ('if', ('==', 'rico_timer', 1), [
        ('set', 'rico_timer', 2), ('move', rico, room6),
        "\nBehind you, a floorboard creaks.\n\nYou turn. Filling the doorway is a big man in a camel-hair coat, with "
        "a white scar running from his ear to the corner of his mouth like a second smile. Rico 'the Knife' "
        "Salvatore. A switchblade snicks open in his hand.\n\n'I'll take that book, shamus,' he says. 'And then I'll "
        "take my time.'\n",
    ]),
    # the finale
    ('if', ('==', 'climax', 1), [
        ('set', 'climax', 2),
        ('move', crane, warehouse), ('move', vivian, warehouse), ('move', junction, warehouse),
        ('ungive', warehouse, 'DARK'),
        "\n'Sam Decker? Viv sent you?' Eddie gasps. 'Oh God, listen to me -- it was never--'\n\nThe overhead lamps "
        "slam on, one after another, BANG, BANG, BANG, until the warehouse is bright as an operating room.\n\n'--never "
        "about me,' Eddie whispers.\n\nAugustus Crane stands by the side door in a white suit that has never seen "
        "rain, a pearl-handled pistol in his manicured hand. And beside him, wrapped in silver fox, a tiny derringer "
        "glinting in her glove, stands Vivian Lark.\n\n'Hello, Sam,' she says. 'I'm sorry. Truly. Eddie hid the "
        "ledger and wouldn't tell us where, and I knew you'd find it. You're very good at finding things.' Her smile "
        "is a razor wrapped in velvet. 'It's the only thing you're good at.'\n\n",
        ('if', 'letter_read', ["You think of the letter in her dressing room. 'Find the one, and I'll close the "
                               "other.' You should have listened to yourself.\n\n"]),
        "'The ledger, Mr. Decker,' says Crane pleasantly, 'if you'd be so kind. And then perhaps we can all go home. "
        "Some of us, anyway.'\n",
        ('rtrue',),
    ]),
    ('if', ('>=', 'climax', 2), [
        ('if', 'police_called', [('do', ('call', 'BestEnding')), ('rtrue',)]),
        ('inc', 'climax'),
        ('if', ('==', 'climax', 3), ["\nCrane checks his pocket watch. 'I'm a patient man, Mr. Decker. The tide is "
                                    "not.'\n"]),
        ('if', ('>=', 'climax', 4), [('nl',), ('do', ('call', 'CraneKills'))]),
        ('rtrue',),
    ]),
    # the Salamander sails at four
    ('if', ('==', 'moves', 260), [
        "\nSomewhere out in the fog, a ship's horn moans, long and low. Four o'clock. The Salamander is sailing -- and "
        "Eddie Lark is aboard, in the dark, in a crate marked MACHINE PARTS. You were too late.\n",
        ('set', 'deadflag', 4)]),
    ('if', ('==', 'moves', 200), ["\nFar off, a church bell strikes three. One hour until the Salamander sails.\n"]),
])

st.routine('Hint', (), (), [
    ('style', 2), '[Hint] ', ('style', 0),
    ('if', ('>=', 'climax', 2), [
        ('if', 'police_called', say("Keep them talking. Help is on its way -- you made sure of that.")),
        ('if', 'loaded', say("A loaded .38 can change a conversation. Shoot Crane... or shoot the lights.")),
        *say("This is bad. With an empty gun there's not much you can do. (Try UNDO a few times: load your revolver, "
             "and call the police before you come here.)")]),
    ('if', ('in', rico, room6), [
        ('if', 'loaded', say("Shoot Rico -- or get out through the window. Now!")),
        *say("Get out through the window (GO OUT). Now!")]),
    ('if', ('not', 'key_found'), say("Vivian said Eddie told her 'the key is in the music'. Have you looked closely at the "
                                     "locket she gave you? (EXAMINE LOCKET)")),
    ('if', ('not', 'piano_open'), [
        ('if', ('not', 'got_roomkey'), [
            ('if', ('not', 'gus_paid'), say("Eddie rents room 6 at the Calloway Hotel, west of Mercer Street, but the "
                                            "night clerk wants money. Gus, the bartender at the Blue Lantern (east of "
                                            "Mercer Street), owes you twenty bucks: TALK TO GUS.")),
            *say("Give the twenty dollars to the night clerk at the Calloway Hotel.")]),
        *say("Eddie's room is upstairs at the Calloway. 'The key is in the music' -- try UNLOCK PIANO.")]),
    ('if', ('not', 'ledger_taken'), say('Take the ledger from the piano.')),
    ('if', ('not', 'police_called'), say("You have proof now. CALL POLICE: there's a telephone in your office and a "
                                         "payphone on Harbor Road (it takes your nickel). And is your revolver loaded? "
                                         "Look in your filing cabinet.")),
    ('if', ('not', 'silas_ok'), [
        ('if', ('not', 'mirror_read'), say("Head for Pier 9, east of Harbor Road. Silas wants to see a pass -- you have "
                                           "one. (Want to know what you're walking into? Vivian's dressing room at the "
                                           "Blue Lantern is worth a look. Moose might let you in if you SHOW him the "
                                           "LOCKET.)")),
        *say("Pier 9 is east of Harbor Road. SHOW PASS TO SILAS.")]),
    ('if', ('not', 'eddie_free'), [
        ('if', ('hasnt', flashlight, 'ON'), say("Warehouse 13 is pitch dark. Your flashlight is in your desk drawer -- "
                                                "TURN ON FLASHLIGHT.")),
        *say("Eddie is tied up. You need something sharp: there's a knife on the pier. Then CUT ROPES.")]),
    'Keep going, Sam.\n',
])

st.routine('Help', (), (), [
    ('style', 2), 'How to play\n', ('style', 0),
    "This is a text adventure. You read what happens, then type what you want to do in plain English, like:\n\n"
    "  LOOK, EXAMINE DESK, OPEN DRAWER, TAKE REVOLVER, INVENTORY (or I)\n"
    "  NORTH (or N), SOUTH, EAST, WEST, UP, DOWN, IN, OUT\n"
    "  TALK TO GUS, ASK GUS ABOUT EDDIE, SHOW LOCKET TO MOOSE, GIVE MONEY TO CLERK\n"
    "  UNLOCK DOOR WITH KEY, TURN ON FLASHLIGHT, CALL POLICE, SHOOT ...\n\n"
    "Other useful commands: HINT (when you're stuck), UNDO (take back your last move), SAVE and RESTORE (in this "
    "browser), SCORE, AGAIN (or G) and RESTART.\n\nEvery move takes a minute of story time. The Salamander sails at "
    "4 AM. Don't be late.\n",
])
st.routine('About', (), (), [
    ('style', 2), 'The Blue Lantern Affair\n', ('style', 0),
    "A noir text adventure for the Z-machine, the virtual computer Infocom built in 1979 to run Zork and its "
    "siblings. This story file runs on any Z-machine interpreter -- including the one on this page.\n\n"
    "An Invict Game Studio production for Davy Schroëder, written and built with Claude.\n",
])

st.routine('Rank', (), (), [
    'You scored ', ('pnum', 'score'), ' out of a possible 100, in ', ('pnum', 'moves'), ' turns, earning the rank of ',
    ('style', 2),
    ('if', ('>=', 'score', 100), ['Legend of Port Halcyon'],
     [('if', ('>=', 'score', 75), ['Seasoned Private Eye'],
       [('if', ('>=', 'score', 45), ['Hired Shamus'], ['Rookie Gumshoe'])])]),
    ('style', 0), '.\n',
])

st.routine('GameOver', (), ('w', 'r'), [
    ('nl',), ('style', 2),
    ('switch', 'deadflag', [
        (1, ['    *** You have died ***']),
        (2, ['    *** Case closed ***']),
        (3, ['    *** Case closed... more or less ***']),
        (4, ['    *** Too late ***']),
    ]),
    ('style', 0), '\n\n',
    ('do', ('call', 'Rank')),
    ('if', ('==', 'deadflag', 3), ["(There's a better ending. Did you call for backup?)\n"]),
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
st.glob('text_a')
st.glob('parse_a')

st.routine('Banner', (), (), [
    ('style', 2), 'THE BLUE LANTERN AFFAIR\n', ('style', 0),
    'A Port Halcyon mystery in one long night\n',
    'Release 1 / Serial number 261108 / Invict Game Studio\n',
    'Type HELP if you are new to text adventures, or HINT if you get stuck.\n',
])

st.routine('Main', (), ('u', 'r'), [
    ('set', 'text_a', ('call', 'TextAddr')),
    ('set', 'parse_a', ('call', 'ParseAddr')),
    ('erase', -1),
    ('set', 'location', office),
    ('set', 'moves', 0),
    ('do', ('call', 'DrawStatus')),
    "\n\n\nPort Halcyon, 1949. The rain has been falling for three days, like the sky is trying to wash the city "
    "clean and losing.\n\nYou are Sam Decker, private investigator: two hundred pounds of bad luck in a trench coat, "
    "with a license on the wall, a bottle in the desk and nothing much in between.\n\nIt's 11:39 PM when the door of "
    "your office flies open and a woman walks in out of the rain like she owns it. You know that face. Everybody in "
    "Port Halcyon knows that face: Vivian Lark, the voice of the Blue Lantern.\n\n'Mr. Decker,' she says, and her "
    "voice is smoke and honey. 'My brother Eddie is missing. He plays piano at the Lantern. Two nights ago he told "
    "me he'd seen something down at the docks. Something about a ledger. Then he was gone.'\n\nShe presses a silver "
    "locket into your palm. Her fingers are ice.\n\n'Eddie gave me this. He said if anything happened to him, the "
    "key is in the music. I don't know what that means. They're going to put him on a boat, Mr. Decker. Before "
    "dawn. Please.'\n\nDown on Mercer Street a car horn barks twice -- and she's gone, a swirl of gardenia perfume "
    "and a door swinging on its hinges.\n\nYou look at the clock. 11:40. Somewhere out there, the night is waiting "
    "for you.\n\n",
    ('do', ('call', 'Banner')),
    ('do', ('call', 'LookRoom')),
    ('while', 1, [
        ('if', 'deadflag', [('do', ('call', 'GameOver'))]),
        ('do', ('call', 'DrawStatus')),
        '\n> ',
        ('do', ('aread', 'text_a', 'parse_a')),
        ('if', ('call', 'Parse'), [
            ('if', ('==', 'action', 'SCORE', 'HELP', 'ABOUT', 'SAVE', 'RESTORE', 'UNDO', 'RESTART', 'QUIT', 'HINT'), [
                ('switch', 'action', [
                    ('HELP', [('do', ('call', 'Help'))]),
                    ('ABOUT', [('do', ('call', 'About'))]),
                    ('HINT', [('do', ('call', 'Hint'))]),
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

st.routine('StatusRight', ('cols',), ('m', 'h', 'x'), [
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
])

build_library(player, flashlight, msg={
    'dark': "It's as black as a banker's heart in here. You can't see a thing.",
    'talk_thing': "You've been alone too long, Sam. It doesn't talk back.",
    'ask_thing': "You'd get more out of a lamppost.",
    'sit': "There's no time to sit down. Eddie doesn't have time.",
    'listen': 'Rain. Always the rain.',
    'smell': 'Wet city: tar, cigarette smoke and the sea.',
    'wait': "Time passes. The rain doesn't.",
    'kiss': 'This is no time for romance, Sam.',
    'xyzzy': "A hollow voice says: 'Wrong genre, gumshoe.'",
    'sing': "You hum a few bars of 'Stormy Weather'. The rain seems to agree with every word.",
    'smoke': 'You quit in 1946. Mostly.',
}, shoot=[
    ('if', ('notin', revolver, player), ['You\'d need a gun in your hand for that.\n', ('rfalse',)]),
    ('if', ('==', 'loaded', 0), ['Click. The revolver is empty. You forgot to load it, genius.\n', ('rfalse',)]),
    "You've only got six bullets. Save them for something that deserves it.\n",
])

# addresses of the buffers, so Main can use them through globals
from lib import TEXT, PARSE
st.routine('TextAddr', (), (), [('ret', TEXT)])
st.routine('ParseAddr', (), (), [('ret', PARSE)])

data = st.compile()
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'stories', 'blue-lantern.z5')
with open(out, 'wb') as f:
    f.write(data)
print('wrote', os.path.normpath(out), len(data), 'bytes,', len(st.objs), 'objects,', len(st.order), 'routines')
