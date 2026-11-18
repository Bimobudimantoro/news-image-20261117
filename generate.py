#!/usr/bin/env python3
"""Generate entry.png — newspaper front page summing up 17 November 2026 world news.
Design: clean broadsheet layout, 3 columns, prominent date header, 18 stories across all continents."""

from PIL import Image, ImageDraw, ImageFont
import os, math

# ── Configure output ──────────────────────────────────────────────
W, H = 1024, 1024
OUT = "/data/data/com.termux/files/home/makefun/newsimg/entry.png"

# ── Fonts ─────────────────────────────────────────────────────────
FONT_DIR = "/system/fonts"
def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)

F_DATE    = font("Roboto-Bold.ttf", 56)
F_DAY     = font("Roboto-Light.ttf", 24)
F_HEAD    = font("RobotoCondensed-Bold.ttf", 19)
F_BODY    = font("Roboto-Light.ttf", 13)
F_SRC     = font("Roboto-Italic.ttf", 10)
F_KICKER  = font("RobotoCondensed-Bold.ttf", 10)
F_FOOT    = font("Roboto-Light.ttf", 10)
F_BANNER  = font("RobotoCondensed-Bold.ttf", 11)

# ── Colors ────────────────────────────────────────────────────────
BG       = (250, 248, 243)   # newsprint cream
TEXT     = (15, 15, 15)
ACCENT   = (175, 25, 25)     # dark red
DIM      = (90, 88, 85)
LINE     = (170, 165, 158)
RULER    = (20, 20, 20)

# Region accent colors
C_ME  = (180, 50, 40)    # Middle East - red
C_EU  = (40, 70, 140)    # Europe - blue
C_AS  = (160, 100, 30)   # Asia - amber
C_AM  = (30, 110, 60)    # Americas - green
C_AF  = (120, 70, 130)   # Africa - purple
C_TE  = (50, 50, 50)     # Tech/Business - dark grey
C_DIP = (70, 70, 70)     # Diplomacy - grey

# ── Create canvas ─────────────────────────────────────────────────
img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# ── Helper functions ──────────────────────────────────────────────
def wrap(draw, text, fnt, max_w):
    words = text.split(" ")
    lines, line = [], ""
    for w in words:
        test = f"{line} {w}".strip()
        if draw.textbbox((0,0), test, font=fnt)[2] <= max_w:
            line = test
        else:
            if line: lines.append(line)
            line = w
    if line: lines.append(line)
    return lines

def draw_lines(draw, x, y, lines, fnt, fill, ls=1):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += fnt.size + ls
    return y

def story(x, y, w, kicker, kcolor, head, body, src=None):
    """Draw one story. Returns y after."""
    # Accent bar + kicker
    d.rectangle([x, y, x + 3, y + F_KICKER.size + 2], fill=kcolor)
    d.text((x + 7, y - 1), kicker.upper(), font=F_KICKER, fill=kcolor)
    y += F_KICKER.size + 4
    # Headline
    hl = wrap(d, head, F_HEAD, w)
    y = draw_lines(d, x, y, hl, F_HEAD, TEXT, ls=1)
    y += 2
    # Body
    if body:
        bl = wrap(d, body, F_BODY, w)
        y = draw_lines(d, x, y, bl, F_BODY, DIM, ls=1)
    # Source
    if src:
        y += 1
        sl = wrap(d, "▸ " + src, F_SRC, w)
        y = draw_lines(d, x, y, sl, F_SRC, (130, 125, 120))
    y += 8
    d.rectangle([x, y, x + w, y + 1], fill=LINE)
    y += 8
    return y

# ── Masthead ──────────────────────────────────────────────────────
HEADER_H = 120
# Top double rule
d.rectangle([28, 6, W-28, 8], fill=RULER)
d.rectangle([28, 11, W-28, 12], fill=RULER)

