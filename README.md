# Z-machine stories

Text adventures for the **Z-machine**, the virtual computer Infocom invented in 1979 to run Zork on every home
computer of the day. A game is a single story file that plays in any Z-machine interpreter, from a phone to a
Raspberry Pi.

An Invict Game Studio project by Davy Schroëder, built with Claude.

## Stories

| File | Game | Version |
| --- | --- | --- |
| [`stories/perihelion.z5`](stories/perihelion.z5) | **Perihelion**: a science-fiction text adventure with a lot of lore (English). You wake from cryosleep on the ark Perihelion, 412 years after it left a dying Earth. The crew is gone, the ship's mind lies in three pieces, and an alien structure outside is singing. A codex of nineteen lore chapters, four endings, 100 points. | Z-machine v5 |
| [`stories/blue-lantern.z5`](stories/blue-lantern.z5) | **The Blue Lantern Affair**: a noir text adventure (English). Port Halcyon, 1949. You are private investigator Sam Decker, a singer's brother has vanished, and the ship that will carry him off sails at four in the morning. Four endings, 100 points, hints and undo. | Z-machine v5 |

**Play them in your browser:** [Perihelion](https://davyschroeder.nl/perihelion.html) ·
[The Blue Lantern Affair](https://davyschroeder.nl/blue-lantern.html)

Or download a `.z5` file and open it in any interpreter, such as Frotz (Linux, also on a Raspberry Pi:
`sudo apt install frotz`, then `frotz blue-lantern.z5`), Lectrote, Gargoyle or Parchment.

## What's in here

- `stories/`: the compiled story files (the "ROMs").
- `src/zcompile.py`: a small compiler that turns a Python-embedded language into Z-machine version 5 story files.
- `src/lib.py`: the adventure library: parser, scope, default verbs, status line, undo/save.
- `src/blue_lantern.py`: The Blue Lantern Affair.
- `src/perihelion.py`: Perihelion, including its codex of lore entries.
- `interpreter/zmachine.js`: a Z-machine interpreter in JavaScript (versions 3, 4, 5, 7 and 8), the one used on the
  website. It has no dependencies; the page supplies the screen through a small `io` object.
- `tests/play.js`: play a story from the command line with Node. `tests/walkthrough.txt` (The Blue Lantern Affair)
  and `tests/perihelion-walkthrough.txt` are full routes to 100 points: spoilers!
- `art/`: the box art and the scripts that draw it.

All stories are in English.

## Building

```sh
cd src
python3 blue_lantern.py                 # writes stories/blue-lantern.z5
python3 perihelion.py                   # writes stories/perihelion.z5
cd ..
node tests/play.js stories/blue-lantern.z5 -f tests/walkthrough.txt
node tests/play.js stories/perihelion.z5 -f tests/perihelion-walkthrough.txt
```

Needs Python 3 and (for the test) Node.js. Nothing else.
