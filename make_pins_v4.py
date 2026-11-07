"""Daily Christmas pin batch (2026-11-07). New angles on existing site pages.

Output: dist/pins/v4-*.jpg plus pins_v4.json (title, description, link, board, date) for posting.
Run after build_site.py, which wipes dist/.
"""
import json
import pathlib
import shutil
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from make_pins_v2 import OUT, covers_pin, puzzle_pin  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
STAGE = pathlib.Path(r"C:\Users\hadoo\Downloads\10k-websites-skill\_kdp-upload-staging\pins")
SITE = "https://parlorpuzzlepress.netlify.app/"
XP, XS, XW, XC = ("cover_xmas_parlor_front.png", "cover_xmas_sudoku_front.png",
                  "cover_xmas_wordsearch_front.png", "cover_xmas_cryptograms_front.png")
AD, WH, NO, WI, BS, SC, BB = ("cover_advent_front.png", "cover_mysteries_front.png", "cover_nonograms_front.png",
                              "cover_cryptograms_front.png", "cover_bigsud_front.png", "coloring_cover_front.png",
                              "cover_blossoms_front.png")
GIFT, XMAS, MYST, WORD, COLOR = ("Christmas Gifts for Puzzle Lovers", "Christmas Printables and Puzzles",
                                 "Murder Mystery Logic Puzzles", "Cryptograms and Word Puzzles",
                                 "Bold and Easy Coloring Pages")
RED, GREEN, NAVY, WINE, INK = (120, 24, 30), (24, 60, 44), (22, 48, 74), (86, 26, 22), (18, 26, 44)
G = (240, 204, 120)

