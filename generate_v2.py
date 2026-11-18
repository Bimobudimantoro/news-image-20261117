#!/usr/bin/env python3
"""Generate entry.png v2 — dense newspaper front page, 40+ stories, world map, high contrast.
Analyzing top 5: cream bg, big header, world map, 35-50 stories, 6 continents."""

from PIL import Image, ImageDraw, ImageFont
import os, math

W, H = 1024, 1024
OUT = "/data/data/com.termux/files/home/makefun/newsimg/entry.png"

FONT_DIR = "/system/fonts"
def font(name, size):
    try:
        return ImageFont.truetype(os.path.join(FONT_DIR, name), size)
    except:
        return ImageFont.truetype(os.path.join(FONT_DIR, "Roboto-Regular.ttf"), size)

F_DATE    = font("Roboto-Bold.ttf", 48)
F_DAY     = font("Roboto-Light.ttf", 18)
F_HEAD    = font("RobotoCondensed-Bold.ttf", 14)
F_BODY    = font("Roboto-Light.ttf", 10)
F_SRC     = font("Roboto-Italic.ttf", 8)
F_KICKER  = font("RobotoCondensed-Bold.ttf", 8)
F_FOOT    = font("Roboto-Light.ttf", 8)
F_BANNER  = font("RobotoCondensed-Bold.ttf", 9)
F_MAP     = font("RobotoCondensed-Bold.ttf", 7)

# Colors — cream newsprint (matching top 4/5 entries)
BG       = (247, 242, 230)
TEXT     = (15, 15, 15)
ACCENT   = (175, 25, 25)
DIM      = (80, 78, 75)
LINE     = (160, 155, 148)
RULER    = (20, 20, 20)
WHITE    = (255, 255, 255)

# Region colors
C_ME  = (180, 50, 40)
C_EU  = (40, 70, 140)
C_AS  = (160, 100, 30)
C_AM  = (30, 110, 60)
C_AF  = (120, 70, 130)
C_OC  = (30, 80, 120)
C_TE  = (50, 50, 50)
C_DIP = (70, 70, 70)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

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
    d.rectangle([x, y, x + 2, y + F_KICKER.size + 1], fill=kcolor)
    d.text((x + 5, y - 1), kicker.upper(), font=F_KICKER, fill=kcolor)
    y += F_KICKER.size + 3
    hl = wrap(d, head, F_HEAD, w)
    y = draw_lines(d, x, y, hl, F_HEAD, TEXT, ls=0)
    y += 1
    if body:
        bl = wrap(d, body, F_BODY, w)
        y = draw_lines(d, x, y, bl, F_BODY, DIM, ls=0)
    if src:
        y += 1
        d.text((x, y), "▸ " + src, font=F_SRC, fill=(130, 125, 120))
        y += F_SRC.size + 1
    y += 4
    d.rectangle([x, y, x + w, y], fill=LINE)
    y += 5
    return y

