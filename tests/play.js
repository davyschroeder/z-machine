// Plays a story file from the command line: node tests/play.js stories/blue-lantern.z5 -f tests/walkthrough.txt
// (or give the commands as arguments: node tests/play.js story.z5 "look" "x locket")
const fs = require("fs");
const ZMachine = require(require("path").join(__dirname, "..", "interpreter", "zmachine.js"));
let args = process.argv.slice(2);
const story = fs.readFileSync(args.shift());
let cmds = args[0] === "-f" ? fs.readFileSync(args[1], "utf8").split("\n").filter((l) => l.trim() && !l.startsWith("#")) : args;
let win = 0, out = "", status = [""], saves = {};
const io = {
  cols: 80, rows: 40,
  print(t) { if (win === 0) out += t; else { const r = status; r[0] = (r[0] + t); } },
  setStyle() {}, splitWindow() {}, setWindow(w) { win = w; if (w === 1) status = [""]; }, eraseWindow() {},
  setCursor(l, c) { if (win === 1) status[0] = status[0].padEnd(c - 1).slice(0, c - 1); }, eraseLine() {},
  requestLine() {}, requestChar() {}, quit() { out += "\n[QUIT]\n"; },
  save(k, j) { saves[k] = j; return true; }, restore(k) { return saves[k] || null; },
};
const zm = new ZMachine(story, io);
zm.run();
for (const c of cmds) {
  if (zm.halted) break;
  out += c + "\n";
  zm.line(c);
}
if (process.env.STATUS) out += "\n[STATUS: " + status[0] + "]\n";
process.stdout.write(out + "\n");
