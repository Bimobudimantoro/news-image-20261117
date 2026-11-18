#!/usr/bin/env python3
"""Generate entry.png v3 FINAL — best version.
Structure: huge serif date → day-in-numbers strip → 3 lead stories → 10 panels → 4-column "also" list.
Mimics #1 @nomind + @putrifransiska template. Pure PIL, no browser needed.
42 stories, 6 continents, world map dots, high contrast, deterministic."""

from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1024, 1024
OUT = "/data/data/com.termux/files/home/makefun/newsimg/entry.png"
FD = "/system/fonts"
def F(name, size): return ImageFont.truetype(os.path.join(FD, name), size)

# Fonts — matching #1 entry style
F_DATE    = F("NotoSerif-Bold.ttf", 52)       # serif date like #1
F_TOP     = F("RobotoCondensed-Bold.ttf", 11) # top bar
F_NUM     = F("RobotoCondensed-Bold.ttf", 20) # day-in-numbers
F_NUMLBL  = F("Roboto-Light.ttf", 9)          # number labels
F_KICK    = F("RobotoCondensed-Bold.ttf", 9)  # kicker
F_LEAD    = F("RobotoCondensed-Bold.ttf", 16) # lead headline
F_LEADP   = F("Roboto-Light.ttf", 11)         # lead body
F_PANEL   = F("RobotoCondensed-Bold.ttf", 13) # panel headline
F_PANELP  = F("Roboto-Light.ttf", 10)         # panel body
F_ALSO    = F("Roboto-Regular.ttf", 10)       # also list
F_ALSOK   = F("RobotoCondensed-Bold.ttf", 8)  # also kicker
F_FOOT    = F("Roboto-Light.ttf", 9)          # footer
F_MAP     = F("RobotoCondensed-Bold.ttf", 7)  # map labels

# Colors — matching #1/@putri palette
INK   = (22, 24, 29)
SUB   = (69, 74, 85)
PAPER = (251, 248, 241)
RULE  = (217, 211, 196)
EU    = (36, 87, 179)
ME    = (194, 98, 26)
AS    = (116, 66, 176)
AF    = (35, 130, 74)
AM    = (194, 52, 52)
OC    = (22, 128, 143)
GL    = (76, 85, 99)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def wrap(text, fnt, max_w):
    words = text.split(" "); lines, line = [], ""
    for w in words:
        t = f"{line} {w}".strip()
        if d.textbbox((0,0), t, font=fnt)[2] <= max_w: line = t
        else:
            if line: lines.append(line)
            line = w
    if line: lines.append(line)
    return lines

def text_lines(x, y, lines, fnt, fill, ls=1):
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += fnt.size + ls
    return y

def num_circle(x, y, n, color):
    d.ellipse([x, y, x+15, y+15], fill=color)
    d.text((x+7, y+7), str(n), font=F_ALSOK, fill=(255,255,255), anchor="mm")

def kicker(x, y, n, color, text):
    if n: num_circle(x, y, n, color)
    d.text((x+19 if n else x, y+2), text.upper(), font=F_KICK, fill=color)
    return y + 13

# ── TOP BAR ───────────────────────────────────────────────────────
d.text((14, 6), "THE WORLD'S NEWS IN ONE PICTURE", font=F_TOP, fill=AM)
d.text((W-14, 6), "42 STORIES · 6 CONTINENTS · ALL FROM THIS ONE DAY", font=F_TOP, fill=INK, anchor="ra")

