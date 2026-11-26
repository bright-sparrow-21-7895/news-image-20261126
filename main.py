"""One-day world news image for Thursday 26 November 2026.

Draws a 1024 by 1024 editorial infographic with PIL: a navy header
naming the day, then six numbered stories from 26 November 2026, each
with a one-line factual summary, and writes it to /output/entry.png.
"""
import os

from PIL import Image, ImageDraw, ImageFont

OUT_DIR = "/output"
OUT = os.path.join(OUT_DIR, "entry.png")
MAX_BYTES = 1048576
MAX_DIM = 1024

W, H = 1024, 1024
NAVY = (20, 27, 51)
GOLD = (232, 163, 61)
BG = (247, 245, 240)
INK = (20, 27, 51)
GREY = (90, 100, 114)
DIVIDER = (216, 210, 200)
FOOTER_GREY = (110, 116, 128)

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

# (kicker, headline, summary, tile colour)
STORIES = [
    ("US TRADE",
     "US proposes tariffs on 14 partners",
     "New duties proposed on 14 economies over excess capacity.",
     (31, 122, 140)),
    ("KUWAIT",
     "Drone strike kills two Italians",
     "Italy blames Iran for the attack; Tehran denies any role.",
     (192, 57, 43)),
    ("EUROPE",
     "EU split over \u20ac45bn Ukraine loan",
     "Leaders debate a \u20ac45bn loan for Ukraine and the next budget.",
     (46, 125, 50)),
    ("HEALTH",
     "Ebola cases pass 12,000 in DR Congo",
     "Outbreak tops 12,000 cases, the second-largest on record.",
     (230, 126, 34)),
    ("EGYPT",
     "31 killed in Cairo tanker fire",
     "A fuel tanker overturns and explodes on Cairo's ring road.",
     (125, 60, 152)),
    ("UNITED STATES",
     "Macy's parade postponed by storm",
     "Thanksgiving parade moves to Saturday, a first in 100 years.",
     (44, 95, 158)),
]

HEADER_H = 176
ROW_H = 134


def fit_font(draw, text, path, start, minimum, max_width):
    """Largest font size at or below start that fits text in max_width."""
    size = start
    while size > minimum:
        font = ImageFont.truetype(path, size)
        if draw.textlength(text, font=font) <= max_width:
            return font
        size -= 1
    return ImageFont.truetype(path, minimum)


def main():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    # Header: navy band naming the day.
    draw.rectangle([0, 0, W, HEADER_H], fill=NAVY)
    kicker_font = ImageFont.truetype(FONT_BOLD, 34)
    draw.text((48, 34), "WORLD NEWS \u2022 THURSDAY", font=kicker_font,
              fill=(165, 178, 205))
    date_font = fit_font(draw, "26 NOVEMBER 2026", FONT_BOLD, 84, 60, W - 96)
    draw.text((48, 74), "26 NOVEMBER 2026", font=date_font, fill=(255, 255, 255))
    draw.rectangle([48, 164, 248, 172], fill=GOLD)

    # Six numbered stories.
    text_x = 172
    text_w = W - text_x - 48
    for i, (kicker, headline, summary, colour) in enumerate(STORIES):
        y = HEADER_H + i * ROW_H
        # Number tile.
        draw.rounded_rectangle([48, y + 22, 140, y + 110], radius=14, fill=colour)
        num_font = ImageFont.truetype(FONT_BOLD, 52)
        num = str(i + 1)
        nw = draw.textlength(num, font=num_font)
        draw.text((94 - nw / 2, y + 34), num, font=num_font, fill=(255, 255, 255))
        # Kicker, headline, one-line summary.
        kick_font = ImageFont.truetype(FONT_BOLD, 25)
        draw.text((text_x, y + 16), kicker, font=kick_font, fill=colour)
        head_font = fit_font(draw, headline, FONT_BOLD, 42, 34, text_w)
        draw.text((text_x, y + 46), headline, font=head_font, fill=INK)
        sum_font = fit_font(draw, summary, FONT_REG, 27, 22, text_w)
        draw.text((text_x, y + 96), summary, font=sum_font, fill=GREY)
        if i < len(STORIES) - 1:
            draw.line([48, y + ROW_H, W - 48, y + ROW_H], fill=DIVIDER, width=2)

    # Footer: date and sources.
    foot_font = ImageFont.truetype(FONT_REG, 23)
    draw.text((48, 992), "Reported 26 November 2026  \u2022  Sources: Reuters / AP / Euronews",
              font=foot_font, fill=FOOTER_GREY)

    os.makedirs(OUT_DIR, exist_ok=True)
    img.save(OUT, format="PNG", optimize=True)
    size = os.path.getsize(OUT)
    if size > MAX_BYTES:
        raise ValueError("entry.png is over 1 MiB")
    if W > MAX_DIM or H > MAX_DIM:
        raise ValueError("entry.png is larger than 1024 by 1024 pixels")
    print("Wrote", OUT, "(", size, "bytes )")


if __name__ == "__main__":
    main()
