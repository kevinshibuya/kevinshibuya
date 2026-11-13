"""Build the heading and row images for the profile README.

Usage, from the repo root:  python3 tools/rows.py

Each image is a small SVG with the typeface embedded, in a dark and a light
variant. The row anatomy comes from the portfolio's WorkRow: a faded index, a
large title, an arrow when the row links somewhere, and a hairline.
"""
import base64
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'assets' / 'readme'
FONT = base64.b64encode((ROOT / 'assets/fonts/PlusJakartaSans-subset.woff2').read_bytes()).decode()

THEMES = {
    'dark': {'text': '#F5F2EC', 'faded': '#A8A49C', 'hair': 'rgba(245,242,236,.13)'},
    'light': {'text': '#0B0E14', 'faded': 'rgba(11,14,20,.62)', 'hair': 'rgba(11,14,20,.12)'},
}
EASE = 'cubic-bezier(.22,1,.36,1)'

# (slug, title, has a link)
ROWS = {
    'building': [
        ('promptfall', 'promptfall', True),
        ('forge', 'forge', True),
        ('barber-app', 'barber-app', True),
        ('arena-ranking', 'arena-ranking', True),
        ('job-form-filler', 'job-form-filler', True),
        ('crypto-token-analysis', 'crypto-token-analysis', True),
    ],
    'shipped': [
        ('painel', 'painel da reconstrução', True),
        ('enquetes', 'enquetes gzh', False),
        ('chat-da-hora', 'chat da hora', False),
        ('politica-essencial', 'política essencial', False),
    ],
}
HEADINGS = [
    ('now-building', 'now building', 44),
    ('shipped', 'shipped', 44),
    ('contact', "got a project or rough idea? let's talk.", 38),
]


def style(extra=''):
    return (f"<style>@font-face{{font-family:PJS;src:url(data:font/woff2;base64,{FONT}) format('woff2');"
            f"font-weight:200 800}}text{{font-family:PJS,system-ui,sans-serif}}"
            f".rise{{animation:rise .6s {EASE} both}}"
            f"@keyframes rise{{from{{transform:translateY(var(--d))}}to{{transform:translateY(0)}}}}"
            f"@media (prefers-reduced-motion:reduce){{.rise{{animation:none}}}}{extra}</style>")


def row(index, title, linked, c):
    delay = 0.06 * index
    arrow = (f'<text x="878" y="42" text-anchor="end" font-size="22" fill="{c["faded"]}">↗</text>' if linked else '')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 64" width="880" height="64" role="img" '
            f'aria-label="{index + 1:02d} {title}">{style()}'
            f'<defs><clipPath id="m"><rect x="0" y="8" width="880" height="50"/></clipPath></defs>'
            f'<rect width="880" height="1" fill="{c["hair"]}"/>'
            f'<g clip-path="url(#m)"><text class="rise" style="--d:52px;animation-delay:{delay:.2f}s" y="44">'
            f'<tspan x="0" font-size="13" letter-spacing=".5" fill="{c["faded"]}">{index + 1:02d}</tspan>'
            f'<tspan dx="18" font-size="34" font-weight="550" letter-spacing="-.68" fill="{c["text"]}">{title}</tspan>'
            f'</text></g>{arrow}</svg>')


def heading(text, size, c):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 76" width="880" height="76" role="img" '
            f'aria-label="{text}">{style()}'
            f'<defs><clipPath id="m"><rect x="0" y="6" width="880" height="64"/></clipPath></defs>'
            f'<g clip-path="url(#m)"><text class="rise" style="--d:66px" x="0" y="54" font-size="{size}" '
            f'font-weight="700" letter-spacing="{-0.03 * size:.2f}" fill="{c["text"]}">{text}</text></g></svg>')


OUT.mkdir(parents=True, exist_ok=True)
n = 0
for theme, c in THEMES.items():
    for slug, text, size in HEADINGS:
        (OUT / f'heading-{slug}-{theme}.svg').write_text(heading(text, size, c)); n += 1
    for group in ROWS.values():
        for i, (slug, title, linked) in enumerate(group):
            (OUT / f'row-{slug}-{theme}.svg').write_text(row(i, title, linked, c)); n += 1
print(n, 'files')
