# Generates the About cards (assets/card-*-{light,dark}.svg). Run: python tools/cards.py
from pathlib import Path
from xml.sax.saxutils import escape

H = 210
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
THEMES = {  # GitHub Primer colours, so cards sit naturally on either page background
    'light': dict(bg='#f6f8fa', border='#d0d7de', fg='#1f2328', muted='#59636e', rule='#d8dee4'),
    'dark': dict(bg='#151b23', border='#30363d', fg='#f0f6fc', muted='#9198a1', rule='#262c36'),
}
# name, width, label, accent per theme, (stat, unit), caption, [(title, subtitle)]
# Items stack in one column on the small cards and sit side by side on the wide one.
CARDS = [
    ('about', 936, 'ABOUT', {'light': '#bc4c00', 'dark': '#f0883e'}, ('B.Tech CSE (IT)', ''),
     'MLR Institute of Technology, Hyderabad  ·  Class of 2027',
     [('Full-stack and mobile', 'React, Next.js, React Native, Node.js'),
      ('Mentor', '250+ students at MLRIT CIE'),
      ('Open to work', 'SDE roles from 2027')]),
    ('products', 300, 'PRODUCTS', {'light': '#0969da', 'dark': '#4493f8'}, ('4,000+', 'users'), 'on Edmit, a campus platform',
     [('FiB – Finance Buddy', 'Offline-first finance app, Google Play'),
      ('Edmit', 'Fees and course registration platform')]),
    ('opensource', 300, 'OPEN SOURCE', {'light': '#1a7f37', 'dark': '#3fb950'}, ('20+', 'merged PRs'), 'to freeCodeCamp',
     [('Tests and accessibility', 'Challenge test fixes, aria-expanded'),
      ('Curriculum', 'React, TypeScript and DSA lessons')]),
    ('games', 300, 'GAMES', {'light': '#8250df', 'dark': '#ab7df8'}, ('3', 'games'), 'built in Unity',
     [('Capybara Space Quest', 'Out now on Google Play'),
      ('BeatHop and PenFight', 'In development')]),
]


def card(w, label, accent, stat, caption, items, t):
    big, unit = stat
    unit_svg = f'<tspan dx="6" font-size="15" font-weight="600" fill="{t["muted"]}">{escape(unit)}</tspan>' if unit else ''
    wide = len(items) > 2
    rows = []
    for i, (title, sub) in enumerate(items):
        x, y = (20 + i * (w - 40) / len(items), 148) if wide else (20, 140 + i * 36)
        rows.append(
            f'<circle cx="{x + 6}" cy="{y - 4}" r="3" fill="{accent}"/>'
            f'<text x="{x + 18}" y="{y}" font-size="13" font-weight="600" fill="{t["fg"]}">{escape(title)}</text>'
            f'<text x="{x + 18}" y="{y + 16}" font-size="12" fill="{t["muted"]}">{escape(sub)}</text>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{H}" viewBox="0 0 {w} {H}" font-family="{FONT}" role="img" aria-label="{escape(label)}: {escape(big)} {escape(unit)} {escape(caption)}">
<rect x="0.5" y="0.5" width="{w - 1}" height="{H - 1}" rx="10" fill="{t['bg']}" stroke="{t['border']}"/>
<rect x="20" y="0.5" width="40" height="3" rx="1.5" fill="{accent}"/>
<text x="20" y="32" font-size="11" font-weight="700" letter-spacing="1.4" fill="{accent}">{escape(label)}</text>
<text x="20" y="74" font-size="34" font-weight="700" fill="{t['fg']}">{escape(big)}{unit_svg}</text>
<text x="20" y="96" font-size="13" fill="{t['muted']}">{escape(caption)}</text>
<line x1="20" y1="113" x2="{w - 20}" y2="113" stroke="{t['rule']}"/>
{''.join(rows)}
</svg>
'''


out = Path(__file__).resolve().parent.parent / 'assets'
for name, w, label, accents, stat, caption, items in CARDS:
    for mode, t in THEMES.items():
        (out / f'card-{name}-{mode}.svg').write_text(card(w, label, accents[mode], stat, caption, items, t), encoding='utf-8')
print('wrote', len(CARDS) * len(THEMES), 'cards to', out)