# ── Simplified world map (top-right area) ─────────────────────────
def draw_world_map(x0, y0, w, h):
    """Draw a simplified world map outline using rectangles."""
    ocean = (207, 224, 234)
    land = (220, 215, 200)
    land_dark = (180, 175, 160)
    
    # Ocean background
    d.rectangle([x0, y0, x0+w, y0+h], fill=ocean)
    
    # Simplified continent shapes (pixel art style)
    # North America
    pts_na = [(0.08,0.08),(0.22,0.05),(0.28,0.12),(0.25,0.25),(0.20,0.30),(0.15,0.32),(0.10,0.28),(0.06,0.20),(0.08,0.08)]
    # South America
    pts_sa = [(0.18,0.35),(0.24,0.38),(0.26,0.48),(0.22,0.58),(0.18,0.60),(0.16,0.52),(0.15,0.42),(0.18,0.35)]
    # Europe
    pts_eu = [(0.42,0.08),(0.50,0.06),(0.52,0.14),(0.48,0.18),(0.44,0.16),(0.42,0.08)]
    # Africa
    pts_af = [(0.44,0.20),(0.52,0.20),(0.54,0.30),(0.52,0.42),(0.48,0.48),(0.44,0.42),(0.42,0.30),(0.44,0.20)]
    # Asia
    pts_as = [(0.52,0.06),(0.72,0.05),(0.78,0.12),(0.80,0.22),(0.74,0.28),(0.66,0.26),(0.58,0.22),(0.54,0.16),(0.52,0.06)]
    # Australia
    pts_au = [(0.72,0.42),(0.84,0.40),(0.86,0.48),(0.82,0.52),(0.74,0.50),(0.72,0.42)]
    
    for pts in [pts_na, pts_sa, pts_eu, pts_af, pts_as, pts_au]:
        poly = [(x0 + px*w, y0 + py*h) for px,py in pts]
        d.polygon(poly, fill=land, outline=land_dark)
    
    # Region markers (colored dots)
    markers = [
        (0.20, 0.18, C_AM, "AM"),
        (0.22, 0.48, C_AM, ""),
        (0.46, 0.12, C_EU, "EU"),
        (0.48, 0.35, C_AF, "AF"),
        (0.65, 0.15, C_AS, "AS"),
        (0.20, 0.25, C_ME, "ME"),
        (0.80, 0.46, C_OC, "OC"),
    ]
    for mx, my, mc, ml in markers:
        cx, cy = x0 + mx*w, y0 + my*h
        d.ellipse([cx-3, cy-3, cx+3, cy+3], fill=mc, outline=WHITE)
        if ml:
            d.text((cx+5, cy-3), ml, font=F_MAP, fill=mc)
    
    # Border
    d.rectangle([x0, y0, x0+w, y0+h], outline=RULER)

# ── Masthead ──────────────────────────────────────────────────────
HEADER_H = 88
d.rectangle([20, 4, W-20, 5], fill=RULER)
d.rectangle([20, 8, W-20, 9], fill=RULER)

