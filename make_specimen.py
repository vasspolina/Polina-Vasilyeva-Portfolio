#!/usr/bin/env python3
"""Render specimen images for the Dada typeface into source/dada/.

The index is a grid of images, so the typeface needs tiles like every other
project. Run before extract.py:

    python3 make_specimen.py && python3 extract.py dada && python3 build.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(ROOT, "fonts", "Dada-Regular.ttf")
OUT = os.path.join(ROOT, "source", "dada")
SCALE = 2          # the specimens are drawn at twice size for retina
PAD = 90 * SCALE

# The capitals Polina redrew; every other glyph is left as Helvetica Neue.
DADA_CAPS = "ACIMOPQRXY"


def face(size):
    return ImageFont.truetype(FONT, size)


def sheet(lines, size, leading=None, fg="black", bg=None, track=0):
    """Draw lines of text on a canvas sized to fit them.

    bg=None leaves the ground transparent, so the letterforms sit directly on
    the page rather than on a white card.
    """
    f = face(size)
    leading = leading or int(size * 1.05)
    d0 = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    widths = []
    for ln in lines:
        w = d0.textlength(ln, font=f) + track * max(0, len(ln) - 1)
        widths.append(w)
    W = int(max(widths)) + PAD * 2
    H = leading * len(lines) + PAD * 2
    im = Image.new("RGBA", (W, H), bg or (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for i, ln in enumerate(lines):
        y = PAD + i * leading
        if track:
            x = PAD
            for ch in ln:
                d.text((x, y), ch, font=f, fill=fg)
                x += d.textlength(ch, font=f) + track
        else:
            d.text((PAD, y), ln, font=f, fill=fg)
    return im


def ladder():
    """One line set at falling sizes, the way a specimen shows text grades."""
    sizes = [s * SCALE for s in (150, 104, 72, 50, 34, 24, 17)]
    text = "DADA IS NOT DEAD, IT SMELLS OF LAUGHTER"
    d0 = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    W = int(max(d0.textlength(text, font=face(s)) for s in sizes)) + PAD * 2
    H = sum(int(s * 1.5) for s in sizes) + PAD * 2
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    y = PAD
    for s in sizes:
        d.text((PAD, y), text, font=face(s), fill="black")
        y += int(s * 1.5)
    return im


def main():
    os.makedirs(OUT, exist_ok=True)

    # Capitals and figures only — the face has no lowercase of its own, so
    # setting any would fall back to the untouched Helvetica underneath.
    sheet(["DADA"], 460 * SCALE).save(f"{OUT}/hero.png")
    sheet([DADA_CAPS], 300 * SCALE, track=18 * SCALE).save(f"{OUT}/capitals.png")
    sheet(["DADA"], 460 * SCALE, fg="white", bg="black").save(f"{OUT}/inverted.png")

    sheet(["ABCDEFGHIJKLM",
           "NOPQRSTUVWXYZ",
           "0123456789",
           "&?!@#$%*() .,;:"], 150 * SCALE, leading=190 * SCALE).save(f"{OUT}/charset.png")

    sheet(["MOMA", "QUARTZ", "PARIS"], 260 * SCALE, leading=320 * SCALE).save(f"{OUT}/words.png")

    ladder().save(f"{OUT}/ladder.png")

    sheet(["THE BOURGEOIS REGARDED",
           "THE DADAIST AS A DISSOLUTE",
           "MONSTER, A REVOLUTIONARY",
           "VILLAIN, A BARBAROUS ASIATIC,",
           "PLOTTING AGAINST HIS BELLS."], 96 * SCALE, leading=130 * SCALE).save(f"{OUT}/setting.png")

    for f in sorted(os.listdir(OUT)):
        p = os.path.join(OUT, f)
        print(f"  {f:16} {Image.open(p).size}")


if __name__ == "__main__":
    main()
