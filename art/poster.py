"""Box art for The Blue Lantern Affair: writes poster.svg and og.svg next to this file.

Render them with:  node render.js   (uses sharp: public/blue-lantern-art.webp and public/og-blue-lantern.jpg)
"""
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))


def rain(rnd, w, h, n, op=(0.08, 0.35)):
    out = []
    for _ in range(n):
        x, y = rnd.uniform(-60, w), rnd.uniform(-40, h)
        ln = rnd.uniform(18, 70)
        out.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#cfe3ff" stroke-opacity="%.2f" '
                   'stroke-width="%.1f"/>' % (x, y, x + ln * 0.22, y + ln, rnd.uniform(*op), rnd.uniform(0.8, 1.8)))
    return ''.join(out)


def scene(w, h, rnd, title_block, fig_x=0.43, fig_scale=None, lantern_x=0.70, sign=True):
    """The street: brick wall, neon lantern sign, street lamp, detective silhouette, wet reflections."""
    ground = h * 0.74
    bricks = []
    for row in range(int(ground // 28) + 1):
        off = 0 if row % 2 else 40
        for col in range(-1, int(w // 80) + 2):
            if rnd.random() < 0.55:
                bricks.append('<rect x="%d" y="%d" width="76" height="24" rx="2" fill="#141a2e" fill-opacity="%.2f"/>'
                              % (col * 80 + off, row * 28, rnd.uniform(0.25, 0.7)))
    lx, ly = w * lantern_x, h * 0.25  # the lantern
    return f'''
  <defs>
    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#05060d"/><stop offset=".55" stop-color="#0b1022"/><stop offset="1" stop-color="#03040a"/>
    </linearGradient>
    <radialGradient id="glow" cx="{lx}" cy="{ly}" r="{w * 0.55}" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#3d8bff" stop-opacity=".55"/><stop offset=".35" stop-color="#1f4fd1" stop-opacity=".18"/>
      <stop offset="1" stop-color="#1f4fd1" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="lamp" cx="{w * 0.2}" cy="{h * 0.36}" r="{w * 0.42}" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#ffc46b" stop-opacity=".5"/><stop offset=".5" stop-color="#ff8a3d" stop-opacity=".12"/>
      <stop offset="1" stop-color="#ff8a3d" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="cone" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#ffd38a" stop-opacity=".35"/><stop offset="1" stop-color="#ffd38a" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="wet" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#0d1430"/><stop offset="1" stop-color="#020309"/>
    </linearGradient>
    <filter id="neon" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="soft"><feGaussianBlur stdDeviation="3"/></filter>
  </defs>
  <rect width="{w}" height="{h}" fill="url(#sky)"/>
  <g>{''.join(bricks)}</g>
  <rect width="{w}" height="{h}" fill="url(#glow)"/>
  <rect width="{w}" height="{h}" fill="url(#lamp)"/>
  <!-- the neon lantern -->
  <g filter="url(#neon)" stroke="#7fb6ff" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round">
    <path d="M{lx - 70} {ly - 150} H{lx + 70}"/>
    <path d="M{lx} {ly - 150} V{ly - 112}"/>
    <path d="M{lx - 30} {ly - 112} H{lx + 30} L{lx + 48} {ly - 88} H{lx - 48} Z"/>
    <path d="M{lx - 48} {ly - 88} L{lx - 40} {ly + 40} H{lx + 40} L{lx + 48} {ly - 88}"/>
    <path d="M{lx - 14} {ly - 88} L{lx - 12} {ly + 40} M{lx + 14} {ly - 88} L{lx + 12} {ly + 40}"/>
    <path d="M{lx - 46} {ly + 40} H{lx + 46} L{lx + 30} {ly + 62} H{lx - 30} Z"/>
  </g>
  <ellipse cx="{lx}" cy="{ly - 25}" rx="26" ry="40" fill="#bcd8ff" opacity=".55" filter="url(#soft)"/>
  <text display="{'inline' if sign else 'none'}" x="{lx}" y="{ly + 118}" text-anchor="middle" font-family="DejaVu Serif" font-style="italic" font-weight="bold"
        font-size="{w * 0.062:.0f}" fill="#d9e9ff" stroke="#5c9dff" stroke-width="1.5" filter="url(#neon)">Blue Lantern</text>
  <!-- street lamp -->
  <g fill="#05060c">
    <rect x="{w * 0.2 - 7}" y="{h * 0.36}" width="14" height="{ground - h * 0.36}"/>
    <path d="M{w * 0.2 - 34} {h * 0.36} h68 l-14 -34 h-40 z"/>
    <rect x="{w * 0.2 - 20}" y="{ground - 14}" width="40" height="14"/>
  </g>
  <ellipse cx="{w * 0.2}" cy="{h * 0.36 + 4}" rx="30" ry="9" fill="#ffd38a" filter="url(#soft)"/>
  <path d="M{w * 0.2 - 26} {h * 0.36 + 6} L{w * 0.2 - 190} {ground} H{w * 0.2 + 190} L{w * 0.2 + 26} {h * 0.36 + 6} Z"
        fill="url(#cone)"/>
  <!-- the detective -->
  <g fill="#020208" transform="translate({w * fig_x} {ground}) scale({fig_scale or w / 840:.3f})">
    <ellipse cx="0" cy="-306" rx="78" ry="13"/>
    <path d="M-44 -308 q4 -52 44 -54 q40 2 44 54 z"/>
    <path d="M-26 -300 q0 34 26 40 q26 -6 26 -40 z"/>
    <path d="M-40 -262 q40 -18 80 0 l26 40 q20 70 14 150 l-10 70 l-22 2 l-6 -60 l-12 60 h-20 l-10 -120 l-10 120
             h-20 l-12 -60 l-6 60 l-22 -2 l-10 -70 q-6 -80 14 -150 z"/>
    <path d="M-18 0 h-30 l6 -14 h22 z M18 0 h30 l-6 -14 h-22 z"/>
  </g>
  <!-- wet street with reflections -->
  <rect y="{ground}" width="{w}" height="{h - ground}" fill="url(#wet)"/>
  <g opacity=".35" filter="url(#soft)">
    <rect x="{lx - 50}" y="{ground + 8}" width="100" height="{(h - ground) * 0.7}" fill="#3d8bff"/>
    <rect x="{w * 0.2 - 40}" y="{ground + 8}" width="80" height="{(h - ground) * 0.6}" fill="#ffb35c"/>
  </g>
  <g stroke="#9cc4ff" stroke-opacity=".18" stroke-width="2">
    <line x1="0" y1="{ground + 30}" x2="{w}" y2="{ground + 26}"/><line x1="0" y1="{ground + 70}" x2="{w}" y2="{ground + 76}"/>
  </g>
  <g>{rain(rnd, w, h, int(w * h / 2600))}</g>
  {title_block}
'''


def poster():
    w, h = 840, 1180
    rnd = random.Random(1949)
    title = f'''
  <rect y="{h * 0.80}" width="{w}" height="{h * 0.2}" fill="#02030a" fill-opacity=".55"/>
  <text x="{w / 2}" y="{h * 0.853}" text-anchor="middle" font-family="Inter Display" font-weight="800" font-size="40"
        letter-spacing="14" fill="#9fc3ff">THE</text>
  <text x="{w / 2}" y="{h * 0.915}" text-anchor="middle" font-family="Inter Display" font-weight="900" font-size="78"
        letter-spacing="3" fill="#f3f1f8">BLUE LANTERN</text>
  <text x="{w / 2}" y="{h * 0.965}" text-anchor="middle" font-family="Inter Display" font-weight="800" font-size="40"
        letter-spacing="22" fill="#ff8a3d">AFFAIR</text>
  <text x="34" y="52" font-family="DejaVu Sans Mono" font-size="22" fill="#9a95ab">PORT HALCYON · 1949</text>
  <text x="{w - 34}" y="52" text-anchor="end" font-family="DejaVu Sans Mono" font-size="22" fill="#9a95ab">&gt; TEXT ADVENTURE_</text>
'''
    return '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">%s</svg>' % (
        w, h, w, h, scene(w, h, rnd, title))


def og():
    w, h = 1200, 630
    rnd = random.Random(7)
    title = f'''
  <rect width="{w * 0.58}" height="{h}" fill="#02030a" fill-opacity=".6"/>
  <text x="70" y="150" font-family="DejaVu Sans Mono" font-size="26" fill="#ff8a3d">&gt; text adventure · Z-machine</text>
  <text x="66" y="250" font-family="Inter Display" font-weight="900" font-size="84" fill="#f3f1f8">The Blue</text>
  <text x="66" y="345" font-family="Inter Display" font-weight="900" font-size="84" fill="#f3f1f8">Lantern Affair</text>
  <text x="70" y="420" font-family="Inter" font-size="30" fill="#9a95ab">A noir mystery in one long, rainy night.</text>
  <text x="70" y="462" font-family="Inter" font-size="30" fill="#9a95ab">Play it in your browser.</text>
  <text x="70" y="560" font-family="Inter Display" font-weight="700" font-size="28" fill="#9fc3ff">davyschroeder.nl</text>
'''
    return '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">%s</svg>' % (
        w, h, w, h, scene(w, h, rnd, title, fig_x=0.88, fig_scale=0.82, lantern_x=0.71, sign=False))


if __name__ == '__main__':
    for name, svg in (('poster.svg', poster()), ('og.svg', og())):
        with open(os.path.join(HERE, name), 'w') as f:
            f.write(svg)
    print('wrote poster.svg and og.svg')
