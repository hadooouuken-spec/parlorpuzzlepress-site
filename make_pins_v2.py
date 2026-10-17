"""Second wave of Pinterest pins (2026-10-16): new angles on the same site pages.

Challenge pins show a real puzzle from the free sample; gift pins show the real covers.
Output: dist/pins/v2-*.jpg (1000x1500). Run after build_site.py, which wipes dist/.
"""
import pathlib
import pymupdf
from PIL import Image, ImageDraw, ImageFont

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = HERE / "dist" / "pins"
F = "C:/Windows/Fonts/"
W, H = 1000, 1500
SITE = "parlorpuzzlepress.netlify.app"
CREAM = (252, 246, 232)


def font(name, size):
    return ImageFont.truetype(F + name, size)


def page(pdf, n, dpi=200):
    pix = pymupdf.open(ROOT / "printables" / pdf)[n - 1].get_pixmap(dpi=dpi)
    return Image.frombytes("RGB", (pix.width, pix.height), pix.samples)


def crop(im, box):
    x0, y0, x1, y1 = box
    return im.crop((int(x0 * im.width), int(y0 * im.height), int(x1 * im.width), int(y1 * im.height)))


def cover(name, width):
    c = Image.open(ROOT / "covers" / name).convert("RGB")
    return c.resize((width, int(c.height * width / c.width)), Image.LANCZOS)


def centered(d, y, text, f, fill):
    d.text(((W - d.textlength(text, font=f)) / 2, y), text, font=f, fill=fill)


def fit(d, text, name, size, maxw):
    while d.textlength(text, font=font(name, size)) > maxw:
        size -= 2
    return font(name, size)


def frame(bg, acc, tag, headline):
    img = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([60, 50, W - 60, 130], 18, fill=acc)
    centered(d, 66, tag, fit(d, tag, "arialbd.ttf", 40, W - 160), (25, 25, 25))
    y = 165
    for line in headline:
        f = fit(d, line, "arialbd.ttf", 76, W - 100)
        centered(d, y, line, f, (255, 255, 255))
        y += 88
    return img, d, y


def footer(d, line, acc):
    centered(d, H - 150, line, fit(d, line, "arial.ttf", 36, W - 100), (240, 236, 228))
    centered(d, H - 95, SITE, font("arial.ttf", 34), acc)


def puzzle_pin(out, bg, acc, tag, headline, pdf, pg, box, cov, foot):
    img, d, y = frame(bg, acc, tag, headline)
    pz = crop(page(pdf, pg), box)
    pw = W - 120
    pz = pz.resize((pw, int(pz.height * pw / pz.width)), Image.LANCZOS)
    cv = cover(cov, 260)
    room = H - 190 - (y + 30) - 120          # leave space for the cover overlap and footer
    if pz.height > room:                     # shrink to fit rather than cut a line in half
        pz = pz.resize((int(pw * room / pz.height), room), Image.LANCZOS)
    py = y + 30
    px = (W - pz.width) // 2
    d.rectangle([px - 6, py - 6, px + pz.width + 6, py + pz.height + 6], fill=(255, 255, 255))
    img.paste(pz, (px, py))
    cy = min(py + pz.height - 60, H - 190 - cv.height)
    d.rectangle([W - cv.width - 46, cy - 4, W - 36, cy + cv.height + 4], fill=acc)
    img.paste(cv, (W - cv.width - 40, cy))
    footer(d, foot, acc)
    img.save(OUT / out, quality=90)
    return out


