#!/usr/bin/env python3
"""Compose the entry image for make.fun news-image-20261120:
"The World in One Day" for Friday 20 November 2026, holding
37 verified stories.

The page mirrors the structure of this series' winning pages,
as the reader directed: navy masthead with date badge,
rainbow region band, a UTC timeline, three lead cards with
art on top, two rows of four cards, a dot-matrix world map
and a numbered briefs block. Nothing here is copied from
another entry - the stories are the 37 verified for this
page (SOURCES.md), the illustrations are drawn for our
editions and re-cropped to the card shapes on per-picture
focal windows, and the words are set here in PIL.

Page plan, on a 1024x1024 sheet, top to bottom:
  masthead   a navy band: a date badge at the left (NOV / 20 /
             FRI - 2026), the paper's name in small caps, the
             date itself in huge white serif, an italic
             standfirst, and the page's counts
             (37 STORIES - 7 REGIONS - 11 DRAWN - ONE PAGE)
  rainbow    one band of seven coloured segments, one per
             region, each carrying its story count
  timeline   THE DAY IN UTC: a label box and five moment
             boxes with the day's grounded times
  lead row   three cards with their artwork on top at about
             2:1 - the Shenzhen declaration under the APEC
             presidents cover, Russia's biggest barrage of the
             year on Kyiv, and GTA VI's record first day
  card rows  two rows of four cards, artwork on top,
             numbered, headline and short brief: the World
             Court judgment's fallout, Anthropic's debut
             close, the Riyadh tower strike, the burning
             Hormuz tanker, COP31's deal-less end, Kenya's
             last Ebola patient, Haiti's Martissant raid and
             the markets' fifth straight fall - eleven drawn
             stories in all
  bottom     WHERE IT HAPPENED at the left: the dot-matrix
             world map, the eleven drawn stories pinned by
             number, dots for the briefs, and the region
             legend; at the right, ALSO ON FRIDAY 20
             NOVEMBER - the remaining 26 stories as numbered
             one-liners in three columns, each with a bold
             lead word, wire-style and terse so the type can
             stay large
  footer     the red DATE CHECK strip and the sources line

The page is built to be read at thumbnail, half and full
size, which is how the judge compares entries: headlines
are big, briefs and one-liners keep their type floors, and
no picture is a sliced banner - every card shows its scene
whole on its focal window.

Stories are numbered in reading order, 1 to 37. All wording
is set here in PIL from the story data below; the
illustrations are text-free artwork, so no lettering can
come out garbled. SOURCES.md is the verification record
behind every line.

Output is entry.png beside this file. If the PNG ever
exceeds the bounty's 1 MiB cap the page is re-saved as a
high-quality JPEG under the same name pattern the rules
allow; at this palette the PNG stays well under.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ASSETS = HERE / "assets"
OUT = HERE / "entry.png"

W = H = 1024
PAPER = (247, 242, 231)
INK = (26, 26, 30)
GRAY = (110, 104, 94)
NAVY = (22, 50, 74)
CARD = (255, 253, 247)
RULE = (198, 188, 168)
RED = (178, 34, 40)
PLUM = (122, 44, 92)
TEAL = (14, 116, 104)
GOLD = (176, 124, 24)
GREEN = (46, 120, 62)
DARKRED = (154, 30, 34)

FDIR = "/usr/share/fonts/truetype"
FONTS = {
    "title": (f"{FDIR}/noto/NotoSerif-Black.ttf", 37),
    "kicker": (f"{FDIR}/liberation/LiberationSans-Bold.ttf", 10),
    "standfirst": (f"{FDIR}/liberation/LiberationSerif-Italic.ttf", 12),
    "counts": (f"{FDIR}/liberation/LiberationSans-Bold.ttf", 10),
    "badge1": (f"{FDIR}/liberation/LiberationSans-Bold.ttf", 13),
    "badge2": (f"{FDIR}/noto/NotoSerif-Black.ttf", 30),
    "badge3": (f"{FDIR}/liberation/LiberationSans-Bold.ttf", 8),
    "band": (f"{FDIR}/liberation/LiberationSans-Bold.ttf", 10),
    "tl_head": (f"{FDIR}/liberation/LiberationSans-Bold.ttf", 11),
    "tl_time": (f"{FDIR}/liberation/LiberationSans-Bold.ttf", 10),
    "tl_text": (f"{FDIR}/liberation/LiberationSans-Regular.ttf", 10),
    "kick": (f"{FDIR}/liberation/LiberationSans-Bold.ttf", 9),
    "lead_head": (f"{FDIR}/noto/NotoSerif-Bold.ttf", 24),
    "lead_brief": (f"{FDIR}/liberation/LiberationSerif-Regular.ttf", 12),
    "head": (f"{FDIR}/noto/NotoSerif-Bold.ttf", 15),
    "brief": (f"{FDIR}/liberation/LiberationSerif-Regular.ttf", 11),
    "tag": (f"{FDIR}/liberation/LiberationSans-Bold.ttf", 8),
    "num": (f"{FDIR}/liberation/LiberationSans-Bold.ttf", 10),
    "map_head": (f"{FDIR}/liberation/LiberationSans-Bold.ttf", 11),
    "map_pin": (f"{FDIR}/liberation/LiberationSans-Bold.ttf", 8),
    "legend": (f"{FDIR}/liberation/LiberationSans-Bold.ttf", 8),
    "also_head": (f"{FDIR}/liberation/LiberationSans-Bold.ttf", 11),
    "also_num": (f"{FDIR}/liberation/LiberationSans-Bold.ttf", 11),
    "also_lead": (f"{FDIR}/liberation/LiberationSans-Bold.ttf", 11),
    "also_text": (f"{FDIR}/liberation/LiberationSans-Regular.ttf", 11),
    "datecheck": (f"{FDIR}/liberation/LiberationSans-Bold.ttf", 9),
    "sources": (f"{FDIR}/liberation/LiberationSans-Regular.ttf", 9),
}
F = {k: ImageFont.truetype(p, s) for k, (p, s) in FONTS.items()}

REGION_BAND = [
    ("ASIA", 6, RED), ("EUROPE", 7, NAVY), ("AMERICAS", 8, PLUM),
    ("MIDDLE EAST", 6, TEAL), ("AFRICA", 4, GOLD),
    ("OCEANIA", 2, GREEN), ("GLOBAL", 4, GRAY),
]

TIMELINE = [
    ("OVERNIGHT", "110 missiles fall on Kyiv"),
    ("MORNING", "Merz: no new Yalta"),
    ("MIDDAY", "COP31: no deal yet"),
    ("19:38 UTC", "GTA VI: $3.79bn day"),
    ("21:00 UTC", "Fifth straight fall"),
]

HERO_CROP = (40, 450, 1560, 1164)  # APEC cover, reader-approved

LEADS = [
    dict(n=1, art="hero-apec.png", hero=True, color=RED,
         kicker="ASIA · SHENZHEN",
         head="Three powers publish the Shenzhen text",
         brief="A four-point text on nuclear risk, UN reform, energy "
               "and the ICC - silent on Ukraine and Iran.",
         tag="REUTERS · ONE TURN"),
    dict(n=2, art="illo-kyiv.png", focal=0.45, color=NAVY,
         kicker="EUROPE · KYIV",
         head="Biggest barrage of the year falls on Kyiv",
         brief="At least 110 missiles overnight; nine killed, three "
               "Dnipro bridges hit. Poland scrambles NATO jets.",
         tag="CNN · REUTERS"),
    dict(n=3, art="illo-gta.png", focal=0.447, color=PLUM,
         kicker="AMERICAS · GAMES",
         head="GTA VI makes $3.79bn in a single day",
         brief="Rockstar confirms the biggest entertainment launch "
               "in history: 32.5m copies sold before release day "
               "even ended.",
         tag="REUTERS · BUSINESS WIRE"),
]

ROWS = [
    dict(n=4, art="illo-icj.png", focal=0.5, color=NAVY,
         kicker="EUROPE · THE HAGUE",
         head="Genocide ruling lands on Myanmar",
         brief="Myanmar is found responsible for genocide against "
               "the Rohingya; reparations ordered.",
         tag="ONE TURN"),
    dict(n=5, art="illo-anthropic.png", focal=0.492, color=PLUM,
         kicker="AMERICAS · MARKETS",
         head="Anthropic ends debut up 17% as AI stocks slide",
         brief="ANT closes 17% above its $83 IPO price, but doubts "
               "over AI values drag world markets down.",
         tag="ONE TURN · REUTERS"),
    dict(n=6, art="illo-riyadh.png", focal=0.72, color=TEAL,
         kicker="MIDDLE EAST · RIYADH",
         head="Houthi missile damages Riyadh's PIF tower",
         brief="Missiles damage the sovereign wealth fund's tower "
               "and other buildings in the capital.",
         tag="ONE TURN"),
    dict(n=7, art="illo-hormuz.png", focal=0.38, color=TEAL,
         kicker="MIDDLE EAST · HORMUZ",
         head="Tanker burns in Hormuz as attacks step up",
         brief="A tanker catches fire after striking a mine; "
               "Iran's tanker attacks intensify in the war's "
               "ninth month.",
         tag="ONE TURN · UKMTO"),
    dict(n=8, art="illo-cop31.png", focal=0.568, color=GRAY,
         kicker="GLOBAL · ANTALYA",
         head="COP31's last day ends without a deal",
         brief="The final draft drops fossil fuels and the $120bn "
               "adaptation pledge; talks run over.",
         tag="AFP · ONE TURN"),
    dict(n=9, art="illo-kenya.png", focal=0.58, color=GOLD,
         kicker="AFRICA · NAIROBI",
         head="Kenya discharges its last Ebola patient",
         brief="Thirty-seven days after the first case, the last "
               "patient goes home - the outbreak nears its end.",
         tag="ONE TURN"),
    dict(n=10, art="illo-haiti.png", focal=0.32, color=PLUM,
         kicker="AMERICAS · PORT-AU-PRINCE",
         head="Haiti police kill 34 in Martissant raid",
         brief="Police say 34 suspected gang members died in the "
               "raid; the account is unverified.",
         tag="REUTERS · ONE TURN"),
    dict(n=11, art="illo-markets.png", focal=0.5, color=GRAY,
         kicker="GLOBAL · MARKETS",
         head="Fifth straight fall for world stocks",
         brief="S&P 500 -2.0%, Nikkei -4.8%, gold -4.2%; Brent "
               "crude climbs to $90.05 a barrel.",
         tag="ONE TURN"),
]

BRIEFS = [
    (12, RED, "Bangladesh:", "riots before Hasina return"),
    (13, RED, "N. Korea:", "enrichment expanding"),
    (14, RED, "Japan:", "inflation up, hike nears"),
    (15, RED, "Taiwan:", "2,700 suspect accounts"),
    (16, RED, "S. Korea:", "first cholera in a decade"),
    (17, NAVY, "Merz:", "no new Yalta over Europe"),
    (18, NAVY, "Brussels:", "EU-UK second summit held"),
    (19, NAVY, "Denmark:", "Greenland deal ratified"),
    (20, NAVY, "Ukraine:", "drones hit Smolensk plant"),
    (21, NAVY, "Crimea:", "Putin vows strike reply"),
    (22, PLUM, "Washington:", "cyber director fired"),
    (23, PLUM, "California:", "Nvidia subpoenaed on chips"),
    (24, PLUM, "Bukele:", "registers for third term"),
    (25, PLUM, "Caracas:", "US military deal signed"),
    (26, PLUM, "Brazil:", "Raoni land recognised"),
    (27, TEAL, "Gaza:", "troops cross Yellow Line"),
    (28, TEAL, "Iraq:", "militia quits Jurf al-Nasr"),
    (29, TEAL, "Israel:", "mosque torched in north"),
    (30, TEAL, "Pentagon:", "Iran campaign cost $48.3bn"),
    (31, GOLD, "Senegal:", "dozens missing in capsize"),
    (32, GOLD, "Sudan:", "10 killed at gold mine"),
    (33, GOLD, "Somalia:", "UAE ambassador expelled"),
    (34, GREEN, "Fiji-Tonga:", "drought disasters declared"),
    (35, GREEN, "S. Pacific:", "Cyclone Xavier hits Cat 4"),
    (36, GRAY, "IMF:", "debt to near 100% of GDP"),
    (37, GRAY, "Mercury:", "probe arrives after 8 yrs"),
]

MAP_PIN_DATA = [
    (1, 114.1, 22.5, RED), (2, 30.5, 50.4, NAVY),
    (4, 4.3, 52.1, NAVY), (6, 46.7, 24.6, TEAL),
    (7, 56.3, 26.5, TEAL), (8, 30.7, 36.9, GRAY),
    (9, 36.8, -1.3, GOLD), (10, -72.3, 18.5, PLUM),
]
MAP_PILL = ("3·5·11", -74.0, 40.7, PLUM)
MAP_DOTS = [
    (90.4, 23.8, RED), (125.8, 39.7, RED), (13.4, 52.5, NAVY),
    (-66.9, 10.5, PLUM), (34.3, 31.4, TEAL), (-17.4, 14.7, GOLD),
    (178.4, -18.1, GREEN),
]

DATE_CHECK_1 = ("DATE CHECK - Every story here happened, or was first "
                "reported, on Friday 20 November 2026.")
DATE_CHECK_2 = ("The Shenzhen summit and the ICJ judgment were Thursday's; "
                "Friday brought their texts and fallout. Claims are "
                "attributed.")
SOURCES_LINE = ("Sources: Reuters · AP · AFP · BBC · CNN · One Turn · "
                "Open Chronicle · Business Wire · UKMTO · UN News")

MASTHEAD_H = 90
RAINBOW_H = 17
TIMELINE_H = 34
LEAD_ART_H = 124
CARD_ART_H = 94
MAP_W, MAP_H = 300, 94


def load_fonts():
    return F


def wrap(d, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def make_wide(path, tw, th, focal=0.5):
    im = Image.open(path).convert("RGB")
    src_ratio = th / tw
    win_w = im.width
    win_h = int(win_w * src_ratio)
    if win_h > im.height:
        win_h = im.height
        win_w = int(win_h / src_ratio)
    cx = int(im.width * focal)
    x0 = min(max(cx - win_w // 2, 0), im.width - win_w)
    y0 = (im.height - win_h) // 2
    return im.crop((x0, y0, x0 + win_w, y0 + win_h)).resize((tw, th),
                                                           Image.LANCZOS)


def make_hero(path, tw, th):
    im = Image.open(path).convert("RGB")
    return im.crop(HERO_CROP).resize((tw, th), Image.LANCZOS)


def shrink_to_fit(d, text, font_path, size, max_w, floor=8):
    while size > floor:
        f = ImageFont.truetype(font_path, size)
        if d.textlength(text, font=f) <= max_w:
            return f
        size -= 1
    return ImageFont.truetype(font_path, floor)


def draw_masthead(d):
    d.rectangle([0, 0, W, MASTHEAD_H], fill=NAVY)
    d.text((118, 10), "THE WORLD IN ONE DAY", font=F["kicker"],
           fill=(255, 255, 255))
    d.text((116, 21), "Friday 20 November 2026", font=F["title"],
           fill=(255, 255, 255))
    d.text((118, 62),
           "Everything on this page happened, or was first reported, "
           "on Friday 20 November 2026.",
           font=F["standfirst"], fill=(216, 222, 235))
    d.text((118, 76), "37 STORIES · 7 REGIONS · 11 DRAWN · ONE PAGE",
           font=F["counts"], fill=(240, 200, 90))
    d.rounded_rectangle([24, 8, 100, 82], 8, fill=(240, 244, 250))
    d.text((62, 11), "NOV", font=F["badge1"], fill=NAVY, anchor="ma")
    d.text((62, 26), "20", font=F["badge2"], fill=NAVY, anchor="ma")
    d.text((62, 60), "FRI · 2026", font=F["badge3"], fill=NAVY,
           anchor="ma")


def draw_band(d, y):
    total = sum(c for _, c, _ in REGION_BAND)
    x = 24
    for name, count, color in REGION_BAND:
        w_ = int((W - 48) * count / total)
        d.rectangle([x, y, x + w_, y + RAINBOW_H], fill=color)
        label = f"{name} {count}"
        tw = d.textlength(label, font=F["band"])
        d.text((x + (w_ - tw) / 2, y + 3), label, font=F["band"],
               fill=(255, 255, 255))
        x += w_
    return y + RAINBOW_H


def draw_timeline(d, y):
    d.rectangle([24, y, 122, y + TIMELINE_H], fill=NAVY)
    d.text((32, y + 4), "THE DAY", font=F["tl_head"],
           fill=(255, 255, 255))
    d.text((32, y + 18), "IN UTC", font=F["tl_head"],
           fill=(255, 255, 255))
    n = len(TIMELINE)
    bw = (W - 48 - 98 - 6 - (n - 1) * 6) / n
    x = 128.0
    for time, text in TIMELINE:
        d.rectangle([x, y, x + bw, y + TIMELINE_H], fill=(238, 233, 220))
        d.text((x + 8, y + 3), time, font=F["tl_time"], fill=DARKRED)
        d.text((x + 8, y + 18), text, font=F["tl_text"], fill=INK)
        x += bw + 6
    return y + TIMELINE_H


def draw_card(d, img, x, y, w_, story, lead=False):
    art_h = LEAD_ART_H if lead else CARD_ART_H
    head_f = F["lead_head"] if lead else F["head"]
    brief_f = F["lead_brief"] if lead else F["brief"]
    head_lh = 31 if lead else 19
    brief_lh = 15 if lead else 13
    head_lines = wrap(d, story["head"], head_f, w_ - 16)
    brief_lines = wrap(d, story["brief"], brief_f, w_ - 16)
    assert len(head_lines) <= 2, (story["n"], head_lines)
    assert len(brief_lines) <= 3, (story["n"], brief_lines)
    height = (art_h + 3 + 13 + 4 + len(head_lines) * head_lh + 2
              + len(brief_lines) * brief_lh + 4 + 11 + 8)
    d.rectangle([x, y, x + w_, y + height], fill=CARD)
    d.rectangle([x, y, x + w_, y + height], outline=RULE)
    if story.get("hero"):
        art = make_hero(ASSETS / story["art"], int(w_), art_h)
    else:
        art = make_wide(ASSETS / story["art"], int(w_), art_h,
                        story.get("focal", 0.5))
    img.paste(art, (int(x), int(y)))
    d.ellipse([x + w_ - 30, y + art_h - 30, x + w_ - 6, y + art_h - 6],
              fill=story["color"])
    d.text((x + w_ - 18, y + art_h - 24), str(story["n"]),
           font=F["num"], fill=(255, 255, 255), anchor="ma")
    ty = y + art_h + 3
    d.text((x + 8, ty), story["kicker"], font=F["kick"],
           fill=story["color"])
    ty += 13
    for ln in head_lines:
        ty += 4
        d.text((x + 8, ty), ln, font=head_f, fill=INK)
        ty += head_lh - 4
    ty += 2
    for ln in brief_lines:
        d.text((x + 8, ty), ln, font=brief_f, fill=(52, 48, 44))
        ty += brief_lh
    ty += 4
    d.text((x + 8, ty), story["tag"], font=F["tag"], fill=GRAY)
    return y + height


def draw_cards(d, img, y):
    gap = 10
    lead_w = (W - 48 - 2 * gap) / 3
    lead_bottom = y
    for i, story in enumerate(LEADS):
        b = draw_card(d, img, 24 + i * (lead_w + gap), y, lead_w,
                      story, lead=True)
        lead_bottom = max(lead_bottom, b)
    y = lead_bottom + gap
    card_w = (W - 48 - 3 * gap) / 4
    row_bottom = y
    for i, story in enumerate(ROWS):
        if i == 4:
            y = row_bottom + gap
        b = draw_card(d, img, 24 + (i % 4) * (card_w + gap), y,
                      card_w, story)
        row_bottom = max(row_bottom, b)
    return row_bottom


def lonlat_to_xy(lon, lat, x0, y0):
    return (x0 + (lon + 180) / 360 * MAP_W,
            y0 + (85 - lat) / 125 * MAP_H)


def draw_map(d, x, y):
    d.text((x, y), "WHERE IT HAPPENED", font=F["map_head"], fill=NAVY)
    my = y + 16
    rows = MAP_ROWS
    assert len(rows) == 25 and all(len(r) == 100 for r in rows)
    cw_ = MAP_W / 100
    ch_ = MAP_H / 25
    for ri, row in enumerate(rows):
        for ci, ch in enumerate(row):
            if ch != ".":
                d.ellipse([x + ci * cw_ + 0.4, my + ri * ch_ + 0.4,
                           x + (ci + 1) * cw_ - 0.4,
                           my + (ri + 1) * ch_ - 0.4],
                          fill=(198, 190, 172))
    for lon, lat, color in MAP_DOTS:
        px, py = lonlat_to_xy(lon, lat, x, my)
        d.ellipse([px - 2.5, py - 2.5, px + 2.5, py + 2.5], fill=color)
    for n, lon, lat, color in MAP_PIN_DATA:
        px, py = lonlat_to_xy(lon, lat, x, my)
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=color)
        d.text((px, py - 6), str(n), font=F["map_pin"],
               fill=(255, 255, 255), anchor="ma")
    label, lon, lat, color = MAP_PILL
    px, py = lonlat_to_xy(lon, lat, x, my)
    pw = d.textlength(label, font=F["map_pin"]) + 10
    d.rounded_rectangle([px - pw / 2, py - 8, px + pw / 2, py + 8], 8,
                        fill=color)
    d.text((px, py - 6), label, font=F["map_pin"],
           fill=(255, 255, 255), anchor="ma")
    ly = my + MAP_H + 6
    d.text((x, ly),
           "ASIA 6 · EUROPE 7 · AMERICAS 8 · MID EAST 6 · AFRICA 4 · "
           "OCEANIA 2 · GLOBAL 4",
           font=F["legend"], fill=GRAY)
    return ly + 12


def draw_also(d, x, y, w_):
    d.text((x, y), "ALSO ON FRIDAY 20 NOVEMBER", font=F["also_head"],
           fill=NAVY)
    ty = y + 14
    per_col = (len(BRIEFS) + 2) // 3
    col_w = w_ / 3
    for i, (n, color, lead, rest) in enumerate(BRIEFS):
        col, row = divmod(i, per_col)
        cx = x + col * col_w
        cy = ty + row * 13
        d.text((cx, cy), f"{n}", font=F["also_num"], fill=color)
        lx = cx + d.textlength(f"{n} ", font=F["also_num"])
        d.text((lx, cy), lead, font=F["also_lead"], fill=INK)
        rx = lx + d.textlength(lead + " ", font=F["also_lead"])
        f_rest = shrink_to_fit(d, rest, FONTS["also_text"][0], 11,
                               x + (col + 1) * col_w - 8 - rx)
        d.text((rx, cy), rest, font=f_rest, fill=(52, 48, 44))
    return ty + per_col * 13


def draw_footer(d, y):
    d.rectangle([24, y, W - 24, y + 26], fill=DARKRED)
    d.text((36, y + 2), DATE_CHECK_1, font=F["datecheck"],
           fill=(255, 255, 255))
    d.text((36, y + 14), DATE_CHECK_2, font=F["datecheck"],
           fill=(255, 235, 235))
    d.text((24, y + 29), SOURCES_LINE, font=F["sources"], fill=GRAY)
    return y + 40


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_masthead(d)
    y = draw_band(d, MASTHEAD_H + 2) + 4
    y = draw_timeline(d, y) + 4
    y = draw_cards(d, img, y) + 6
    map_bottom = draw_map(d, 24, y)
    also_bottom = draw_also(d, 24 + MAP_W + 16, y - 2, W - 48 - MAP_W - 16)
    bottom = max(map_bottom, also_bottom)
    end = draw_footer(d, bottom + 4)
    assert end <= H - 2, f"page overflow: ends at {end}"
    img.save(OUT)
    size = OUT.stat().st_size
    if size > 1_048_576:
        img.save(OUT.with_suffix(".jpg"), quality=88)
        print(f"PNG too big ({size}); wrote JPEG instead")
    else:
        print(f"wrote {OUT} ({size} bytes)")


# The real dot-matrix land grid (100 x 25), loaded here so the
# data tables above stay readable.
MAP_ROWS = [
    "......####............................####............#.........##.###......###.....#.....#.........",
    "....#####..##.##.##.................#########............................######...#######......##...",
    "...########################..........#######........##############################################..",
    "...############################.......#####........################################################.",
    "....####################....######.....###...#.....################################################.",
    ".....#######.###########.....######.....#.......##..#############################################...",
    "................#################...............###############################################.....",
    ".................###############...............################################################.....",
    "................###############................###..######################################..........",
    "................##############.....................#.####################################...........",
    ".................############................#########################################..............",
    "....................######.##...............########################################................",
    ".....................#####..................####################################....#...............",
    "........................###.#######.........#####################.....##########..###...............",
    "............................###########......###################.......##...##......................",
    "............................############......#################............#########..###...........",
    "............................############.......#############.#.............################.........",
    ".............................##########.........#############...................###....#####........",
    ".............................##########.........############...................####.................",
    ".............................#########...........##########..##...................##########........",
    ".............................########............#########...###.................############.......",
    ".............................#######..............#######....##..................############.......",
    ".............................######...............######..........................##########........",
    ".............................#####.................####............................########.....##..",
    ".............................####.....................................................#####.....###.",
]

if __name__ == "__main__":
    main()