PINS = [
    ("11-09", "v4-under-15.jpg", lambda f: covers_pin(f, RED, G, "PRICED UNDER $15", ["Christmas Gifts Under $15", "for Puzzle Lovers"],
                                                     [XP, XW, AD, NO], "Try a free sample of each before you buy"),
     "Christmas Gifts Under $15 for Puzzle Lovers",
     "Affordable Christmas gifts for puzzle lovers, all under $15: a large print puzzle variety book, a Christmas word search, an Advent mystery calendar and murder mystery nonograms. Free samples to try first.",
     SITE, GIFT),
    ("11-11", "v4-cryptogram-code.jpg", lambda f: puzzle_pin(f, GREEN, G, "CAN YOU CRACK IT?", ["Christmas Code", "Puzzles for Adults"],
                                                            "christmas-cryptograms-free-sample.pdf", 2, (0.04, 0.03, 0.96, 0.486), XC,
                                                            "Hint letters included • Free printable"),
     "Christmas Code Puzzles for Adults (Free Printable Cryptograms)",
     "Christmas cryptograms for adults and seniors: decode lines from classic holiday stories, letter by letter. Large print, with hint letters to get you started. Print a free sample today.",
     SITE + "christmas-cryptograms-printable/", XMAS),
    ("11-13", "v4-seniors-activities.jpg", lambda f: puzzle_pin(f, WINE, G, "FREE TO PRINT", ["Christmas Activities", "for Seniors"],
                                                               "christmas-parlor-free-sample.pdf", 4, (0.05, 0.05, 0.95, 0.88), XP,
                                                               "Large print word search, codes & mazes"),
     "Free Printable Christmas Activities for Seniors",
     "Free large print Christmas activities for seniors: a word search, a Christmas code and a maze, with answers. Easy to print for a parent, a grandparent or an activity group. Plain white pages and big, clear print.",
     SITE + "christmas-puzzles-for-seniors-printable/", XMAS),
    ("11-15", "v4-stocking-stuffers.jpg", lambda f: covers_pin(f, GREEN, G, "CHRISTMAS STOCKING IDEAS", ["Stocking Stuffers", "for Adults Who Love Puzzles"],
                                                              [NO, XC, AD, XS], "Free samples of every book"),
     "Stocking Stuffers for Adults Who Love Puzzles",
     "Stocking stuffers for adults: murder mystery picture puzzles, Christmas cryptograms, an Advent mystery calendar and large print sudoku. Try a free printable sample of each one before you buy.",
     SITE, GIFT),
    ("11-16", "v4-whodunit-gift.jpg", lambda f: covers_pin(f, INK, G, "A GIFT FOR MYSTERY FANS", ["Gifts for People Who", "Love a Good Mystery"],
                                                          [WH, NO, AD], "Cozy cases, never gory • Free samples"),
     "Gifts for Mystery Lovers: Cozy Murder Mystery Puzzle Books",
     "Gifts for anyone who loves a good mystery: cozy murder mystery logic puzzles, picture puzzles with a culprit to name, and an Advent calendar of Christmas cases. Print a free sample case of each.",
     SITE, MYST),
    ("11-17", "v4-big-sudoku.jpg", lambda f: puzzle_pin(f, NAVY, G, "FREE PRINTABLE • LARGE PRINT", ["Big, Clear Sudoku", "One Puzzle Per Page"],
                                                       "big-parlor-sudoku-free-sample.pdf", 2, (0.06, 0.05, 0.94, 0.76), BS,
                                                       "Easy to Very Hard • Answers included"),
     "Large Print Sudoku for Adults and Seniors (Free Printable)",
     "Large print sudoku that's easy on the eyes: big digits, roomy squares and thick box lines, one puzzle per page. Print a free sample with answers. From The Big Parlor Sudoku Book.",
     SITE + "large-print-sudoku-printable/", WORD),
    ("11-18", "v4-word-search-gift.jpg", lambda f: puzzle_pin(f, RED, G, "NOSTALGIC CHRISTMAS PUZZLES", ["A Word Search", "That Feels Like Home"],
                                                             "christmas-word-search-free-sample.pdf", 2, (0.05, 0.03, 0.95, 0.62), XW,
                                                             "Big letters • Free puzzles to print"),
     "Nostalgic Large Print Christmas Word Search (Free Printable)",
     "A large print Christmas word search full of nostalgic holiday themes, with big, bold letters. A cozy activity for a winter afternoon. Print free puzzles today, with answers.",
     SITE + "christmas-word-search-large-print/", XMAS),
    ("11-19", "v4-coloring-gift.jpg", lambda f: covers_pin(f, (34, 84, 74), G, "BOLD & EASY COLORING", ["Coloring Books", "for Mom & Grandma"],
                                                          [SC, BB], "Thick lines • Big shapes • Free pages to print"),
     "Bold and Easy Coloring Books for Mom and Grandma",
     "A gentle gift for mom or grandma: bold and easy coloring books with thick lines and big, simple shapes. One for Christmas and one for all four seasons. Print some free pages to try first.",
     SITE + "bold-easy-coloring-pages-seasons-printable/", COLOR),
    ("11-20", "v4-nonogram-howto.jpg", lambda f: puzzle_pin(f, INK, G, "NEW TO NONOGRAMS?", ["How to Solve a", "Picture Logic Puzzle"],
                                                           "whodunit-nonograms-free-sample.pdf", 1, (0.04, 0.03, 0.96, 0.9), NO,
                                                           "Beginner's guide + a free case to print"),
     "How to Solve a Nonogram: Easy Beginner's Guide",
     "New to nonograms? Learn how to solve these picture logic puzzles in a few simple steps, then try a free cozy murder mystery case. Also called griddlers, hanjie or paint by numbers.",
     SITE + "murder-mystery-nonogram-printable/", MYST),
    ("11-21", "v4-witty-gift.jpg", lambda f: puzzle_pin(f, WINE, G, "A GIFT FOR WORD LOVERS", ["Decode the Wit of", "Twain and Wilde"],
                                                       "witty-cryptograms-free-sample.pdf", 2, (0.04, 0.03, 0.96, 0.522), WI,
                                                       "300 large print quotes • Free sample"),
     "Cryptogram Puzzle Book Gift: Mark Twain and Oscar Wilde Quotes",
     "A gift for word lovers: large print cryptograms that hide clever quotes from Mark Twain, Oscar Wilde, Benjamin Franklin and Ambrose Bierce. Hint letters included. Print a free sample.",
     SITE + "cryptograms-large-print-printable/", WORD),
    ("11-22", "v4-family-night.jpg", lambda f: puzzle_pin(f, NAVY, G, "CHRISTMAS GAME NIGHT", ["Solve a Christmas", "Mystery Together"],
                                                         "advent-whodunits-free-sample.pdf", 2, (0.04, 0.03, 0.96, 0.595), AD,
                                                         "Family-friendly • Free printable case"),
     "Christmas Mystery Puzzle for Game Night (Free Printable)",
     "A family-friendly Christmas mystery to solve together: the case of the angel's wings, with suspects, clues and a logic grid. Cozy, never gory. Free to print for a holiday game night.",
     SITE + "christmas-mystery-puzzle-printable/", XMAS),
    ("11-23", "v4-teacher-coworker.jpg", lambda f: covers_pin(f, GREEN, G, "EASY CHRISTMAS GIFT IDEAS", ["Small Gifts for", "Coworkers & Neighbors"],
                                                             [XC, XS, SC, AD], "Under $15 • Free samples to try"),
     "Small Christmas Gifts for Coworkers and Neighbors",
     "Small Christmas gifts under $15 for coworkers and neighbors who enjoy a quiet hobby: Christmas cryptograms, sudoku, a coloring book and an Advent mystery calendar. Try free samples first.",
     SITE, GIFT),
    ("11-24", "v4-black-friday-free.jpg", lambda f: covers_pin(f, (28, 28, 34), G, "FREE TO PRINT", ["Free Christmas Puzzles", "to Keep Everyone Busy"],
                                                              [XP, XW, XS], "Word searches, sudoku & more • Free PDFs"),
     "Free Christmas Puzzles to Print for the Holidays",
     "Free printable Christmas puzzles to keep everyone busy at the holidays: large print word searches, sudoku, codes and mazes. Download the free PDFs and print at home.",
     SITE, XMAS),
]

records = []
for date, name, make, title, desc, link, board in PINS:
    make(name)
    shutil.copy(OUT / name, STAGE / name)
    assert len(title) <= 100 and len(desc) <= 500, name
    records.append({"date": date, "file": name, "title": title, "desc": desc, "link": link, "board": board})
(HERE / "pins_v4.json").write_text(json.dumps(records, indent=1), encoding="utf-8")
print(len(records), "pins")