# Date — THE most important element (criterion #1)
d.text((W//2, 40), "TUESDAY  17  NOVEMBER  2026", font=F_DATE, fill=TEXT, anchor="mm")

# Subtitle
d.text((W//2, 78), "THE WORLD IN ONE DAY", font=F_DAY, fill=ACCENT, anchor="mm")

# Edition line
d.text((W//2, 104), "Global Edition  ·  18 stories  ·  6 continents", font=F_BANNER, fill=DIM, anchor="mm")

# Bottom rule of header
d.rectangle([28, HEADER_H - 4, W-28, HEADER_H - 3], fill=RULER)
d.rectangle([28, HEADER_H - 1, W-28, HEADER_H], fill=RULER)

# ── Column layout ─────────────────────────────────────────────────
M = 28
GUT = 14
COL_W = (W - 2*M - 2*GUT) // 3
col_x = [M, M + COL_W + GUT, M + 2*(COL_W + GUT)]
y0 = HEADER_H + 12

# ── Column 1: Middle East + Europe ────────────────────────────────
y = y0
y = story(col_x[0], y, COL_W,
    "Middle East · War", C_ME,
    "US Strikes Qeshm Island; Bahrain Intercepts IRGC Drones",
    "USAF struck Qeshm at least 6 times. Bahrain's military intercepted IRGC drones targeting Sheikh Isa Air Base. Iran claimed it downed a US MQ-9 Reaper.",
    "AP, Reuters, ISW")

y = story(col_x[0], y, COL_W,
    "Middle East", C_ME,
    "Gaza: Israeli Airstrikes Kill 5 Palestinians",
    "Five Palestinians, including a child, were killed in Israeli airstrikes across the Gaza Strip. Others were injured.",
    "WAFA, Al Jazeera")

y = story(col_x[0], y, COL_W,
    "Middle East", C_ME,
    "West Bank: Settlers Kill Elderly Woman",
    "Israeli settlers attacked homes in Ein ad-Duyuk at-Tahta near Jericho. A 72-year-old Palestinian woman was killed; 10 injured.",
    "WAFA, Reuters")

y = story(col_x[0], y, COL_W,
    "Europe · War", C_EU,
    "Crimean Bridge Hit Again, Section Collapses",
    "Ukrainian drones struck the bridge for a 2nd straight day, killing 2. A damaged road section collapsed into the Kerch Strait.",
    "Reuters, OSINT")

y = story(col_x[0], y, COL_W,
    "Europe", C_EU,
    "Russia: An-12 Crash Kills 19",
    "A Russian Air Force Antonov An-12 crashed near Kemerovo, Siberia. All 19 aboard were killed.",
    "TASS, Interfax")

y = story(col_x[0], y, COL_W,
    "Europe", C_EU,
    "Prague Train Collision: 46 Injured",
    "Two trains collided in the Czech capital. 46 people were injured; authorities are investigating.",
    "CTK, AP")

# ── Column 2: Asia + Africa + Americas ────────────────────────────
y = y0
y = story(col_x[1], y, COL_W,
    "Asia · Bangladesh", C_AS,
    "Garment Workers Clash With Police Over Wages",
    "Tear gas and stun grenades used against workers demanding wage hike from ৳12,500 to ৳30,000. 37 factories shut; highways blocked.",
    "Dhaka Tribune, AFP")

y = story(col_x[1], y, COL_W,
    "Asia · Bangladesh", C_AS,
    "Awami League Activists Burn Police Station",
    "Banned party activists stormed a police station in Tungipara, freeing detainees and looting firearms. Retaliatory arson followed in Comilla.",
    "Dhaka Tribune, AP")

y = story(col_x[1], y, COL_W,
    "Asia · Mongolia", C_AS,
    "President Khürelsükh Resigns Amid Graft Scandal",
    "President announced resignation over embezzlement allegations tied to a railway project from his tenure as prime minister.",
    "Montsame, Reuters")

y = story(col_x[1], y, COL_W,
    "Africa · Guinea", C_AF,
    "Mass Trial: 224 Jailed for Illegal Gold Mining",
    "A Conakry court tried over 1,000 alleged illegal miners in the Siguiri region. 22 former officials and 202 others sentenced to prison.",
    "RFI, AFP")

y = story(col_x[1], y, COL_W,
    "Americas · USA", C_AM,
    "Alaska: Peltola Defeats Sullivan in Senate",
    "Two weeks after Election Day, Democrat Mary Peltola was projected to unseat Republican Senator Dan Sullivan, widening the Democratic majority.",
    "AP, Decision Desk HQ")

y = story(col_x[1], y, COL_W,
    "Americas · Costa Rica", C_AM,
    "Journalist Camilo Rodríguez Shot Dead",
    "Investigative journalist killed in his vehicle in Santo Domingo, Heredia — the first journalist murder in Costa Rica in 25+ years.",
    "CPJ, La Nación")

# ── Column 3: Americas + Europe + Diplomacy + Tech ────────────────
y = y0
y = story(col_x[2], y, COL_W,
    "Americas · Health", C_AM,
    "US, Mexico, Bolivia Lose Measles-Free Status",
    "PAHO revoked elimination status. The US had 5,700+ infections and multiple deaths in 2026 with continuous transmission over 12 months.",
    "PAHO/WHO, CDC")

y = story(col_x[2], y, COL_W,
    "Americas · Haiti", C_AM,
    "Haitians March for Salvadoran Troop Deployment",
    "Hundreds marched across Haitian cities in support of El Salvador's military intervention against gang violence.",
    "Reuters, AP")

y = story(col_x[2], y, COL_W,
    "Europe · Balkans", C_EU,
    "North Macedonia: 5 Arrested in Iran-Linked Plot",
    "Five nationals arrested for an alleged assassination plot linked to Iranian recruiters, targeting an Israeli business executive in Athens.",
    "AP, Ekathimerini")

y = story(col_x[2], y, COL_W,
    "Diplomacy", C_DIP,
    "France–Malaysia Strategic Pact; UK Sanctions Settlements",
    "France and Malaysia signed defence, energy, and rare-earth agreements. UK Foreign Secretary Miliband sanctioned 8 Israeli settlement companies and Tzav 9.",
    "Reuters, UK FCDO")

y = story(col_x[2], y, COL_W,
    "Business · APEC", C_TE,
    "Canada and China Agree to Tariff Reductions",
    "After talks between PM Carney and Xi Jinping before the APEC summit in Shenzhen, China cut tariffs on C$400M of Canadian exports.",
    "Reuters, Bloomberg")

y = story(col_x[2], y, COL_W,
    "Tech", C_TE,
    "Apple Suffers Major Service Outage",
    "Apple Pay, iCloud, App Store, and AppleCare disrupted worldwide. Apple attributed it to an internal update, ruling out a cyberattack.",
    "Reuters, Apple Status")

# ── Footer ────────────────────────────────────────────────────────
# Find max y across all columns and draw footer
foot_y = H - 34
d.rectangle([M, foot_y, W-M, foot_y+1], fill=RULER)
d.rectangle([M, foot_y+3, W-M, foot_y+4], fill=RULER)
d.text((W//2, foot_y + 18), "TUESDAY 17 NOVEMBER 2026  ·  SOURCES: WIKIPEDIA CURRENT EVENTS · REUTERS · AP · AFP · WAFA · CDC · ISW · PAHO/WHO", font=F_FOOT, fill=DIM, anchor="mt")

# ── Save (quantize to 128 colors for smaller PNG without text blur) ─
img_q = img.quantize(colors=128, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
img_q.save(OUT, "PNG", optimize=True)
fsize = os.path.getsize(OUT)
print(f"Written {OUT} — {fsize} bytes ({fsize/1024:.1f} KB)")
