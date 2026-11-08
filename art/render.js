// Renders poster.svg and og.svg (made by poster.py) into the site's images. Needs sharp.
const sharp = require(process.env.SHARP || "sharp");
const path = require("path");
const pub = __dirname;
(async () => {
  await sharp(path.join(__dirname, "poster.svg")).webp({ quality: 82 }).toFile(path.join(pub, "blue-lantern-art.webp"));
  await sharp(path.join(__dirname, "poster.svg")).resize(420).webp({ quality: 80 }).toFile(path.join(pub, "blue-lantern-art-sm.webp"));
  await sharp(path.join(__dirname, "og.svg")).jpeg({ quality: 84 }).toFile(path.join(pub, "og-blue-lantern.jpg"));
  console.log("rendered");
})();
