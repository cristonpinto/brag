"""Trace the reference owl (tools/owl-reference.webp) into SVG path data.

Writes src/shapes.generated.js. Run from the owl-mascot folder:
    python3 -I tools/trace.py
Needs: pillow, numpy, opencv-python-headless.
"""
import json, os, sys
import cv2, numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
im = np.array(Image.open(os.path.join(HERE, 'owl-reference.webp')).convert('RGB')).astype(float)
H, W = im.shape[:2]
r, g, b = im[..., 0], im[..., 1], im[..., 2]
lum = 0.3 * r + 0.59 * g + 0.11 * b
navy = (lum < 90).astype('uint8')
cream = ((r > 225) & (b > 150)).astype('uint8')
yellow = ((r > 200) & (b < 110))


def comps(mask, min_area=400):
    n, lab, st, ce = cv2.connectedComponentsWithStats(mask, 8)
    return [(i, st[i], ce[i]) for i in range(1, n) if st[i, 4] > min_area], lab


def path_of(mask, eps=0.7):
    cs, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    c = max(cs, key=cv2.contourArea)
    c = cv2.approxPolyDP(c, eps, True)[:, 0, :]
    pts = ' L'.join(f'{x:.1f} {y:.1f}' for x, y in c)
    return 'M' + pts + 'Z'


def circle_of(mask):
    cs, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    c = max(cs, key=cv2.contourArea)
    (x, y), rad = cv2.minEnclosingCircle(c)
    return [round(x, 1), round(y, 1), round(rad, 1)]


nc, nlab = comps(navy)
big = max(nc, key=lambda c: c[1][4])
body_mask = (nlab == big[0]).astype('uint8')
small = [c for c in nc if c[0] != big[0]]
eyes, beak = [], None
for i, st, ce in small:
    m = (nlab == i).astype('uint8')
    if st[2] > 150 and abs(st[2] - st[3]) < 12:
        eyes.append((ce[0], circle_of(m)))
    else:
        beak = path_of(m, 0.5)
eyes.sort(key=lambda e: e[0])  # left (viewer) first

cc, clab = comps(cream)
cbig = max(cc, key=lambda c: c[1][4])
face_mask = (clab == cbig[0]).astype('uint8')
hl = [(ce[0], circle_of((clab == i).astype('uint8'))) for i, st, ce in cc if i != cbig[0]]
hl.sort(key=lambda e: e[0])

