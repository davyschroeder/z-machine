"""Box art for Perihelion: writes perihelion-poster.svg and perihelion-og.svg next to this file.
Render them to public/perihelion-art.webp and public/og-perihelion.jpg with sharp (see render.js)."""
import math
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))

DEFS = '''
  <radialGradient id="dwarf" cx=".38" cy=".32" r=".8"><stop offset="0" stop-color="#ffb070"/><stop offset=".25" stop-color="#f26a35"/>
    <stop offset=".65" stop-color="#9c1f1c"/><stop offset="1" stop-color="#2a0710"/></radialGradient>
  <radialGradient id="rim" cx=".5" cy=".5" r=".5"><stop offset=".86" stop-color="#ff6a3d" stop-opacity="0"/>
    <stop offset=".97" stop-color="#ff8a5c" stop-opacity=".55"/><stop offset="1" stop-color="#ff8a5c" stop-opacity="0"/></radialGradient>
  <linearGradient id="hull" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f4f7fc"/><stop offset=".45" stop-color="#b9c2d3"/>
    <stop offset="1" stop-color="#4a5163"/></linearGradient>
  <linearGradient id="hullDark" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9aa3b5"/><stop offset="1" stop-color="#2c3140"/></linearGradient>
  <radialGradient id="ice" cx=".35" cy=".35" r=".7"><stop offset="0" stop-color="#ffffff"/><stop offset=".5" stop-color="#cfe6f7"/>
    <stop offset="1" stop-color="#6f8fae"/></radialGradient>
  <linearGradient id="plume" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#ffffff"/><stop offset=".15" stop-color="#9fd4ff"/>
    <stop offset=".6" stop-color="#5a7dff" stop-opacity=".45"/><stop offset="1" stop-color="#5a7dff" stop-opacity="0"/></linearGradient>
  <filter id="blur6"><feGaussianBlur stdDeviation="6"/></filter>
  <filter id="blur2"><feGaussianBlur stdDeviation="2"/></filter>
  <filter id="blur40" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="40"/></filter>
'''


def ellipse_arc(cx, cy, rx, ry, rot, back):
    """Half of a tilted ellipse: the back half (behind the dwarf) or the front half."""
    a0, a1 = (math.pi, 2 * math.pi) if back else (0, math.pi)
    pts = []
    for i in range(61):
        a = a0 + (a1 - a0) * i / 60
        x, y = rx * math.cos(a), ry * math.sin(a)
        c, s = math.cos(math.radians(rot)), math.sin(math.radians(rot))
        pts.append((cx + x * c - y * s, cy + x * s + y * c))
    return 'M' + ' L'.join('%.1f %.1f' % p for p in pts)


def lattice(cx, cy, r, rnd, back):
    out = []
    rr = random.Random(99)
    for i in range(10):
        rx, ry, rot = r * (1.45 + i * 0.36), r * (0.36 + i * 0.09), -12 + rr.uniform(-3, 3)
        col = rr.choice(['#ff8a6a', '#c79bff', '#9fb0ff', '#ffb38a'])
        dash = rr.choice(['none', '60 8 6 8', '140 14', '10 6', '220 6 20 6'])
        op = (0.28 if back else 0.55) * rr.uniform(.6, 1)
        d = ellipse_arc(cx, cy, rx, ry, rot, back)
        out.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-opacity="{op:.2f}" stroke-width="{rr.uniform(.8, 2.4):.1f}" '
                   f'stroke-dasharray="{dash}"/>')
        for k in range(rr.randint(1, 3)):  # glowing nodes travelling along the ring
            a = rr.uniform(math.pi, 2 * math.pi) if back else rr.uniform(0, math.pi)
            x, y = rx * math.cos(a), ry * math.sin(a)
            c, s = math.cos(math.radians(rot)), math.sin(math.radians(rot))
            px, py = cx + x * c - y * s, cy + x * s + y * c
            out.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="7" fill="{col}" opacity=".6" filter="url(#blur6)"/>'
                       f'<circle cx="{px:.1f}" cy="{py:.1f}" r="1.8" fill="#fff"/>')
    if back:
        for i in range(34):  # filaments radiating out from the dwarf
            a = rr.uniform(0, math.pi * 2)
            r1, r2 = r * rr.uniform(1.15, 1.5), r * rr.uniform(2.6, 5.4)
            out.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#ffb08a" stroke-opacity="%.2f" stroke-width=".7"/>' % (
                cx + r1 * math.cos(a), cy + r1 * math.sin(a) * .3, cx + r2 * math.cos(a), cy + r2 * math.sin(a) * .3,
                rr.uniform(.06, .22)))
    return ''.join(out)