def covers_pin(out, bg, acc, tag, headline, covs, foot):
    img, d, y = frame(bg, acc, tag, headline)
    per = 2 if len(covs) == 4 else 3
    cw, gap = (330, 40) if per == 2 else (285, 26)
    rows = [covs[:per], covs[per:]]
    hs = [max(int(cover(c, cw).height) for c in r) for r in rows if r]
    total = sum(hs) + 40 * (len(hs) - 1)
    cy = y + 20 + max(0, (H - 200 - (y + 20) - total) // 2)
    for row in rows:
        if not row:
            continue
        x0 = (W - len(row) * cw - (len(row) - 1) * gap) // 2
        hmax = 0
        for k, c in enumerate(row):
            im = cover(c, cw)
            x = x0 + k * (cw + gap)
            d.rectangle([x - 4, cy - 4, x + cw + 4, cy + im.height + 4], fill=acc)
            img.paste(im, (x, cy))
            hmax = max(hmax, im.height)
        cy += hmax + 40
    footer(d, foot, acc)
    img.save(OUT / out, quality=90)
    return out


def coloring_pin(out):
    bg, acc = (150, 28, 34), (236, 196, 106)
    img, d, y = frame(bg, acc, "FREE PRINTABLE COLORING PAGES",
                      ["Bold & Easy Christmas", "Coloring for Seniors"])
    names = ["puppy-christmas-tree", "snow-globe", "gingerbread", "cat-armchair-christmas"]
    tw, gap = 420, 40
    cy = y + 40
    for k, n in enumerate(names):
        im = Image.open(HERE / "dist" / "img" / f"{n}-coloring-page-colored.jpg").convert("RGB")
        im = im.resize((tw, int(im.height * tw / im.width)), Image.LANCZOS)
        if im.height > tw:
            im = im.crop((0, (im.height - tw) // 2, tw, (im.height - tw) // 2 + tw))
        x = (W - 2 * tw - gap) // 2 + (k % 2) * (tw + gap)
        yy = cy + (k // 2) * (tw + gap)
        d.rectangle([x - 5, yy - 5, x + tw + 5, yy + im.height + 5], fill=CREAM)
        img.paste(im, (x, yy))
    footer(d, "Thick lines • Big spaces • Free PDFs", acc)
    img.save(OUT / out, quality=90)
    return out


made = [
    puzzle_pin("v2-whodunit-challenge.jpg", (18, 26, 44), (232, 192, 104), "CAN YOU SOLVE IT?",
               ["Who Killed", "Mr. Sedley?"], "whodunit-free-sample-case.pdf", 2,
               (0.06, 0.05, 0.94, 0.705), "cover_mysteries_front.png",
               "Free printable murder mystery + logic grid"),
    puzzle_pin("v2-witty-challenge.jpg", (86, 26, 22), (236, 196, 116), "CAN YOU CRACK THE CODE?",
               ["Decode This", "Famous Quote"], "witty-cryptograms-free-sample.pdf", 2,
               (0.04, 0.03, 0.96, 0.375), "cover_cryptograms_front.png",
               "Large print cryptograms • Hint letters included"),
    puzzle_pin("v2-xmas-cryptogram-challenge.jpg", (20, 52, 38), (232, 196, 110), "FREE PRINTABLE",
               ["Decode a Line From", "A Christmas Carol"], "christmas-cryptograms-free-sample.pdf", 2,
               (0.04, 0.03, 0.96, 0.405), "cover_xmas_cryptograms_front.png",
               "Large print Christmas cryptograms for adults"),
    puzzle_pin("v2-wordsearch-bigletters.jpg", (120, 20, 24), (240, 204, 120), "FREE PRINTABLE • LARGE PRINT",
               ["Big-Letter Christmas", "Word Search"], "christmas-word-search-free-sample.pdf", 2,
               (0.05, 0.03, 0.95, 0.62), "cover_xmas_wordsearch_front.png",
               "Easy to read for seniors • Free puzzles to print"),
    puzzle_pin("v2-advent-day1.jpg", (16, 28, 58), (236, 196, 106), "AN ADVENT CALENDAR FOR PUZZLE LOVERS",
               ["24 Christmas Mysteries,", "One a Day"], "advent-whodunits-free-sample.pdf", 2,
               (0.06, 0.05, 0.94, 0.595), "cover_advent_front.png",
               "Try December 1 free • Cozy, never gory"),
    covers_pin("v2-gifts-puzzle-lovers.jpg", (34, 30, 46), (236, 196, 106), "CHRISTMAS GIFT IDEAS",
               ["Gifts for", "Puzzle Lovers"],
               ["cover_mysteries_front.png", "cover_advent_front.png", "cover_cryptograms_front.png",
                "cover_xmas_cryptograms_front.png", "cover_xmas_wordsearch_front.png"],
               "Mysteries, cryptograms & word searches • Free samples"),
    covers_pin("v2-stocking-stuffers-seniors.jpg", (24, 60, 44), (240, 204, 120), "LARGE PRINT • EASY TO READ",
               ["Stocking Stuffers for", "Grandma & Grandpa"],
               ["cover_xmas_wordsearch_front.png", "cover_xmas_cryptograms_front.png", "coloring_cover_front.png",
                "cover_cryptograms_front.png"],
               "Puzzle & coloring books for seniors • Free samples"),
    coloring_pin("v2-coloring-seniors.jpg"),
]
print("\n".join(made))