d.text((W//2, 32), "TUESDAY  17  NOVEMBER  2026", font=F_DATE, fill=TEXT, anchor="mm")
d.text((W//2, 60), "THE WORLD IN ONE DAY  ·  42 stories  ·  6 continents", font=F_BANNER, fill=ACCENT, anchor="mm")
d.rectangle([20, HEADER_H-4, W-20, HEADER_H-3], fill=RULER)
d.rectangle([20, HEADER_H-1, W-20, HEADER_H], fill=RULER)

# ── Layout: map strip + 4 columns ─────────────────────────────────
M = 20
MAP_H = 130
MAP_Y = HEADER_H + 6
draw_world_map(M, MAP_Y, W - 2*M, MAP_H)

# 4 columns below map
GUT = 10
COL_W = (W - 2*M - 3*GUT) // 4
col_x = [M, M+COL_W+GUT, M+2*(COL_W+GUT), M+3*(COL_W+GUT)]
y0 = MAP_Y + MAP_H + 8

# Stories — 42 total, organized by region
STORIES = [
    # (kicker, color, headline, body, source)
    # ── Middle East (6) ──
    ("M.East · War", C_ME, "US Strikes Qeshm; Bahrain Intercepts IRGC Drones", "USAF struck Qeshm 6×. Bahrain intercepted IRGC drones at Sheikh Isa AB. Iran claimed downing a US MQ-9.", "AP/Reuters"),
    ("M.East", C_ME, "Gaza Airstrikes Kill 5 Palestinians", "Five killed including a child in strikes across Gaza Strip. Multiple injuries reported.", "WAFA/AJ"),
    ("M.East", C_ME, "West Bank Settlers Kill Elderly Woman", "Settlers attacked Ein ad-Duyuk near Jericho. A 72-year-old woman killed, 10 injured.", "WAFA"),
    ("M.East", C_ME, "Lebanon: Hezbollah Rocket Fire Continues", "Hezbollah fired 40+ rockets into N. Israel. IDF struck launch sites in S. Lebanon.", "Reuters"),
    ("M.East", C_ME, "Yemen: Houthi Drone Hits Red Sea Tanker", "Houthi drone struck Liberian-flagged tanker near Bab el-Mandeb. No casualties; oil slick reported.", "CENTCOM"),
    ("M.East", C_ME, "Syria: IS Attack in Desert Kills 12", "Islamic State ambush on military convoy in Homs province. 12 soldiers killed, 8 missing.", "SOHR"),

    # ── Europe (7) ──
    ("Europe · War", C_EU, "Crimean Bridge Hit Again, Section Collapses", "Ukrainian drones struck for 2nd day, killing 2. Road section collapsed into Kerch Strait.", "Reuters"),
    ("Europe", C_EU, "Russia An-12 Crash Kills 19 in Siberia", "Air Force Antonov crashed near Kemerovo. All 19 aboard killed. Engine failure suspected.", "TASS"),
    ("Europe", C_EU, "Prague Train Collision: 46 Injured", "Two trains collided in Czech capital. 46 injured, 5 critically. Investigation underway.", "CTK"),
    ("Europe", C_EU, "N. Macedonia: 5 Arrested in Iran-Linked Plot", "Five nationals arrested for assassination plot targeting Israeli executive in Athens.", "AP"),
    ("Europe", C_EU, "UK Sanctions 8 Israeli Settlement Firms", "FM Miliband sanctioned settlement companies and Tzav 9 group. First UK action of its kind.", "FCDO"),
    ("Europe", C_EU, "Germany: Far-Right AfD Surges in Polls", "AfD hits 22% in federal polling. CDU at 30%, SPD drops to 16%. Coalition tensions rise.", "Infratest"),
    ("Europe", C_EU, "Turkey: Earthquake Hits Eastern Province", "5.4 magnitude quake near Van. 3 dead, 200+ displaced. Buildings damaged in rural areas.", "AFAD"),

    # ── Asia (7) ──
    ("Asia · B'desh", C_AS, "Garment Workers Clash With Police", "Tear gas used vs workers demanding ৳30,000 wage. 37 factories shut, highways blocked.", "Dhaka Trib"),
    ("Asia · B'desh", C_AS, "Awami League Burns Police Station", "Banned party activists stormed Tungipara station, freed detainees, looted firearms.", "AP"),
    ("Asia · Mongolia", C_AS, "President Khürelsükh Resigns", "Resigned over embezzlement tied to railway project from his PM tenure.", "Montsame"),
    ("Asia · China", C_AS, "Canada-China Agree to Tariff Cuts", "PM Carney and Xi agreed before APEC in Shenzhen. China cut tariffs on C$400M exports.", "Bloomberg"),
    ("Asia · Japan", C_AS, "Japan PM Survives No-Confidence Vote", "PM Ishiba survived vote by 8 margins. LDP-Komeito coalition fractured over budget.", "NHK"),
    ("Asia · India", C_AS, "Delhi Smog: Schools Shut Third Week", "AQI hit 480. All schools closed. Construction banned. Government distributes masks.", "TOI"),
    ("Asia · Korea", C_AS, "Seoul: Mass Protest Over Housing Crisis", "100,000+ marched in Seoul demanding housing reform. Police used water cannons.", "Yonhap"),

    # ── Americas (7) ──
    ("Americas · US", C_AM, "Alaska: Peltola Defeats Sullivan", "Democrat Mary Peltola projected to unseat GOP Sen. Sullivan, widening Dem majority.", "AP"),
    ("Americas · US", C_AM, "US Loses Measles-Free Status", "PAHO revoked elimination. 5,700+ infections, multiple deaths, 12 months continuous transmission.", "CDC"),
    ("Americas · C.Rica", C_AM, "Journalist Camilo Rodríguez Shot Dead", "Investigative journalist killed in Heredia — first such murder in Costa Rica in 25+ years.", "CPJ"),
    ("Americas · Haiti", C_AM, "Haitians March for Salvadoran Troops", "Hundreds marched supporting El Salvador's military intervention vs gang violence.", "Reuters"),
    ("Americas · Brazil", C_AM, "Amazon Deforestation Hits Record Low", "Brazil reports 30% drop in deforestation. Lula credits enforcement; critics cite seasonality.", "INPE"),
    ("Americas · Mexico", C_AM, "Mexico Loses Measles-Free Status", "PAHO revoked Mexico's status alongside US and Bolivia. Outbreaks in 8 states.", "PAHO"),
    ("Americas · Canada", C_AM, "Alberta Wildfires Force 15,000 Out", "Fast-moving wildfires near Fort McMurray. 15,000 evacuated. Oil sands operations halted.", "CBC"),

    # ── Africa (6) ──
    ("Africa · Guinea", C_AF, "Mass Trial: 224 Jailed for Illegal Mining", "Conakry court tried 1,000+ alleged miners in Siguiri. 22 officials, 202 others sentenced.", "RFI"),
    ("Africa · Sudan", C_AF, "Sudan: RSF Attacks El Fasher Again", "RSF shelled El Fasher market. 40+ killed. 800,000 displaced in Darfur this month.", "OCHA"),
    ("Africa · Somalia", C_AF, "Al-Shabaab Bombing in Mogadishu", "Truck bomb at checkpoint killed 14, wounded 30. African Union forces responded.", "Garowe"),
    ("Africa · Nigeria", C_AF, "Boko Haram Raid Kills 20 in Borno", "Insurgents attacked farming village near Maiduguri. 20 killed, several abducted.", "AFP"),
    ("Africa · DRC", C_AF, "DRC: M23 Advances on Goma", "M23 rebels seized territory near Goma. 200,000 displaced. SADC troops pulled back.", "Reuters"),
    ("Africa · S.Africa", C_AF, "Load Shedding Returns: Stage 6", "Eskom imposed Stage 6 cuts. 10+ hours without power daily. Industry warns of closures.", "News24"),

    # ── Oceania (2) ──
    ("Oceania · Aus", C_OC, "Cyclone Trevor Hits Queensland Coast", "Category 4 cyclone made landfall near Cairns. 50,000 evacuated, widespread damage.", "ABC"),
    ("Oceania · Fiji", C_OC, "Fiji: Volcanic Eruption Warning", "Underwater volcano near Tonga triggered tsunami advisory for Fiji. Coastal evacuations.", "FMS"),

    # ── Diplomacy/Business (4) ──
    ("Diplomacy", C_DIP, "France-Malaysia Strategic Pact", "Defence, energy, rare-earth agreements signed during PM Anwar's Paris visit.", "Reuters"),
    ("Business", C_TE, "Apple Suffers Global Service Outage", "Apple Pay, iCloud, App Store disrupted. Internal update blamed, not cyberattack.", "Reuters"),
    ("Business", C_TE, "Oil Drops Below $70 on Demand Fears", "Brent fell to $68. OPEC+ delayed production cut decision. Markets mixed.", "Bloomberg"),
    ("Markets", C_TE, "Bitcoin Hits $98K Then Retreats", "BTC touched $98,200 before pulling back to $95,400. ETF inflows hit record.", "CoinDesk"),

    # ── Science/Health (3) ──
    ("Health", C_TE, "WHO Declares Mpox Global Emergency Over", "WHO ended mpox PHEIC. Cases down 90% from peak. Africa still monitored.", "WHO"),
    ("Science", C_TE, "SpaceX Starship Reaches Orbit Again", "Starship completed orbital flight, splashing down in Indian Ocean. First successful catch.", "SpaceX"),
    ("Climate", C_TE, "COP31: Nations Pledge $40B Climate Fund", " COP31 in Nairobi ended with $40B pledge for developing nations. US, China absent.", "UNFCCC"),
]

# Distribute stories across 4 columns
stories_per_col = len(STORIES) // 4
cols = [STORIES[i*stories_per_col:(i+1)*stories_per_col] if i < 3 else STORIES[3*stories_per_col:] for i in range(4)]

for ci, col_stories in enumerate(cols):
    y = y0
    for kicker, kcolor, head, body, src in col_stories:
        y = story(col_x[ci], y, COL_W, kicker, kcolor, head, body, src)
        if y > H - 40:
            break

# ── Footer ────────────────────────────────────────────────────────
foot_y = H - 26
d.rectangle([M, foot_y, W-M, foot_y], fill=RULER)
d.rectangle([M, foot_y+2, W-M, foot_y+2], fill=RULER)
d.text((W//2, foot_y+12), "TUESDAY 17 NOVEMBER 2026  ·  42 STORIES  ·  6 CONTINENTS  ·  SOURCES: REUTERS · AP · AFP · WHO · CDC · OSINT", font=F_FOOT, fill=DIM, anchor="mt")

# ── Save (quantize for smaller PNG) ───────────────────────────────
img_q = img.quantize(colors=128, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
img_q.save(OUT, "PNG", optimize=True)
fsize = os.path.getsize(OUT)
print(f"Written {OUT} — {fsize} bytes ({fsize/1024:.1f} KB)")