def dwarf(cx, cy, r):
    bands = ''.join(
        f'<ellipse cx="{cx}" cy="{cy + r * o:.1f}" rx="{r * 1.05:.1f}" ry="{r * w:.1f}" fill="{c}" opacity="{a}"/>'
        for o, w, c, a in [(-.55, .07, '#ffcf9a', .1), (-.3, .1, '#5a0f14', .15), (-.05, .06, '#ffb27a', .08),
                           (.18, .12, '#4a0a12', .17), (.45, .08, '#ff9a6a', .07), (.68, .1, '#300610', .2)])
    return f'''
  <circle cx="{cx}" cy="{cy}" r="{r * 2.4}" fill="#ff5a3d" opacity=".22" filter="url(#blur40)"/>
  <clipPath id="dclip"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>
  <circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#dwarf)"/>
  <g clip-path="url(#dclip)" filter="url(#blur2)">{bands}</g>
  <circle cx="{cx}" cy="{cy}" r="{r * 1.04}" fill="url(#rim)"/>'''


def ship(x, y, s, rot):
    """The ark, bow (ice shield) to the left, fusion torch to the right."""
    windows = ''.join(f'<rect x="{-62 + i * 8}" y="-62" width="3" height="2" fill="#ffd9a0" opacity=".9"/>' for i in range(0))
    ring_lights = ''.join(
        f'<circle cx="{-40 + 16 * math.cos(a):.1f}" cy="{70 * math.sin(a):.1f}" r="1.6" fill="#ffd9a0"/>'
        for a in [i * math.pi / 9 for i in range(18)] if math.cos(a) > -0.2)
    trusses = ''.join(f'<line x1="{-120 + i * 18}" y1="-6" x2="{-111 + i * 18}" y2="6" stroke="#5c6476" stroke-width="1"/>'
                      for i in range(16))
    return f'''
  <g transform="translate({x} {y}) rotate({rot}) scale({s})">
    <!-- the torch has been cold for 260 years: only a faint glow of the habitat lights -->
    <ellipse cx="-40" cy="0" rx="26" ry="80" fill="#ffcf8a" opacity=".12" filter="url(#blur6)"/>
    <!-- radiator fins -->
    <path d="M120 -8 L150 -60 L176 -60 L150 -8 Z" fill="url(#hullDark)" opacity=".95"/>
    <path d="M120 8 L150 60 L176 60 L150 8 Z" fill="#3a4152"/>
    <!-- spine -->
    <rect x="-150" y="-7" width="330" height="14" rx="4" fill="url(#hull)"/>
    {trusses}
    <!-- cryo drums -->
    <rect x="30" y="-22" width="34" height="44" rx="6" fill="url(#hull)"/><rect x="30" y="-22" width="34" height="5" rx="2" fill="#ffffff" opacity=".6"/>
    <rect x="72" y="-22" width="34" height="44" rx="6" fill="url(#hull)"/><rect x="72" y="-22" width="34" height="5" rx="2" fill="#ffffff" opacity=".6"/>
    <line x1="47" y1="-22" x2="47" y2="22" stroke="#3a4152" stroke-width="1.5"/><line x1="89" y1="-22" x2="89" y2="22" stroke="#3a4152" stroke-width="1.5"/>
    <!-- engine bell -->
    <path d="M176 -10 L200 -22 L200 22 L176 10 Z" fill="url(#hullDark)"/>
    <!-- habitat ring: back half, spokes, front half -->
    <path d="M-40 -70 A16 70 0 0 0 -40 70" fill="none" stroke="#6b7386" stroke-width="11"/>
    <line x1="-40" y1="-66" x2="-40" y2="66" stroke="#8c95a8" stroke-width="3"/>
    <line x1="-46" y1="-40" x2="-34" y2="40" stroke="#8c95a8" stroke-width="2"/>
    <path d="M-40 -70 A16 70 0 0 1 -40 70" fill="none" stroke="url(#hull)" stroke-width="12"/>
    {ring_lights}
    <!-- the ice shield at the bow -->
    <ellipse cx="-168" cy="0" rx="30" ry="36" fill="url(#ice)"/>
    <ellipse cx="-176" cy="-10" rx="10" ry="14" fill="#ffffff" opacity=".55" filter="url(#blur2)"/>
  </g>'''


