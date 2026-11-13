# Usage: python3 gen-svg.py <frames.json> <font.woff2> <out.svg>
import json, base64, sys
FRAMES, FONT, OUT = sys.argv[1:4]
d = json.load(open(FRAMES))
N, fps = d['frames'], d['fps']
L = N / fps                      # loop seconds
slot = 100 / N                   # percent of the loop one frame owns
font = base64.b64encode(open(FONT, 'rb').read()).decode()
roles = ['software engineer · full-stack', 'react · typescript · node.js', 'ai engineer', 'system architect', 'tech lead']
R = 5.0                          # seconds per role, as on the site
RT = R * len(roles)
pc = lambda s: f'{100 * s / RT:.3f}%'
EASE = 'cubic-bezier(.22,1,.36,1)'
css = f'''
@font-face{{font-family:PJS;src:url(data:font/woff2;base64,{font}) format('woff2');font-weight:200 800}}
text{{font-family:PJS,system-ui,sans-serif;fill:#F5F2EC}}
.f{{opacity:0;animation:f {L}s linear infinite}}
.f0{{opacity:1;animation:f0 {L}s linear infinite}}
.fc{{opacity:0;animation:fc {L}s linear infinite}}
@keyframes f{{0%{{opacity:0}}{slot:.4f}%{{opacity:1}}{2*slot:.4f}%{{opacity:1}}{2*slot+.001:.4f}%,100%{{opacity:0}}}}
@keyframes f0{{0%,{2*slot:.4f}%{{opacity:1}}{2*slot+.001:.4f}%,100%{{opacity:0}}}}
@keyframes fc{{0%{{opacity:0}}{slot:.4f}%{{opacity:1}}{slot+.001:.4f}%,100%{{opacity:0}}}}
.rise{{animation:rise .9s {EASE} both}}
@keyframes rise{{from{{transform:translateY(var(--d))}}to{{transform:translateY(0)}}}}
.role{{opacity:0;animation:role {RT}s infinite}}
@keyframes role{{0%{{opacity:0;transform:translateY(12px);animation-timing-function:{EASE}}}{pc(.45)}{{opacity:1;transform:translateY(0)}}{pc(R-.3)}{{opacity:1;transform:translateY(0);animation-timing-function:{EASE}}}{pc(R)},100%{{opacity:0;transform:translateY(-12px)}}}}
@media (prefers-reduced-motion:reduce){{.f,.fc,.role,.rise{{animation:none}}.f0{{animation:none;opacity:1}}.role:first-of-type{{opacity:1}}}}
'''
o = [f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 1280 440" width="1280" height="440" role="img" aria-labelledby="t">',
     '<title id="t">kevin shibuya. software engineer, full-stack.</title>', f'<style>{css}</style>',
     '<defs><clipPath id="m0"><rect x="0" y="93" width="1280" height="35"/></clipPath><clipPath id="m1"><rect x="0" y="141.1" width="1280" height="121.5"/></clipPath><clipPath id="m2"><rect x="0" y="262.6" width="1280" height="145.4"/></clipPath></defs>',
     '<rect width="1280" height="440" fill="#E6996A"/>']
for i, j in enumerate(d['jpegs']):
    cls = 'f0' if i == 0 else 'f'
    delay = '' if i == 0 else f' style="animation-delay:{i / fps:.4f}s"'
    o.append(f'<image id="p{i}" class="{cls}"{delay} width="1280" height="440" preserveAspectRatio="none" href="{j}"/>')
o.append('<use class="fc" href="#p0" xlink:href="#p0"/>')   # wraps the last frame back into the first
o.append('<g clip-path="url(#m0)"><g class="rise" style="--d:38px;animation-delay:.35s" font-size="24" font-weight="500" letter-spacing="-0.24">')
for i, r in enumerate(roles):
    o.append(f'<text class="role" style="animation-delay:{i * R}s" x="70" y="118.1">{r}</text>')
o.append('</g></g>')
o.append('<g font-size="132" font-weight="700" letter-spacing="-3.96">'
         '<g clip-path="url(#m1)"><text class="rise" style="--d:152px;animation-delay:.43s" x="70" y="255.1">kevin</text></g>'
         '<g clip-path="url(#m2)"><text class="rise" style="--d:152px;animation-delay:.51s" x="70" y="376.6">shibuya.</text></g></g>')
o.append('</svg>')
open(OUT, 'w').write('\n'.join(o))
print(len('\n'.join(o)))
