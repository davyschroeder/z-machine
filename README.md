# Z-machine stories

Text adventures for the **Z-machine**, the virtual computer Infocom invented in 1979 to run Zork on every home
computer of the day. A game is a single story file that plays in any Z-machine interpreter, from a phone to a
Raspberry Pi.

An Invict Game Studio project by Davy Schroëder, built with Claude.

## Stories

| File | Game | Version |
| --- | --- | --- |
| [`stories/blue-lantern.z5`](stories/blue-lantern.z5) | **The Blue Lantern Affair**: a noir text adventure (English). Port Halcyon, 1949. You are private investigator Sam Decker, a singer's brother has vanished, and the ship that will carry him off sails at four in the morning. Four endings, 100 points, hints and undo. | Z-machine v5 |

**Play it in your browser:** [davyschroeder.nl/blue-lantern.html](https://davyschroeder.nl/blue-lantern.html)

Or download the `.z5` file and open it in any interpreter, such as Frotz (Linux, also on a Raspberry Pi:
`sudo apt install frotz`, then `frotz blue-lantern.z5`), Lectrote, Gargoyle or Parchment.

## What's in here

- `stories/`: the compiled story files (the "ROMs").
- `src/zcompile.py`: a small compiler that turns a Python-embedded language into Z-machine version 5 story files.
- `src/lib.py`: the adventure library: parser, scope, default verbs, status line, undo/save.
- `src/blue_lantern.py`: The Blue Lantern Affair itself.
- `interpreter/zmachine.js`: a Z-machine interpreter in JavaScript (versions 3, 4, 5, 7 and 8), the one used on the
  website. It has no dependencies; the page supplies the screen through a small `io` object.
- `tests/play.js` + `tests/walkthrough.txt`: play a story from the command line with Node (spoilers in the walkthrough).
- `art/`: the box art and the script that draws it.

## Building

```sh
cd src
python3 blue_lantern.py                 # writes stories/blue-lantern.z5
cd ..
node tests/play.js stories/blue-lantern.z5 -f tests/walkthrough.txt
```

Needs Python 3 and (for the test) Node.js. Nothing else.