def scene(w, h, cx, cy, r, seed, ship_xy, ship_s, ship_rot, tether_to, title):
    rnd = random.Random(seed)
    stars = ''.join('<circle cx="%.1f" cy="%.1f" r="%.2f" fill="%s" fill-opacity="%.2f"/>' % (
        rnd.uniform(0, w), rnd.uniform(0, h), rnd.choice([0.5, 0.6, 0.8, 1.1, 1.5]),
        rnd.choice(['#ffffff', '#ffffff', '#cfd8ff', '#ffe2c8']), rnd.uniform(0.25, 0.95)) for _ in range(int(w * h / 1100)))
    nebula = ''.join(f'<circle cx="{nx}" cy="{ny}" r="{nr}" fill="{nc}" opacity="{no}" filter="url(#blur40)"/>'
                     for nx, ny, nr, nc, no in [(w * .15, h * .2, w * .3, '#5b2a8c', .22), (w * .85, h * .7, w * .32, '#2a3a8c', .2),
                                                (w * .7, h * .12, w * .2, '#8c2a4a', .16)])
    sx, sy = ship_xy
    tx, ty = tether_to
    tether = (f'<line x1="{sx}" y1="{sy}" x2="{tx}" y2="{ty}" stroke="#e2c8ff" stroke-opacity=".5" stroke-width="1.4"/>'
              f'<line x1="{sx}" y1="{sy}" x2="{tx}" y2="{ty}" stroke="#c79bff" stroke-opacity=".35" stroke-width="5" filter="url(#blur2)"/>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  <defs>{DEFS}</defs>
  <rect width="{w}" height="{h}" fill="#04040b"/>
  {nebula}
  <g>{stars}</g>
  {lattice(cx, cy, r, rnd, True)}
  {dwarf(cx, cy, r)}
  {lattice(cx, cy, r, rnd, False)}
  {tether}
  {ship(sx, sy, ship_s, ship_rot)}
  {title}
</svg>'''


def poster():
    w, h = 840, 1180
    title = f'''
  <rect y="{h * .78}" width="{w}" height="{h * .22}" fill="#04040b" opacity=".5" filter="url(#blur40)"/>
  <text x="{w / 2}" y="{h * 0.865}" text-anchor="middle" font-family="Inter Display" font-weight="900" font-size="96" letter-spacing="10" fill="#f3f1f8">PERIHELION</text>
  <text x="{w / 2}" y="{h * 0.92}" text-anchor="middle" font-family="Inter Display" font-weight="700" font-size="27" letter-spacing="9" fill="#c79bff">A CHRONICLE OF THE LONG DRIFT</text>
  <text x="{w / 2}" y="{h * 0.958}" text-anchor="middle" font-family="DejaVu Sans Mono" font-size="19" letter-spacing="3" fill="#8a85a0">SHIP-YEAR 412 · A TEXT ADVENTURE</text>'''
    return scene(w, h, w * .56, h * .33, 118, 412, (w * .36, h * .62), 1.1, -18, (w * .56 + 150, h * .33 + 40), title)


def og():
    w, h = 1200, 630
    title = '''<rect width="600" height="630" fill="#04040b" opacity=".6" filter="url(#blur40)"/>
  <text x="70" y="150" font-family="DejaVu Sans Mono" font-size="26" fill="#c79bff">&gt; text adventure · Z-machine</text>
  <text x="66" y="265" font-family="Inter Display" font-weight="900" font-size="96" fill="#f3f1f8">Perihelion</text>
  <text x="70" y="340" font-family="Inter" font-size="30" fill="#a8a3bd">A derelict ark. An alien song.</text>
  <text x="70" y="382" font-family="Inter" font-size="30" fill="#a8a3bd">Nineteen chapters of lore.</text>
  <text x="70" y="560" font-family="Inter Display" font-weight="700" font-size="28" fill="#ff8a6a">davyschroeder.nl</text>'''
    return scene(w, h, 900, 250, 92, 7, (800, 470), .62, -16, (980, 290), title)


if __name__ == '__main__':
    for name, svg in (('perihelion-poster.svg', poster()), ('perihelion-og.svg', og())):
        open(os.path.join(HERE, name), 'w').write(svg)
    print('wrote perihelion-poster.svg and perihelion-og.svg')