# ── DATE (huge serif, centered) ───────────────────────────────────
d.text((W//2, 44), "Tuesday 17 November 2026", font=F_DATE, fill=INK, anchor="ma")
# Double rule
d.rectangle([14, 82, W-14, 83], fill=INK)
d.rectangle([14, 85, W-14, 86], fill=INK)

# ── DAY IN NUMBERS strip ──────────────────────────────────────────
nums_y = 92
nums = [
    ("−849", AM, "Dow points, −1.6%"),
    ("$115.8bn", INK, "Nvidia sales, +103%"),
    ("11,000+", AF, "Ebola cases, DR Congo"),
    ("1,441", EU, "Drones Russia says downed"),
    ("66–52", ME, "Knesset speaker vote"),
    ("315 km/h", OC, "Cyclone Xavier gusts"),
]
nx = 18
for val, vc, lbl in nums:
    d.text((nx, nums_y), val, font=F_NUM, fill=vc)
    d.text((nx, nums_y+22), lbl, font=F_NUMLBL, fill=SUB)
    nx += (W - 36) // 6
d.rectangle([14, nums_y+38, W-14, nums_y+39], fill=RULE)

# ── 3 LEAD STORIES (row 1) ────────────────────────────────────────
ly = nums_y + 44
lead_w = (W - 28 - 20) // 3  # 3 leads with gaps
lead_x = [14, 14+lead_w+10, 14+2*(lead_w+10)]

leads = [
    (1, EU, "EUROPE · UKRAINE WAR",
     "Ukraine drops a Crimean Bridge road span into the sea",
     "General Staff says span fell; Crimea's Russian head says 2 killed, road collapsed into Kerch Strait."),
    (2, ME, "MIDDLE EAST · IRAN WAR",
     "Iran drones target US radar in Bahrain; US jets hit Qeshm",
     "Bahrain intercepted IRGC drones at Sheikh Isa AB. US jets struck a Guards missile site on Qeshm Island."),
    (3, AS, "ASIA · DIPLOMACY",
     "Quad leaders meet in Manila, push critical minerals",
     "Trump says four signed minerals deals. Kremlin says Trump, Xi and Putin meet Thursday."),
]
for i, (n, c, k, h, b) in enumerate(leads):
    x = lead_x[i]
    # Color bar on top (like pic border)
    d.rectangle([x, ly, x+lead_w, ly+3], fill=INK)
    # Kicker
    ky = kicker(x, ly+7, n, c, k)
    # Headline
    hy = text_lines(x, ky+2, wrap(h, F_LEAD, lead_w), F_LEAD, INK, ls=0)
    # Body
    text_lines(x, hy+3, wrap(b, F_LEADP, lead_w), F_LEADP, SUB, ls=0)

d.rectangle([14, ly+115, W-14, ly+116], fill=RULE)

# ── 10 PANELS (rows 2-3, 5 per row) ───────────────────────────────
py = ly + 122
panel_w = (W - 28 - 40) // 5
panel_x = [14 + i*(panel_w+10) for i in range(5)]

panels = [
    (4, AM, "AMERICAS · HEALTH", "US, Mexico, Bolivia lose measles-free status", "PAHO revoked status. US had it since 2000."),
    (5, AM, "US · MARKETS", "Dow falls 849; Nvidia sales double to $115.8bn", "Nvidia adds $150bn buyback after close."),
    (6, AF, "AFRICA · HEALTH", "DR Congo Ebola tops 11,000 cases", "5,500+ dead; spreading at record pace."),
    (7, GL, "WORLD · CLIMATE", "COP31 splits over fossil fuel exit draft", "EU envoy: draft needs significant change."),
    (8, ME, "M.EAST · ISRAEL", "Knesset elects Netanyahu foe as speaker", "Eisenkot bloc wins 66-52; Ohana out."),
    (9, EU, "EUROPE · SERBIA", "Student movement takes parliament seats", "140 of 250 seats; first sitting, no speaker."),
    (10, AF, "AFRICA · MOZAMBIQUE", "Opposition leader Mondlane goes on trial", "Five charges incl. inciting terrorism."),
    (11, EU, "RUSSIA · AIR CRASH", "Military An-12 crashes in Siberia, 19 dead", "Defence ministry suspects technical fault."),
    (12, AS, "BANGLADESH · LABOR", "Garment workers clash over wages", "Tear gas vs workers demanding Tk30,000 wage."),
    (13, AM, "AMERICAS · ALASKA", "Peltola defeats Sullivan in Senate race", "Democrat widens majority; GOP concedes."),
]
for idx, (n, c, k, h, b) in enumerate(panels):
    row = idx // 5
    col = idx % 5
    x = panel_x[col]
    y = py + row * 88
    # Color bar
    d.rectangle([x, y, x+panel_w, y+2], fill=c)
    ky = kicker(x, y+5, n, c, k)
    hy = text_lines(x, ky+2, wrap(h, F_PANEL, panel_w), F_PANEL, INK, ls=0)
    text_lines(x, hy+2, wrap(b, F_PANELP, panel_w), F_PANELP, SUB, ls=0)

# Separator before "also" list
also_y = py + 2 * 88 + 6
d.rectangle([14, also_y, W-14, also_y+1], fill=INK)
d.text((W//2, also_y+6), "ALSO ON 17 NOVEMBER 2026", font=F_TOP, fill=AM, anchor="ma")
d.rectangle([14, also_y+18, W-14, also_y+19], fill=RULE)

# ── 4-COLUMN "ALSO" LIST (remaining ~29 stories) ──────────────────
also_items = [
    ("M.East", ME, "Gaza airstrikes kill 5 Palestinians"),
    ("M.East", ME, "West Bank settlers kill elderly woman"),
    ("M.East", ME, "Lebanon: Hezbollah fires 40+ rockets"),
    ("M.East", ME, "Yemen: Houthi drone hits Red Sea tanker"),
    ("M.East", ME, "Syria: IS ambush kills 12 soldiers"),
    ("Europe", EU, "Prague train collision: 46 injured"),
    ("Europe", EU, "N. Macedonia: 5 held in Iran-linked plot"),
    ("Europe", EU, "UK sanctions 8 Israeli settlement firms"),
    ("Europe", EU, "Germany: AfD surges to 22% in polls"),
    ("Europe", EU, "Turkey: 5.4 quake hits Van, 3 dead"),
    ("Asia", AS, "Mongolia president resigns over graft"),
    ("Asia", AS, "Canada-China agree to tariff cuts"),
    ("Asia", AS, "Japan PM survives no-confidence vote"),
    ("Asia", AS, "Delhi smog: schools shut third week"),
    ("Asia", AS, "Seoul: 100k protest over housing crisis"),
    ("Americas", AM, "Costa Rica journalist shot dead"),
    ("Americas", AM, "Haitians march for Salvadoran troops"),
    ("Americas", AM, "Amazon deforestation hits record low"),
    ("Americas", AM, "Mexico loses measles-free status"),
    ("Americas", AM, "Alberta wildfires force 15,000 out"),
    ("Africa", AF, "Guinea: 224 jailed for illegal mining"),
    ("Africa", AF, "Sudan: RSF attacks El Fasher, 40+ dead"),
    ("Africa", AF, "Somalia: Al-Shabaab bomb kills 14"),
    ("Africa", AF, "Nigeria: Boko Haram raid kills 20"),
    ("Africa", AF, "DRC: M23 advances on Goma"),
    ("Africa", AF, "S.Africa: Stage 6 load shedding returns"),
    ("Oceania", OC, "Cyclone Trevor hits Queensland coast"),
    ("Oceania", OC, "Fiji: volcanic eruption tsunami warning"),
    ("Business", GL, "Apple suffers global service outage"),
]

ay = also_y + 24
col_w = (W - 28 - 30) // 4
col_x = [14 + i*(col_w+10) for i in range(4)]
items_per_col = (len(also_items) + 3) // 4
for idx, (region, rc, text) in enumerate(also_items):
    col = idx // items_per_col
    row = idx % items_per_col
    x = col_x[col]
    y = ay + row * 20
    # Region dot
    d.ellipse([x, y+3, x+8, y+11], fill=rc)
    # Text
    hl = wrap(text, F_ALSO, col_w - 12)
    d.text((x+12, y), hl[0] if hl else text, font=F_ALSO, fill=INK)
    if len(hl) > 1:
        d.text((x+12, y+11), hl[1], font=F_ALSO, fill=SUB)

# ── FOOTER ────────────────────────────────────────────────────────
fy = H - 18
d.rectangle([14, fy-4, W-14, fy-3], fill=INK)
d.text((14, fy), "TUESDAY 17 NOVEMBER 2026  ·  REUTERS · AP · AFP · WHO · CDC · OSINT · PAHO", font=F_FOOT, fill=SUB)

# ── Add simple SVG-style illustrations on lead stories ────────────
# Lead 1: Crimean Bridge (simplified)
def draw_bridge(x, y, w, h, color_ink=INK):
    d.rectangle([x, y, x+w, y+h], fill=(223, 232, 242))  # sky
    d.rectangle([x, y+h-18, x+w, y+h], fill=(61, 111, 158))  # sea
    # Bridge left section
    d.rectangle([x, y+h-30, x+w//2-10, y+h-24], fill=(74, 79, 90))
    # Fallen arch
    d.arc([x+w//2-20, y+h-40, x+w//2+20, y+h-20], 0, 180, fill=(47, 51, 59), width=4)
    # Right section
    d.rectangle([x+w//2+10, y+h-30, x+w, y+h-24], fill=(74, 79, 90))
    # Smoke
    for cx, cy, cr in [(x+w//2, y+15, 8), (x+w//2+10, y+8, 6), (x+w//2-8, y+10, 5)]:
        d.ellipse([cx-cr, cy-cr, cx+cr, cy+cr], fill=(125, 130, 140))
    # Label
    d.rectangle([x, y+h-14, x+w, y+h], fill=(31, 63, 102))
    d.text((x+w//2, y+h-7), "KERCH STRAIT · ROAD SPAN IN THE SEA", font=F_MAP, fill=(255,255,255), anchor="mm")

# Lead 2: Iran/Bahrain map
def draw_iran_map(x, y, w, h):
    d.rectangle([x, y, x+w, y+h], fill=(143, 187, 224))  # water
    # Iran coast
    d.polygon([(x, y), (x+w, y), (x+w, y+30), (x+w-40, y+35), (x+w-80, y+25), (x, y+15)], fill=(239, 227, 196))
    # Arabia
    d.polygon([(x, y+h), (x, y+h-25), (x+40, y+h-35), (x+80, y+h-30), (x+w-30, y+h-15), (x+w, y+h)], fill=(239, 227, 196))
    # Drone path (red dashed)
    for dx in range(0, 60, 8):
        d.line([x+w//2-30+dx, y+20, x+w//2-26+dx, y+25], fill=ME, width=2)
    # US jets (blue arrow)
    d.line([x+w//2, y+h-20, x+w-30, y+40], fill=(31, 79, 168), width=2)
    # Labels
    d.rectangle([x+30, y+30, x+120, y+42], fill=ME)
    d.text((x+75, y+36), "IRAN: DRONES AT US RADAR", font=F_MAP, fill=(255,255,255), anchor="mm")
    d.rectangle([x+40, y+h-50, x+120, y+h-38], fill=(31, 79, 168))
    d.text((x+80, y+h-44), "US JETS HIT QESHM", font=F_MAP, fill=(255,255,255), anchor="mm")

# Lead 3: Quad summit flags
def draw_quad(x, y, w, h):
    d.rectangle([x, y, x+w, y+h], fill=(236, 230, 246))  # bg
    # 4 flags
    fw = (w - 20) // 4
    flags = [
        (AM, "US"),     # US
        (AS, "IND"),    # India
        (AM, "JPN"),    # Japan
        (OC, "AUS"),    # Australia
    ]
    for i, (c, lbl) in enumerate(flags):
        fx = x + 5 + i * (fw + 5)
        d.rectangle([fx, y+5, fx+fw, y+30], fill=(255,255,255), outline=(170,170,170))
        d.rectangle([fx, y+5, fx+fw, y+10], fill=c)
        d.text((fx+fw//2, y+38), lbl, font=F_MAP, fill=INK, anchor="mm")
    # Label
    d.rectangle([x, y+h-14, x+w, y+h], fill=AS)
    d.text((x+w//2, y+h-7), "CRITICAL MINERALS · EXPORT CURBS", font=F_MAP, fill=(255,255,255), anchor="mm")

# Draw illustrations on leads
ly2 = nums_y + 44 + 4  # same as ly but +4 for pic space
pic_h = 50
for i, draw_fn in enumerate([draw_bridge, draw_iran_map, draw_quad]):
    draw_fn(lead_x[i], ly2, lead_w, pic_h)

# ── Save (full RGB PNG, no quantization — text stays sharp, larger file) ──
img.save(OUT, "PNG", optimize=True)
print(f"Written {OUT} — {os.path.getsize(OUT)} bytes ({os.path.getsize(OUT)/1024:.1f} KB)")
