"""Box art for Perihelion: writes perihelion-poster.svg and perihelion-og.svg next to this file.
Render with: node render.js perihelion"""
import math
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))


def scene(w, h, cx, cy, r, rnd, ship_x, ship_y, ship_s, title):
    stars = ''.join('<circle cx="%.1f" cy="%.1f" r="%.2f" fill="#fff" fill-opacity="%.2f"/>' % (
        rnd.uniform(0, w), rnd.uniform(0, h), rnd.choice([0.5, 0.7, 0.9, 1.3]), rnd.uniform(0.2, 0.9)) for _ in range(int(w * h / 1400)))
    rings = []
    for i in range(9):  # the Lattice: tilted rings within rings around the Anvil
        rx, ry, rot = r * (1.5 + i * 0.42), r * (0.42 + i * 0.13), -14 + rnd.uniform(-5, 5)
        rings.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" transform="rotate(%.1f %.1f %.1f)" fill="none" '
                     'stroke="%s" stroke-opacity="%.2f" stroke-width="%.1f" stroke-dasharray="%s"/>' % (
                         cx, cy, rx, ry, rot, cx, cy, rnd.choice(['#ff7a5c', '#c98bff', '#9aa8ff']), rnd.uniform(.18, .5),
                         rnd.uniform(.8, 2.2), rnd.choice(['', '40 6 4 6', '120 10', '6 4'])))
    for i in range(26):  # filaments
        a = rnd.uniform(0, math.pi * 2)
        r1, r2 = r * rnd.uniform(1.2, 1.6), r * rnd.uniform(2.6, 5.2)
        rings.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#ff9a7a" stroke-opacity="%.2f" stroke-width=".8"/>' % (
            cx + r1 * math.cos(a), cy + r1 * math.sin(a) * .35, cx + r2 * math.cos(a), cy + r2 * math.sin(a) * .35, rnd.uniform(.08, .3)))
    sx, sy, s = ship_x, ship_y, ship_s
    ship = f'''
  <line x1="{sx}" y1="{sy}" x2="{cx + r * 1.6}" y2="{cy + r * .2}" stroke="#d6b8ff" stroke-opacity=".55" stroke-width="1.2"/>
  <g transform="translate({sx} {sy}) rotate(-24) scale({s})">
    <rect x="-150" y="-5" width="300" height="10" rx="3" fill="#cfd6e4"/>
    <rect x="-150" y="-5" width="300" height="4" fill="#ffffff" fill-opacity=".55"/>
    <ellipse cx="-160" cy="0" rx="22" ry="26" fill="#e9eef7"/>
    <ellipse cx="-30" cy="0" rx="16" ry="58" fill="none" stroke="#cfd6e4" stroke-width="7"/>
    <ellipse cx="40" cy="0" rx="9" ry="34" fill="none" stroke="#aeb7c8" stroke-width="5"/>
    <ellipse cx="80" cy="0" rx="9" ry="34" fill="none" stroke="#aeb7c8" stroke-width="5"/>
    <path d="M150 -12 L176 -26 L176 26 L150 12 Z" fill="#8e98ab"/>
    <ellipse cx="190" cy="0" rx="30" ry="9" fill="#9fd0ff" fill-opacity=".35"/>
  </g>'''
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  <defs>
    <radialGradient id="bg" cx="{cx / w}" cy="{cy / h}" r="1"><stop offset="0" stop-color="#1d0b14"/><stop offset=".6" stop-color="#07060f"/><stop offset="1" stop-color="#020208"/></radialGradient>
    <radialGradient id="dwarf" cx=".4" cy=".35" r=".75"><stop offset="0" stop-color="#ff7a3d"/><stop offset=".55" stop-color="#b3261e"/><stop offset="1" stop-color="#3a0a10"/></radialGradient>
    <radialGradient id="halo" cx="{cx}" cy="{cy}" r="{r * 2.6}" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#ff5a3d" stop-opacity=".45"/><stop offset="1" stop-color="#ff5a3d" stop-opacity="0"/></radialGradient>
  </defs>
  <rect width="{w}" height="{h}" fill="url(#bg)"/>
  <g>{stars}</g>
  <circle cx="{cx}" cy="{cy}" r="{r * 2.6}" fill="url(#halo)"/>
  <g>{''.join(rings[:len(rings) // 2])}</g>
  <circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#dwarf)"/>
  <g>{''.join(rings[len(rings) // 2:])}</g>
  {ship}
  {title}
</svg>'''


def poster():
    w, h = 840, 1180
    title = f'''<text x="{w / 2}" y="{h * 0.86}" text-anchor="middle" font-family="Inter Display" font-weight="900" font-size="92" letter-spacing="10" fill="#f3f1f8">PERIHELION</text>
  <text x="{w / 2}" y="{h * 0.915}" text-anchor="middle" font-family="Inter Display" font-weight="700" font-size="28" letter-spacing="9" fill="#c98bff">A CHRONICLE OF THE LONG DRIFT</text>
  <text x="34" y="52" font-family="DejaVu Sans Mono" font-size="22" fill="#9a95ab">SHIP-YEAR 412</text>
  <text x="{w - 34}" y="52" text-anchor="end" font-family="DejaVu Sans Mono" font-size="22" fill="#9a95ab">&gt; TEXT ADVENTURE_</text>'''
    return scene(w, h, w * .5, h * .4, 120, random.Random(412), w * .3, h * .66, .95, title)


def og():
    w, h = 1200, 630
    title = '''<rect width="560" height="630" fill="#02030a" fill-opacity=".55"/>
  <text x="70" y="150" font-family="DejaVu Sans Mono" font-size="26" fill="#c98bff">&gt; text adventure · Z-machine</text>
  <text x="66" y="265" font-family="Inter Display" font-weight="900" font-size="96" fill="#f3f1f8">Perihelion</text>
  <text x="70" y="340" font-family="Inter" font-size="30" fill="#9a95ab">A derelict ark. An alien song.</text>
  <text x="70" y="382" font-family="Inter" font-size="30" fill="#9a95ab">Nineteen chapters of lore.</text>
  <text x="70" y="560" font-family="Inter Display" font-weight="700" font-size="28" fill="#ff8a6a">davyschroeder.nl</text>'''
    return scene(w, h, 880, 300, 95, random.Random(7), 760, 480, .7, title)


if __name__ == '__main__':
    for name, svg in (('perihelion-poster.svg', poster()), ('perihelion-og.svg', og())):
        open(os.path.join(HERE, name), 'w').write(svg)
    print('wrote perihelion-poster.svg and perihelion-og.svg')
