#!/usr/bin/env python3
"""THE MONDAY EDITION - one image summing up the world news of Monday 23 November 2026.
Drawn entirely in code (PIL). Every story happened or was first reported on Mon 23 Nov 2026;
the research log lives in ../stories.md. No photographs."""
from PIL import Image, ImageDraw, ImageFont
import os

FD = "/usr/share/fonts/truetype/dejavu"
def F(name, size):
    return ImageFont.truetype(os.path.join(FD, name), size)
SERIF_B = "DejaVuSerif-Bold.ttf"
SERIF = "DejaVuSerif.ttf"
SANS_B = "DejaVuSans-Bold.ttf"
SANS = "DejaVuSans.ttf"

PAPER = (246, 239, 221)
PANEL_BG = (251, 247, 236)
INK = (28, 30, 38)
MUTED = (96, 90, 78)
RED = (168, 44, 34)
NAVY = (30, 58, 92)
GOLD = (178, 138, 44)
BORDER = (203, 190, 158)
WHITE = (252, 250, 244)

W, H = 1024, 1024
img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def tw(text, font):
    return d.textlength(text, font=font)

def wrap(text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if tw(t, font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines

def spaced(text, font, tracking):
    """draw letter-spaced text centered at cx; returns total width"""
    widths = [tw(c, font) for c in text]
    total = sum(widths) + tracking * (len(text) - 1)
    return total

def draw_spaced(cx, y, text, font, fill, tracking=3):
    total = spaced(text, font, tracking)
    x = cx - total / 2
    for c in text:
        d.text((x, y), c, font=font, fill=fill)
        x += tw(c, font) + tracking

# ---------------------------------------------------------------- vignettes
def vig_base(box, sky):
    x, y, w, h = box
    d.rectangle([x, y, x + w, y + h], fill=sky)
    return x, y, w, h

def v_capitol(box):
    x, y, w, h = vig_base(box, (198, 216, 232))
    gy = y + h - 5
    d.rectangle([x, gy, x + w, y + h], fill=(112, 128, 96))          # lawn
    cx = x + w // 2
    bw = min(w - 40, 300)
    d.rectangle([cx - bw // 2, gy - 18, cx + bw // 2, gy], fill=(238, 236, 228))  # main block
    for i in range(9):                                                # columns
        px = cx - bw // 2 + 12 + i * (bw - 24) // 8
        d.line([px, gy - 16, px, gy - 3], fill=(178, 176, 168), width=2)
    d.polygon([(cx - 34, gy - 18), (cx + 34, gy - 18), (cx, gy - 30)], fill=(238, 236, 228))
    d.rectangle([cx - 14, gy - 40, cx + 14, gy - 30], fill=(226, 224, 216))
    d.ellipse([cx - 16, gy - 54, cx + 16, gy - 38], fill=(70, 96, 128))          # dome
    d.rectangle([cx - 2, gy - 59, cx + 2, gy - 54], fill=(70, 96, 128))
    for i in range(11):                                               # crowd
        px = x + 14 + i * (w - 28) // 10
        d.ellipse([px - 2, gy + 1, px + 2, gy + 4], fill=(60, 60, 70))
    d.rectangle([x + 8, gy - 10, x + 24, gy - 2], fill=(168, 44, 34)) # ballot box
    d.rectangle([x + 11, gy - 8, x + 21, gy - 6], fill=WHITE)
    for cxx, cyy in [(x + 60, y + 8), (x + w - 120, y + 5)]:          # clouds
        d.ellipse([cxx, cyy, cxx + 34, cyy + 9], fill=(240, 246, 250))
        d.ellipse([cxx + 10, cyy - 4, cxx + 28, cyy + 5], fill=(240, 246, 250))
    fx = x + w - 34                                                   # flag
    d.line([fx, gy, fx, y + 10], fill=(90, 80, 70), width=2)
    d.rectangle([fx, y + 10, fx + 24, y + 24], fill=(178, 44, 34))
    for s in range(3):
        d.rectangle([fx, y + 14 + s * 4, fx + 24, y + 16 + s * 4], fill=(246, 244, 238))
    d.rectangle([fx, y + 10, fx + 10, y + 17], fill=(70, 96, 128))

def v_markets(box):
    x, y, w, h = vig_base(box, (24, 32, 48))
    # faint grid over the whole board
    for gx in range(x + 14, x + w - 4, 26):
        d.line([gx, y + 3, gx, y + h - 9], fill=(38, 50, 70), width=1)
    for gy in range(y + 6, y + h - 8, 9):
        d.line([x + 4, gy, x + w - 4, gy], fill=(38, 50, 70), width=1)
    # candlesticks marching along the lower half
    import random
    rnd = random.Random(23)
    cw = (w - 16) // 14
    base = y + h - 12
    for i in range(14):
        cx = x + 8 + i * cw + cw // 2
        o = base - 6 - rnd.randint(0, 9)
        c = o + rnd.randint(-6, 7)
        hi = min(o, c) - rnd.randint(1, 4)
        lo = max(o, c) + rnd.randint(1, 4)
        col = (84, 200, 120) if c <= o else (224, 84, 60)
        d.line([cx, hi, cx, lo], fill=col, width=1)
        d.rectangle([cx - 2, min(o, c), cx + 2, max(o, c) + 1], fill=col)
    # the day's line: red plunge, then a bright green clawback to a new high
    pts = [(x + 6, y + 5), (x + w * 0.2, y + 9), (x + w * 0.36, y + h * 0.34),
           (x + w * 0.5, y + h - 13), (x + w * 0.63, y + h - 19),
           (x + w * 0.8, y + 9), (x + w - 10, y + 4)]
    d.line(pts[:4], fill=(224, 84, 60), width=3)
    d.line(pts[3:], fill=(84, 200, 120), width=3)
    d.polygon([(x + w - 10, y + 4), (x + w - 21, y + 3), (x + w - 13, y - 3)], fill=(84, 200, 120))
    d.ellipse([x + w * 0.5 - 3, y + h - 16, x + w * 0.5 + 3, y + h - 10], fill=(246, 244, 238))
    # ticker blocks along the top edge, exchange-board style
    for i, col in enumerate([(224, 84, 60), (84, 200, 120), (240, 190, 90), (84, 200, 120),
                             (224, 84, 60), (120, 170, 220), (84, 200, 120), (224, 84, 60)]):
        bx = x + 6 + i * (w - 12) // 8
        d.rectangle([bx, y + 2, bx + (w - 12) // 8 - 5, y + 5], fill=col)
    # skyline silhouette along the bottom
    for i, bh in enumerate([0.3, 0.5, 0.36, 0.62, 0.44, 0.7, 0.4, 0.55, 0.34, 0.48, 0.6, 0.38]):
        bx = x + 4 + i * (w - 8) // 12
        top = y + h - int(bh * 10) - 1
        d.rectangle([bx, top, bx + (w - 8) // 12 - 2, y + h], fill=(16, 24, 38))
        d.rectangle([bx + 2, top + 2, bx + 4, top + 4], fill=(240, 200, 90))

def v_strike(box):
    x, y, w, h = vig_base(box, (206, 216, 224))
    gy = y + h - 10
    d.rectangle([x, gy, x + w, y + h], fill=(150, 150, 146))
    d.rectangle([x + w - 62, y + 8, x + w - 44, gy], fill=(120, 130, 142))        # tower
    d.rectangle([x + w - 68, y + 8, x + w - 38, y + 16], fill=(90, 100, 114))
    px, py = x + 26, gy - 16                                                      # grounded plane
    d.ellipse([px, py, px + 62, py + 13], fill=(232, 232, 230))
    d.polygon([(px + 50, py + 1), (px + 66, py - 10), (px + 70, py + 2)], fill=(190, 60, 48))
    d.polygon([(px + 8, py + 2), (px - 4, py - 8), (px + 10, py + 4)], fill=(190, 60, 48))
    for i in range(5):
        d.ellipse([px + 8 + i * 11, py + 4, px + 12 + i * 11, py + 8], fill=(70, 96, 128))
    d.line([px + 4, py - 6, px + 62, py + 16], fill=RED, width=3)                 # grounded X
    d.line([px + 62, py - 6, px + 4, py + 16], fill=RED, width=3)
    for i in range(3):                                                            # pickets
        sx = x + w - 108 + i * 16
        d.line([sx, gy, sx, gy - 14], fill=(90, 70, 50), width=2)
        d.rectangle([sx - 6, gy - 24, sx + 7, gy - 14], fill=WHITE, outline=RED)

def v_gaza(box):
    x, y, w, h = vig_base(box, (216, 205, 182))
    gy = y + h - 8
    d.rectangle([x, gy, x + w, y + h], fill=(148, 132, 108))
    for i, (bw, bh) in enumerate([(26, 28), (20, 18), (30, 32), (18, 14), (24, 24), (20, 20)]):
        bx = x + 10 + i * (w - 20) // 6
        d.rectangle([bx, gy - bh, bx + bw, gy], fill=(146, 132, 110))
        d.line([bx + 3, gy - bh + 4, bx + bw - 4, gy - 6], fill=(104, 92, 74), width=2)
    d.ellipse([x + w * 0.3, gy - 4, x + w * 0.52, gy + 3], fill=(96, 128, 74))     # toxic pool
    d.ellipse([x + w * 0.62, gy - 3, x + w * 0.78, gy + 3], fill=(96, 128, 74))
    d.rectangle([x + w - 34, gy - 18, x + w - 22, gy - 4], fill=(196, 164, 60))    # barrel
    d.line([x + w - 34, gy - 12, x + w - 22, gy - 12], fill=(120, 96, 30), width=2)

def v_graves(box):
    x, y, w, h = vig_base(box, (188, 204, 178))
    gy = y + h - 6
    d.rectangle([x, gy - 8, x + w, y + h], fill=(128, 142, 104))
    for r in range(2):
        for i in range(7):
            gx = x + 14 + i * (w - 28) // 6 + (r * 9)
            gy2 = gy - 4 - r * 14
            d.line([gx, gy2 - 9, gx, gy2], fill=(240, 238, 230), width=3)
            d.line([gx - 3, gy2 - 6, gx + 3, gy2 - 6], fill=(240, 238, 230), width=3)
    d.polygon([(x + w - 46, gy - 8), (x + w - 30, gy - 26), (x + w - 14, gy - 8)], fill=(226, 224, 218))
    d.rectangle([x + w - 34, gy - 18, x + w - 26, gy - 8], fill=RED)
    d.rectangle([x + w - 38, gy - 15, x + w - 22, gy - 12], fill=WHITE)

def v_nhs(box):
    x, y, w, h = vig_base(box, (214, 226, 238))
    mx = x + w // 2
    d.rectangle([mx - 52, y + 5, mx + 52, y + h - 6], fill=(240, 244, 248), outline=(120, 140, 160))
    d.ellipse([mx - 42, y + 9, mx - 8, y + h - 10], fill=(238, 196, 204))         # scan image
    d.ellipse([mx - 29, y + 15, mx - 19, y + 25], fill=(214, 130, 150))
    for cx_, cy_, s in [(mx - 48, y + 7, 6), (mx - 2, y + 7, 6), (mx - 48, y + h - 14, 6), (mx - 2, y + h - 14, 6)]:
        d.line([cx_, cy_, cx_ + s, cy_], fill=(30, 120, 90), width=2)
        d.line([cx_, cy_, cx_, cy_ + s], fill=(30, 120, 90), width=2)
    d.rectangle([mx + 6, y + 10, mx + 36, y + 15], fill=(30, 120, 90))
    d.rectangle([mx + 6, y + 19, mx + 30, y + 22], fill=(150, 170, 190))
    d.rectangle([mx + 6, y + 26, mx + 33, y + 29], fill=(150, 170, 190))

def v_factory(box):
    x, y, w, h = vig_base(box, (84, 74, 78))
    gy = y + h - 8
    d.rectangle([x, gy, x + w, y + h], fill=(52, 48, 52))
    d.rectangle([x + 16, gy - 30, x + 96, gy], fill=(104, 96, 100))
    d.rectangle([x + 104, gy - 40, x + 116, gy], fill=(88, 82, 86))
    for i in range(4):
        d.rectangle([x + 24 + i * 18, gy - 24, x + 34 + i * 18, gy - 14], fill=(240, 190, 90))
    for fx, fs in [(30, 16), (52, 22), (76, 14), (108, 18)]:
        d.polygon([(x + fx, gy - 28), (x + fx + fs // 2, gy - 28 - fs), (x + fx + fs, gy - 28)], fill=(232, 116, 40))
        d.polygon([(x + fx + 3, gy - 28), (x + fx + fs // 2, gy - 28 - fs + 6), (x + fx + fs - 3, gy - 28)], fill=(246, 190, 70))
    for i in range(3):
        sx = x + 34 + i * 26
        d.ellipse([sx, y + 4, sx + 16, y + 16], fill=(140, 136, 140))
    for i in range(3):                                                            # rescuers
        rx = x + w - 52 + i * 16
        d.ellipse([rx, gy - 14, rx + 5, gy - 9], fill=(246, 190, 70))
        d.line([rx + 2, gy - 9, rx + 2, gy], fill=(230, 120, 40), width=3)

def v_sub(box):
    x, y, w, h = vig_base(box, (16, 44, 74))
    for i in range(4):
        d.ellipse([x + 12 + i * 30, y + h - 12, x + 34 + i * 30, y + h - 4], fill=(30, 66, 100))
    sx, sy = x + w * 0.3, y + h * 0.38
    d.ellipse([sx, sy, sx + 74, sy + 20], fill=(238, 168, 60))                   # ROV body
    d.rectangle([sx + 26, sy - 8, sx + 48, sy + 2], fill=(220, 148, 48))
    d.ellipse([sx + 58, sy + 6, sx + 68, sy + 16], fill=(180, 220, 240))
    d.polygon([(sx + 74, sy + 4), (x + w - 6, sy - 4), (x + w - 6, sy + 22)], fill=(250, 240, 190, ))  # light cone base
    d.line([sx + 70, sy + 10, sx + 84, sy + 24], fill=(200, 130, 40), width=3)   # arm
    for i in range(5):                                                            # pyroclastic rocks
        rx = x + w - 58 + (i % 3) * 16
        ry = y + h - 16 + (i // 3) * 7
        d.polygon([(rx, ry), (rx + 7, ry - 6), (rx + 13, ry)], fill=(96, 110, 128))
    for i in range(6):
        d.ellipse([x + 8 + i * 16, y + 6 + (i % 2) * 5, x + 10 + i * 16, y + 8 + (i % 2) * 5], fill=(150, 190, 220))

def v_flags(box):
    x, y, w, h = vig_base(box, (206, 220, 234))
    gy = y + h - 8
    d.rectangle([x, gy, x + w, y + h], fill=(150, 138, 110))
    p1, p2 = x + w * 0.3, x + w * 0.62
    for px in (p1, p2):
        d.line([px, gy, px, y + 8], fill=(90, 80, 70), width=3)
    fw, fh = 44, 26                                                              # India
    d.rectangle([p1, y + 8, p1 + fw, y + 8 + fh // 3], fill=(240, 140, 50))
    d.rectangle([p1, y + 8 + fh // 3, p1 + fw, y + 8 + 2 * fh // 3], fill=(246, 244, 238))
    d.rectangle([p1, y + 8 + 2 * fh // 3, p1 + fw, y + 8 + fh], fill=(60, 140, 70))
    d.ellipse([p1 + fw // 2 - 3, y + 8 + fh // 2 - 3, p1 + fw // 2 + 3, y + 8 + fh // 2 + 3], outline=(40, 60, 150), width=1)
    d.polygon([(p2, y + 8), (p2 + fw, y + 8 + fh // 2), (p2, y + 8 + fh)], fill=(190, 40, 60))   # Nepal pennant
    d.polygon([(p2, y + 12), (p2 + 26, y + 8 + fh // 2), (p2, y + 8 + fh - 4)], fill=(250, 248, 244))
    for i in range(4):                                                            # crowd
        cx_ = x + 16 + i * (w - 32) // 3
        d.ellipse([cx_ - 3, gy - 8, cx_ + 3, gy - 2], fill=(70, 64, 60))

def v_castle(box):
    x, y, w, h = vig_base(box, (190, 216, 232))
    gy = y + h - 5
    d.rectangle([x, gy, x + w, y + h], fill=(140, 150, 120))
    d.rectangle([x, gy - 3, x + w, gy], fill=(196, 192, 184))                     # stone wall
    cx = x + w // 2
    d.rectangle([cx - 48, gy - 15, cx + 48, gy - 3], fill=(250, 248, 242))        # white base
    d.rectangle([cx - 40, gy - 24, cx + 40, gy - 15], fill=(178, 44, 34))         # red hall
    for i in range(5):
        d.rectangle([cx - 32 + i * 15, gy - 22, cx - 25 + i * 15, gy - 17], fill=(250, 230, 170))
    d.polygon([(cx - 50, gy - 24), (cx + 50, gy - 24), (cx + 34, gy - 31), (cx - 34, gy - 31)], fill=(150, 36, 28))
    d.polygon([(cx - 34, gy - 31), (cx + 34, gy - 31), (cx, gy - 36)], fill=(168, 44, 34))
    d.polygon([(cx - 4, gy - 36), (cx, gy - 39), (cx + 4, gy - 36)], fill=(178, 138, 44))

def v_quake(box):
    x, y, w, h = vig_base(box, (170, 206, 224))
    d.rectangle([x, y + h * 0.55, x + w, y + h], fill=(70, 130, 170))             # sea
    ix, iy = x + w * 0.42, y + h * 0.5
    d.polygon([(ix, iy), (ix + 52, iy), (ix + 40, iy + 12), (ix + 10, iy + 12)], fill=(96, 150, 92))  # island
    d.line([ix + 24, iy, ix + 24, iy - 14], fill=(90, 70, 50), width=3)           # palm
    d.arc([ix + 12, iy - 22, ix + 38, iy - 6], 200, 330, fill=(60, 130, 70), width=3)
    d.arc([ix + 16, iy - 20, ix + 34, iy - 8], 200, 330, fill=(60, 130, 70), width=3)
    for r in (10, 18, 26):                                                        # seismic rings
        d.ellipse([ix - r + 26, iy + 8 - r // 2, ix + r + 26, iy + 8 + r // 2], outline=(240, 244, 248), width=2)
    d.polygon([(x + 10, y + h - 8), (x + 22, y + h - 22), (x + 34, y + h - 8)], fill=(240, 244, 248))

def v_stadium(box):
    x, y, w, h = vig_base(box, (178, 208, 190))
    gy = y + h - 6
    d.ellipse([x + 14, y + 8, x + w - 14, gy], fill=(240, 238, 230))              # bowl
    d.ellipse([x + 26, y + 16, x + w - 26, gy - 6], fill=(96, 160, 92))           # pitch
    d.ellipse([x + w // 2 - 12, y + h // 2 - 10, x + w // 2 + 12, y + h // 2 + 14], fill=(250, 250, 248), outline=(60, 60, 60))
    for px, py in [(x + w // 2 - 6, y + h // 2 - 4), (x + w // 2 + 3, y + h // 2 + 3), (x + w // 2 - 1, y + h // 2 + 8)]:
        d.polygon([(px, py), (px + 5, py + 2), (px + 2, py + 6), (px - 2, py + 3)], fill=(30, 30, 34))
    for i in range(6):                                                            # floodlights
        fx = x + 18 + i * (w - 36) // 5
        d.line([fx, y + 12, fx, y + 4], fill=(90, 90, 90), width=2)
        d.ellipse([fx - 2, y + 1, fx + 2, y + 5], fill=(250, 240, 170))
    tx = x + w - 34                                                                       # trophy
    d.polygon([(tx, y + 10), (tx + 16, y + 10), (tx + 13, y + 22), (tx + 3, y + 22)], fill=GOLD)
    d.rectangle([tx + 6, y + 22, tx + 10, y + 27], fill=GOLD)
    d.rectangle([tx + 3, y + 27, tx + 13, y + 30], fill=GOLD)

def v_talks(box):
    x, y, w, h = vig_base(box, (208, 210, 216))
    gy = y + h - 8
    d.rectangle([x, gy, x + w, y + h], fill=(120, 118, 124))
    for px, col in [(x + w * 0.26, NAVY), (x + w * 0.62, (90, 90, 96))]:
        d.rectangle([px - 16, gy - 22, px + 16, gy], fill=(238, 236, 230))        # podium
        d.ellipse([px - 4, gy - 32, px + 4, gy - 24], fill=(216, 180, 150))       # head
        d.rectangle([px - 6, gy - 24, px + 6, gy - 14], fill=col)
    fx = x + w * 0.44                                                             # flag between
    d.line([fx, gy, fx, y + 6], fill=(90, 80, 70), width=2)
    d.rectangle([fx, y + 6, fx + 26, y + 20], fill=(246, 246, 244))
    d.rectangle([fx, y + 6, fx + 26, y + 9], fill=(60, 90, 170))
    d.rectangle([fx, y + 17, fx + 26, y + 20], fill=(60, 90, 170))
    cx, cy = fx + 13, y + 13
    for a in range(6):
        import math
        dx, dy = math.cos(a * 3.14159 / 3) * 3.4, math.sin(a * 3.14159 / 3) * 3.4
        d.line([cx - dx, cy - dy, cx + dx, cy + dy], fill=(60, 90, 170), width=1)
    d.line([x + w * 0.4, gy - 30, x + w * 0.56, gy - 38], fill=RED, width=3)       # broken bridge line
    d.line([x + w * 0.56, gy - 38, x + w * 0.72, gy - 30], fill=(150, 148, 152), width=3)

def v_school(box):
    x, y, w, h = vig_base(box, (204, 216, 226))
    gy = y + h - 7
    d.rectangle([x, gy, x + w, y + h], fill=(128, 126, 118))
    sx = x + 16                                                                     # schoolhouse
    d.rectangle([sx, gy - 24, sx + 52, gy], fill=(238, 232, 220))
    d.polygon([(sx - 4, gy - 24), (sx + 56, gy - 24), (sx + 26, gy - 35)], fill=(150, 62, 48))
    d.rectangle([sx + 21, gy - 13, sx + 31, gy], fill=(90, 70, 55))
    for wx in (sx + 6, sx + 38):
        d.rectangle([wx, gy - 20, wx + 8, gy - 13], fill=(170, 200, 220))
    fx = sx + 66                                                                    # flag pole
    d.line([fx, gy, fx, y + 3], fill=(90, 80, 70), width=2)
    d.rectangle([fx, y + 3, fx + 20, y + 8], fill=(30, 30, 30))
    d.rectangle([fx, y + 8, fx + 20, y + 13], fill=(200, 40, 45))
    d.rectangle([fx, y + 13, fx + 20, y + 18], fill=GOLD)
    for i, col in enumerate([(70, 110, 180), (190, 80, 70), (80, 150, 90)]):        # children filing out
        cx = x + w * 0.52 + i * 17
        d.ellipse([cx - 3, gy - 17, cx + 3, gy - 11], fill=(216, 180, 150))
        d.rectangle([cx - 3, gy - 11, cx + 3, gy - 2], fill=col)
        d.rectangle([cx + 3, gy - 10, cx + 7, gy - 4], fill=(90, 70, 50))
    px = x + w - 52                                                                 # police car
    d.rectangle([px, gy - 11, px + 40, gy - 3], fill=(240, 240, 242))
    d.rectangle([px + 8, gy - 17, px + 28, gy - 11], fill=(240, 240, 242))
    d.rectangle([px + 11, gy - 16, px + 17, gy - 12], fill=(170, 200, 220))
    d.rectangle([px + 19, gy - 16, px + 25, gy - 12], fill=(170, 200, 220))
    d.rectangle([px, gy - 8, px + 40, gy - 6], fill=NAVY)
    d.rectangle([px + 15, gy - 19, px + 20, gy - 17], fill=RED)
    d.rectangle([px + 20, gy - 19, px + 25, gy - 17], fill=(60, 90, 200))
    for wx in (px + 8, px + 32):
        d.ellipse([wx - 4, gy - 5, wx + 4, gy + 1], fill=(35, 35, 35))
    ex, ey = x + w - 30, y + 3                                                      # the emailed threat
    d.rectangle([ex, ey, ex + 18, ey + 11], fill=(250, 250, 248), outline=(90, 90, 90))
    d.line([ex, ey, ex + 9, ey + 6], fill=(90, 90, 90), width=1)
    d.line([ex + 18, ey, ex + 9, ey + 6], fill=(90, 90, 90), width=1)

def v_army(box):
    x, y, w, h = vig_base(box, (198, 200, 188))
    gy = y + h - 8
    d.rectangle([x, gy, x + w, y + h], fill=(130, 126, 112))
    d.rectangle([x + 12, gy - 20, x + 62, gy - 6], fill=(96, 104, 74))            # truck
    d.rectangle([x + 62, gy - 16, x + 76, gy - 6], fill=(84, 92, 64))
    d.rectangle([x + 66, gy - 15, x + 74, gy - 10], fill=(170, 200, 220))
    for wx in (24, 58):
        d.ellipse([x + wx - 6, gy - 8, x + wx + 6, gy + 2], fill=(40, 40, 40))
    for i in range(3):                                                            # crates
        cx_ = x + w - 58 + (i % 2) * 20
        cy_ = gy - 14 - (i // 2) * 14
        d.rectangle([cx_, cy_, cx_ + 16, cy_ + 12], fill=(150, 124, 84), outline=(110, 90, 58))
    sx, sy = x + w - 30, y + 12                                                   # blast star
    import math
    pts = []
    for a in range(12):
        r = 11 if a % 2 == 0 else 5
        pts.append((sx + r * math.cos(a * math.pi / 6), sy + r * math.sin(a * math.pi / 6)))
    d.polygon(pts, fill=(240, 170, 60))
    for i in range(4):                                                            # barrier tape
        bx = x + 90 + i * 22
        d.line([bx, gy - 16, bx, gy], fill=(90, 80, 70), width=2)
        d.polygon([(bx, gy - 16), (bx + 20, gy - 16), (bx + 20, gy - 11), (bx, gy - 11)], fill=(240, 200, 60))

# ---------------------------------------------------------------- world map
def lonlat(lon, lat, box):
    x, y, w, h = box
    return (x + (lon + 170) / 360.0 * w, y + (75 - lat) / 135.0 * h)

def draw_map(box):
    x, y, w, h = box
    d.rectangle([x, y, x + w, y + h], fill=(196, 214, 226))
    land = (168, 178, 148)
    polys = [
        [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 70), (-80, 73), (-76, 68), (-65, 62), (-55, 52), (-65, 45), (-70, 42), (-75, 38), (-80, 32), (-80, 26), (-84, 30), (-90, 29), (-97, 26), (-97, 22), (-94, 17), (-87, 13), (-83, 9), (-86, 13), (-97, 16), (-105, 20), (-110, 23), (-114, 29), (-120, 34), (-125, 40), (-125, 49), (-132, 56), (-152, 60), (-165, 60)],
        [(-79, 9), (-75, 11), (-64, 10), (-55, 6), (-50, 0), (-44, -3), (-35, -8), (-39, -13), (-40, -20), (-48, -26), (-52, -33), (-58, -39), (-65, -45), (-69, -54), (-73, -46), (-73, -37), (-71, -30), (-70, -20), (-75, -15), (-79, -8), (-80, -4), (-77, 4)],
        [(-10, 36), (-9, 43), (-2, 44), (0, 46), (-4, 48), (0, 50), (5, 53), (8, 57), (12, 56), (18, 56), (21, 55), (24, 59), (28, 60), (30, 64), (40, 66), (55, 68), (68, 70), (60, 64), (48, 60), (42, 54), (38, 47), (30, 46), (26, 40), (20, 40), (15, 38), (10, 37), (12, 42), (7, 44), (3, 42), (0, 39)],
        [(-6, 35), (0, 36), (10, 37), (20, 32), (30, 31), (35, 28), (38, 22), (40, 15), (43, 12), (51, 12), (48, 5), (42, -2), (40, -10), (40, -18), (37, -22), (33, -26), (28, -30), (20, -35), (17, -32), (15, -27), (12, -18), (13, -12), (9, -5), (9, 0), (4, 6), (-3, 5), (-8, 5), (-13, 8), (-17, 12), (-17, 16), (-16, 21), (-13, 27), (-10, 31)],
        [(44, -16), (47, -15), (50, -18), (48, -22), (45, -25), (44, -20)],
        [(28, 41), (33, 46), (38, 47), (42, 54), (48, 60), (60, 64), (70, 66), (75, 72), (85, 73), (95, 76), (105, 77), (115, 73), (125, 72), (135, 71), (145, 72), (155, 70), (165, 66), (178, 65), (178, 62), (162, 60), (156, 52), (148, 50), (141, 50), (140, 44), (135, 40), (130, 38), (126, 40), (122, 38), (120, 32), (115, 23), (110, 20), (108, 13), (105, 8), (103, 5), (100, 8), (98, 14), (95, 16), (92, 17), (89, 22), (86, 20), (80, 15), (77, 8), (74, 13), (72, 20), (66, 25), (61, 25), (57, 26), (51, 28), (48, 30), (43, 29), (39, 31), (36, 36), (30, 36)],
        [(95, 5), (102, -3), (110, -7), (118, -8), (125, -8), (132, -6), (139, -7), (146, -8), (150, -10), (143, -9), (135, -8), (126, -9), (117, -10), (108, -9), (100, -5), (96, 1)],
        [(109, 1), (113, 4), (117, 6), (119, 1), (116, -3), (111, -2)],
        [(130, 31), (133, 34), (137, 35), (140, 37), (141, 41), (142, 44), (140, 42), (137, 38), (134, 34), (131, 32)],
        [(-5, 50), (-3, 53), (-5, 56), (-2, 57), (0, 53), (1, 51)],
        [(113, -22), (114, -29), (116, -34), (119, -35), (126, -32), (132, -32), (136, -35), (139, -37), (145, -38), (148, -38), (150, -37), (153, -30), (153, -25), (150, -23), (146, -19), (142, -14), (141, -12), (137, -12), (136, -15), (134, -12), (130, -12), (126, -14), (122, -17), (117, -20)],
        [(167, -45), (171, -42), (174, -39), (176, -37), (173, -40), (171, -43), (168, -47)],
    ]
    for poly in polys:
        d.polygon([lonlat(lon, lat, box) for lon, lat in poly], fill=land)
    pins = {1: (-77, 39), 2: (121, 25), 3: (4.5, 50.8), 4: (34.3, 31.4), 5: (30.3, 1.6),
            6: (-0.1, 51.5), 7: (106.2, -6.3), 8: (142, 11.3), 9: (77.2, 28.6), 10: (127.7, 26.2),
            11: (169, -15), 12: (-3.5, 53.5), 13: (13.4, 52.5), 14: (-93.5, 42)}
    offsets = {3: (8, 6), 10: (9, -7), 12: (11, -9), 13: (14, -4)}  # keep clustered pins apart
    for n, (lon, lat) in pins.items():
        px, py = lonlat(lon, lat, box)
        if n in offsets:
            px += offsets[n][0]
            py += offsets[n][1]
        d.ellipse([px - 6, py - 6, px + 6, py + 6], fill=RED, outline=WHITE, width=1)
        t = str(n)
        fnt = F(SANS_B, 8 if n < 10 else 7)
        d.text((px - tw(t, fnt) / 2, py - 4), t, font=fnt, fill=WHITE)

# ---------------------------------------------------------------- panels
def render_vig(fn, x, y, w, h):
    """Draw a vignette on its own layer so nothing can escape its box."""
    global d
    tmp = Image.new("RGB", (w, h), PANEL_BG)
    old = d
    d = ImageDraw.Draw(tmp)
    fn((0, 0, w, h))
    d = old
    img.paste(tmp, (x, y))

def panel(x, y, w, h, num, tag, status, head, sub, vig, head_size=13, sub_size=9,
          vig_h=46, head_lines=2, sub_lines=2):
    d.rectangle([x, y, x + w, y + h], fill=PANEL_BG, outline=BORDER, width=1)
    render_vig(vig, x + 5, y + 5, w - 10, vig_h)
    hy = y + 5 + vig_h + 4
    d.ellipse([x + 6, hy, x + 20, hy + 14], fill=RED)
    t = str(num)
    fnt = F(SANS_B, 9 if num < 10 else 8)
    d.text((x + 13 - tw(t, fnt) / 2, hy + 2), t, font=fnt, fill=WHITE)
    d.text((x + 24, hy + 2), tag, font=F(SANS_B, 7.5), fill=NAVY)
    stf = F(SANS_B, 7)
    d.text((x + w - 6 - tw(status, stf), hy + 3), status, font=stf, fill=RED)
    yy = hy + 17
    hf = F(SERIF_B, head_size)
    for ln in wrap(head, hf, w - 14)[:head_lines]:
        d.text((x + 7, yy), ln, font=hf, fill=INK)
        yy += head_size + 4
    sf = F(SANS, sub_size)
    for ln in wrap(sub, sf, w - 14)[:sub_lines]:
        d.text((x + 7, yy), ln, font=sf, fill=(52, 52, 58))
        yy += sub_size + 2.5

PANELS = [
    (2, "ASIA · MARKETS", "REPORTED · REUTERS",
     "AI sell-off, week two: Asia slides, then claws back",
     "Taipei swings 1,578 points, then recovers; Korea's exports top $1tn; Tokyo shut.",
     v_markets),
    (3, "EUROPE · STRIKE", "CONFIRMED · AP",
     "Belgium's airports shut for a day of strikes",
     "All 429 Brussels flights cancelled - 59,500 passengers - as unions fight austerity.",
     v_strike),
    (4, "GAZA · ENVIRONMENT", "REPORTED · GUARDIAN",
     "Report: 99% of Gaza shows contamination",
     "Oxfam finds toxic risk across the Strip: 61m tonnes of debris, sewage in the sea.",
     v_gaza),
    (5, "AFRICA · HEALTH", "REPORTED · REUTERS",
     "Counting Congo's graves: Ebola toll is far higher",
     "Bunia's graves imply 1,000+ excess deaths; the official Ebola tally is 707.",
     v_graves),
    (6, "EUROPE · HEALTH", "CONFIRMED · BBC",
     "NHS opens world's largest AI cancer-screening trial",
     "The NHS begins the world's largest trial of AI to spot breast cancer earlier.",
     v_nhs),
    (7, "ASIA · DISASTER", "CONFIRMED · REUTERS",
     "Indonesia confirms 24 dead in candy-factory fire",
     "Saturday's blaze at Cikande; ~30 workers missing as 500 rescuers search.",
     v_factory),
    (8, "OCEAN · SCIENCE", "REPORTED · SCIENCE NEWS",
     "Robot sub finds deepest explosive eruptions",
     "Pyroclastic deposits 6,148m down by Challenger Deep, where eruptions 'can't' happen.",
     v_sub),
    (9, "ASIA · DIPLOMACY", "CONFIRMED · INSHORTS",
     "Nepal's PM Balen Shah welcomed in Delhi",
     "Ceremonial welcome in Delhi; energy and connectivity top his first bilateral trip.",
     v_flags),
    (10, "ASIA · CULTURE", "CONFIRMED · SHURIJO PARK",
     "Shuri Castle's red hall opens again",
     "Seven years after fire gutted it, Okinawa's Seiden reopens at noon today.",
     v_castle),
    (11, "OCEANIA · QUAKE", "CONFIRMED · USGS",
     "M6.5 quake deep under the Pacific",
     "02:40 UTC, 598km down southeast of Vanuatu; too deep to do damage. PAGER: green.",
     v_quake),
    (12, "EUROPE · FOOTBALL", "REPORTED · BBC",
     "FIFA votes today on UK as 2035 Women's Cup host",
     "The four home nations are the sole bidders; a first UK World Cup since 1966.",
     v_stadium),
    (13, "EUROPE · SECURITY", "REPORTED · REUTERS",
     "Bomb threats emailed to 450 schools across Germany",
     "'Death awaits you' emails spark evacuations; Denmark hit too, no concrete danger.",
     v_school),
    (14, "AMERICAS · SOCIETY", "REPORTED · REUTERS",
     "Army to detonate unstable explosives in Iowa",
     "68 barrels of unstable lead azide; the Army now says Wednesday, despite a court's pause.",
     v_army),
]

ALSO = [
    "Canberra: Albanese defends Bowen after COP31",
    "Canberra: jobless will pass 5%, treasurer warns",
    "Seoul: police quiz exam cheat Han a 4th time",
    "Taipei: short sales curbed from today",
    "Taiwan: export orders rise a 21st month",
    "Mumbai: Tata Steel's $1.67bn pipe-maker deal",
    "Mumbai: IndusInd sacks ex-CEO, seeks clawback",
    "Delhi: India-China hold 10 days of border talks",
    "Sydney: India stays Asia's No. 3 power - Lowy",
    "Washington: MSCI sounded out Prabowo, Dalio",
    "Houston: US energy exports hit records",
    "Hormuz: hunt on for sailor missing off tanker",
    "Tehran: dual missile launcher shown off",
    "Paris: frontrunners question Ukraine aid",
    "London: Burnham's EU-deal pitch to MPs",
    "Jerusalem: Eisenkot condemns settler arson",
    "Bogota: state asks X to suspend Petro account",
    "Kathmandu: first UN Loss & Damage payout",
    "Abuja: move to end jail for suicide attempts",
    "Kuala Lumpur: otters back in city river",
    "Tokyo: Milky Way simulation sets record",
    "St Helena: DNA of a 194-year-old tortoise",
    "Nairobi: Zipline hires Uber exec for Africa",
    "Hormuz: Iran claims US MQ-9 drone downed",
    "Rome: jeweller Paolo Bulgari dies at 89",
    "Gaza: only 19% of sewage pumps still work",
    "Brasilia: Bolsonaro still in intensive care",
    "Indonesia: navy seizes 405t chemical ship",
    "Oil: Brent holds near $90 on reopening",
    "Gold: up 2.7% in the flight to safety",
    "Congo: fighting hampers Ebola response",
    "Legazpi: Mayon stays at alert level 3",
    "Seoul: Ateez take 4th Billboard 200 No. 1",
    "Jakarta: factory CEO to be summoned",
    "Brussels: trains run as airports shut",
    "Paris: students plan nationwide protests",
]

DATECHECK = ("COP31's gavel fell Sunday - Dymer's strike was Sunday - the Shenzhen summit was Thursday - "
             "Hormuz's tankers and Bahrain were Saturday - the Baltic freighter burned Saturday - Khartoum's drones came Sunday - "
             "the Riemann 'proof' was claimed Friday - Alcaraz and Marquez won their titles on Sunday.")

# ---------------------------------------------------------------- assembly
MX = 26
CW = W - 2 * MX

# top strip
d.line([MX, 12, W - MX, 12], fill=INK, width=1)
d.text((MX, 17), "THE WORLD · IN ONE PAGE", font=F(SANS_B, 10), fill=INK)
r = "ONE DAY · ONE PAGE · NO PHOTOGRAPHS"
d.text((W - MX - tw(r, F(SANS_B, 10)), 17), r, font=F(SANS_B, 10), fill=INK)
d.line([MX, 34, W - MX, 34], fill=RED, width=3)
d.line([MX, 39, W - MX, 39], fill=INK, width=1)

# masthead
draw_spaced(W // 2, 48, "THE MONDAY EDITION", F(SANS_B, 19), INK, tracking=6)
df = F(SERIF_B, 50)
dt = "Monday 23 November 2026"
d.text(((W - tw(dt, df)) / 2, 72), dt, font=df, fill=INK)
d.rectangle([MX, 128, W - MX, 152], fill=NAVY)
bt = "50 STORIES · 8 REGIONS · EVERY ONE FROM MONDAY 23 NOVEMBER 2026"
bf = F(SANS_B, 13.5)
d.text(((W - tw(bt, bf)) / 2, 134), bt, font=bf, fill=WHITE)

# timeline strip: the day unfolding in UTC
TY = 158
d.rectangle([MX, TY, W - MX, TY + 32], fill=(243, 234, 214), outline=BORDER)
d.rectangle([MX, TY, MX + 96, TY + 32], fill=RED)
d.text((MX + 10, TY + 5), "THE DAY", font=F(SANS_B, 9.5), fill=WHITE)
d.text((MX + 10, TY + 17), "IN UTC", font=F(SANS_B, 9.5), fill=WHITE)
tl = [("00:49", "NHS opens giant AI cancer-screening trial"),
      ("02:40", "M6.5 quake strikes deep off Vanuatu"),
      ("03:00", "Shuri Castle's red hall reopens in Naha"),
      ("06:00", "Belgium's strike shuts its airspace")]
tlf, ttf = F(SANS_B, 9), F(SANS, 9)
for i, (tm, tx) in enumerate(tl):
    tx0 = MX + 108 + i * 218
    d.text((tx0, TY + 5), tm, font=tlf, fill=RED)
    lines = wrap(tx, ttf, 208 - tw(tm, tlf) - 6)
    d.text((tx0 + tw(tm, tlf) + 5, TY + 5), lines[0], font=ttf, fill=INK)
    if len(lines) > 1:
        d.text((tx0, TY + 16), lines[1], font=ttf, fill=INK)

# lead row: panel 1 (custom, large) + panel 2
LY, LH = 196, 144
panel(MX, LY, 576, LH, 1, "AMERICAS · POLITICS", "CONFIRMED · BBC",
      "Democrats clinch largest House majority since 1992",
      "258 seats after a North Carolina recount flips the last race; the Senate is theirs too, 56 seats.",
      v_capitol, head_size=19, sub_size=11, vig_h=54, head_lines=1, sub_lines=2)
panel(610, LY, 388, LH, *PANELS[0], head_size=14, sub_size=9.5, vig_h=46)

# small panels: rows of 4
COLX = [26, 271, 516, 761]
COLW = 237
ROWY = [348, 476, 604]
ROWH = 120
rest = PANELS[1:]
for i, p in enumerate(rest):
    cx = COLX[i % 4]
    cy = ROWY[i // 4]
    panel(cx, cy, COLW, ROWH, *p, head_size=13, sub_size=8.5, vig_h=40)

# bottom: map (left) + ALSO (right)
BY = 732
d.text((MX, BY), "WHERE IT HAPPENED", font=F(SANS_B, 11), fill=RED)
d.line([MX, BY + 16, MX + 216, BY + 16], fill=INK, width=1)
draw_map((MX, BY + 22, 216, 132))
d.text((MX, BY + 160), "Pins: the 14 numbered stories", font=F(SANS, 8), fill=MUTED)

AX = 258
d.text((AX, BY), "ALSO ON MONDAY 23 NOVEMBER", font=F(SANS_B, 12), fill=INK)
d.line([AX, BY + 17, W - MX, BY + 17], fill=INK, width=1)
also_items = [(15 + i, t) for i, t in enumerate(ALSO)]
cols = [also_items[0:12], also_items[12:24], also_items[24:36]]
colw = (W - MX - AX - 2 * 14) // 3
nf, tf = F(SANS_B, 9), F(SANS, 9)
for ci, col in enumerate(cols):
    cx = AX + ci * (colw + 14)
    yy = BY + 24
    for n, t in col:
        d.text((cx, yy), str(n), font=nf, fill=RED)
        lines = wrap(t, tf, colw - 17)
        for ln in lines:
            d.text((cx + 17, yy), ln, font=tf, fill=(52, 52, 58))
            yy += 10.5
        yy += 2

# date check band
DY = 946
d.rectangle([MX, DY, W - MX, DY + 34], fill=(243, 234, 214), outline=BORDER)
d.rectangle([MX, DY, MX + 118, DY + 34], fill=RED)
d.text((MX + 8, DY + 4), "DATE CHECK", font=F(SANS_B, 10.5), fill=WHITE)
d.text((MX + 8, DY + 18), "NOT THIS DAY", font=F(SANS_B, 8), fill=WHITE)
dcf = F(SANS, 9.5)
dc = ("COP31's gavel fell Sunday - Dymer's strike was Sunday - the Shenzhen summit was Thursday - Hormuz's tankers "
      "were Saturday - Khartoum's drones came Sunday - the Riemann 'proof' was claimed Friday - Alcaraz & Marquez won Sunday.")
yy = DY + 3
for ln in wrap(dc, dcf, 836)[:3]:
    d.text((MX + 128, yy), ln, font=dcf, fill=(52, 52, 58))
    yy += 11.5

# footer
foot = ("Every story above happened or was first reported on Monday 23 November 2026. CONFIRMED = verified against the named outlet; "
        "REPORTED = as reported by it. Sources: BBC, Reuters, AP, AFP, The Guardian, USGS, Yonhap, The Hindu, Science News. Original drawings.")
ff = F(SANS, 8)
yy = 986
for ln in wrap(foot, ff, CW)[:2]:
    d.text(((W - tw(ln, ff)) / 2, yy), ln, font=ff, fill=MUTED)
    yy += 10.5

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
img.save(out, optimize=True)
print("wrote", out, os.path.getsize(out), "bytes")