# ---- wing: the lighter oval over the body. Its edge is a soft step in luminance: blur, threshold, then
# keep only the reliable edge (leftmost pixel per row, topmost per column) and fit an ellipse to it.
fc, _ = cv2.findContours(face_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
fc = max(fc, key=cv2.contourArea)[:, 0, :]
bl = cv2.GaussianBlur(lum, (0, 0), 5)
wm0 = ((bl > 38.5) & (bl < 60)).astype('uint8'); wm0[:780] = 0
wm0 = cv2.morphologyEx(wm0, cv2.MORPH_OPEN, np.ones((9, 9), np.uint8))
wm0 = cv2.morphologyEx(wm0, cv2.MORPH_CLOSE, np.ones((25, 25), np.uint8))
n_, lab_, st_, _ = cv2.connectedComponentsWithStats(wm0, 8)
wm0 = (lab_ == 1 + int(np.argmax(st_[1:, 4]))).astype('uint8')
epts = []
for y in range(900, 1150, 4):
    xs_ = np.nonzero(wm0[y])[0]
    if len(xs_): epts.append((xs_.min(), y))
for x in range(720, 1100, 4):
    ys_ = np.nonzero(wm0[:, x])[0]
    if len(ys_): epts.append((x, ys_.min()))
# the wing is egg-shaped rather than elliptical, so keep the measured edge itself
def smooth_line(pts, sigma=9.0):
    """Gaussian smoothing along a polyline (index space), end points kept."""
    pts = np.array(pts, float); n = len(pts); out = np.zeros_like(pts)
    idx = np.arange(n)
    for i in range(n):
        w = np.exp(-0.5 * ((idx - i) / sigma) ** 2); out[i] = (pts * w[:, None]).sum(axis=0) / w.sum()
    out[0], out[-1] = pts[0], pts[-1]
    return out
top_cols = sorted([p for p in epts if p[0] >= 720 and p[1] < 880], key=lambda p: p[0])   # left to right
# where the wing edge IS the cream face's edge, trust the cream contour: it is crisp, the threshold is not
ex = {}
for x_, y_ in fc[(fc[:, 0] >= 735) & (fc[:, 0] <= 914) & (fc[:, 1] >= 798) & (fc[:, 1] <= 935)]:
    ex[int(x_)] = max(ex.get(int(x_), 0), int(y_))
if ex:
    xs_e = sorted(ex); ys_e = [ex[x_] for x_ in xs_e]
    top_cols = [(x_, float(np.interp(x_, xs_e, ys_e)) if 735 <= x_ <= 914 else y_) for x_, y_ in top_cols]
left_rows = sorted([p for p in epts if 880 <= p[1] <= 1180 and p[0] < 760], key=lambda p: p[1])  # top to bottom
chain = [tuple(c) for c in smooth_line([p for p in top_cols if p[0] <= 1000][::-1] + left_rows)]   # from the top, round the left side, down
# the right-hand run-out is read off by eye (the edge is too soft there to threshold); the rest is closed
# far outside the frame so a tilt or squash never shows what is behind
poly = [(1500, 1010), (1254, 886), (1180, 838), (1100, 813)] + chain + [(748, 1254), (760, 1500), (1500, 1500)]
wing = dict(path='M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in poly) + 'Z')
wm = np.zeros((H, W), 'uint8')
cv2.fillPoly(wm, [np.array(poly, np.int32)], 1)

# cream tucks under the wing: grow it into the wing area so a moving wing never shows a gap
grown = cv2.dilate(face_mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (61, 61)))
face_full = ((face_mask > 0) | ((grown > 0) & (wm > 0) & (body_mask > 0))).astype('uint8')

# ---- ear tufts: the part of the body above a cut line, extended inward so it can rotate
def poly_mask(poly):
    m = np.zeros((H, W), 'uint8')
    cv2.fillPoly(m, [np.array(poly, np.int32)], 1)
    return m
left_poly = [(150, 200), (380, 200), (395, 345), (272, 470), (150, 500)]
right_poly = [(780, 60), (1060, 60), (1060, 335), (992, 328), (800, 268)]
tufts = {
    'L': path_of((body_mask & poly_mask(left_poly)).astype('uint8'), 0.5),
    'R': path_of((body_mask & poly_mask(right_poly)).astype('uint8'), 0.5),
}

# ---- colours sampled from the reference
def med(mask, ch=None):
    return [int(np.median(im[..., k][mask > 0])) for k in range(3)]
face_core = (face_mask > 0)
ys, xs = np.nonzero(face_core)
colors = dict(
    yellow=[int(np.median(im[..., k][yellow])) for k in range(3)],
    navy=med((body_mask > 0) & (wm == 0) & (face_full == 0)),
    wing=med((wm > 0) & (body_mask > 0)),
    cream=med(face_core),
)
# gradient end-points: top-left / bottom-right of the face
def patch(x, y, s=30):
    return [int(np.median(im[y - s:y + s, x - s:x + s, k])) for k in range(3)]
colors['creamLight'] = patch(380, 520)
colors['creamDark'] = patch(900, 850)
colors['navyLight'] = patch(380, 1000)
colors['navyDark'] = patch(1150, 700)
colors['yellowCorner'] = [patch(60, 60), patch(1190, 60), patch(60, 1190)]

# the face edge sits on a soft shadow in the reference, so its threshold is noisy: smooth it before tracing
ff = face_full.astype('float32')
sm, sm_heavy = cv2.GaussianBlur(ff, (0, 0), 3.0), cv2.GaussianBlur(ff, (0, 0), 11.0)
yy, xx = np.mgrid[0:H, 0:W]
heavy = (yy > 870) & (xx > 470) & (xx < 1010)      # the soft shadowed stretch next to the wing
face_smooth = (np.where(heavy, sm_heavy, sm) > 0.5).astype('uint8')
out = dict(
    size=[W, H], body=path_of(body_mask, 0.6), face=path_of(face_smooth, 0.8), beak=beak,
    eyes=[e[1] for e in eyes], highlights=[h[1] for h in hl], wing=wing, tufts=tufts, colors=colors,
)
with open(os.path.join(ROOT, 'src', 'shapes.generated.js'), 'w') as f:
    f.write('/* generated by tools/trace.py from tools/owl-reference.webp, do not edit */\n')
    f.write('const SHAPES = ' + json.dumps(out, separators=(',', ':')) + ';\n')
print({k: (v if not isinstance(v, str) else len(v)) for k, v in out.items() if k not in ('colors', 'tufts')})
print(colors)
print({k: len(v) for k, v in tufts.items()})
