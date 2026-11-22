"""Pin batch v6 (2026-11-22): Dec 10-20, the last-minute gift window, plus the two newest books.

Output: dist/pins/v6-*.jpg plus pins_v6.json (title, description, link, board, date) for posting.
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
W2, LJ, WS, RR = "cover_wd2_front.png", "cover_mem_front.png", "cover_win_front.png", "cover_gar_front.png"
GIFT, XMAS, MYST, WORD, COLOR = ("Christmas Gifts for Puzzle Lovers", "Christmas Printables and Puzzles",
                                 "Murder Mystery Logic Puzzles", "Cryptograms and Word Puzzles",
                                 "Bold and Easy Coloring Pages")
RED, GREEN, NAVY, WINE, INK = (120, 24, 30), (24, 60, 44), (22, 48, 74), (86, 26, 22), (18, 26, 44)
BROWN, GARDEN = (70, 34, 24), (36, 70, 44)
G = (240, 204, 120)

PINS = [
    ("12-10", "v6-woodstove-evening.jpg", lambda f: puzzle_pin(f, BROWN, G, "FREE PRINTABLE • LARGE PRINT", ["Winter Sudoku for", "Snowy Evenings"],
                                                               "woodstove-sudoku-free-sample.pdf", 2, (0.05, 0.03, 0.95, 0.80), WS,
                                                               "Big digits • One puzzle per page • Answers"),
     "Large Print Winter Sudoku for Snowy Evenings (Free Printable)",
     "Cozy large print winter sudoku for snowy evenings by the fire: big, clear digits and thick box lines, one puzzle per page. Print two free puzzles with a how-to page and answers. From Woodstove Sudoku.",
     SITE + "winter-sudoku-large-print-printable/", WORD),
    ("12-11", "v6-gardener-gift.jpg", lambda f: puzzle_pin(f, GARDEN, (244, 196, 200), "A GIFT FOR GARDENERS", ["Garden Word Search", "for Bird Lovers"],
                                                          "robins-roses-free-sample.pdf", 2, (0.05, 0.03, 0.95, 0.88), RR,
                                                          "Large print • 80 puzzles • Free sample"),
     "Christmas Gift for Gardeners: Large Print Garden Word Search",
     "A Christmas gift for the gardener who has everything: 80 large print word searches about spring bulbs, roses, songbirds at the feeder and the potting shed. Print two free puzzles with answers first.",
     SITE + "garden-word-search-large-print-printable/", GIFT),
    ("12-12", "v6-last-minute.jpg", lambda f: covers_pin(f, RED, G, "LAST-MINUTE GIFT IDEAS", ["Last-Minute Gifts", "for Puzzle Lovers"],
                                                        [XP, WH, XS, LJ], "Large print • Free samples of each"),
     "Last-Minute Christmas Gifts for Puzzle Lovers",
     "Still need a gift? Large print puzzle books for adults and seniors: a Christmas variety book, cozy murder mysteries, Christmas sudoku and a nostalgic word search. Print a free sample of each first.",
     SITE, GIFT),
    ("12-13", "v6-grandma-word-search.jpg", lambda f: covers_pin(f, (34, 84, 74), G, "GIFTS FOR GRANDMA", ["Word Search Books", "Grandma Will Love"],
                                                                [LJ, XW, RR], "Big letters • Easy to hard • Answers"),
     "Large Print Word Search Books Grandma Will Love",
     "Three large print word search books for grandma: nostalgic memories, an old-fashioned Christmas, and gardens and songbirds. Big bold letters, 16 words per puzzle and answers at the back. Free samples to print.",
     SITE, GIFT),
    ("12-14", "v6-christmas-eve-case.jpg", lambda f: puzzle_pin(f, NAVY, G, "SOLVE IT TOGETHER", ["A Christmas Mystery", "for Family Night"],
                                                               "advent-whodunits-free-sample.pdf", 2, (0.04, 0.03, 0.96, 0.62), AD,
                                                               "Cozy, never gory • Free printable case"),
     "Christmas Mystery to Solve as a Family (Free Printable Case)",
     "A cozy Christmas mystery to solve together after dinner: suspects, clues and a logic grid, with the answer explained. Family-friendly and never gory. Print the free case from Advent Whodunits.",
     SITE + "christmas-mystery-puzzle-printable/", XMAS),
    ("12-15", "v6-snow-day-seniors.jpg", lambda f: covers_pin(f, GREEN, G, "SNOW DAY ACTIVITIES", ["Cozy Puzzles for", "a Snow Day Indoors"],
                                                             [WS, XS, XP], "Large print • Free pages to print"),
     "Snow Day Activities for Seniors: Large Print Puzzles",
     "Snowed in? Large print puzzles for seniors to enjoy indoors: winter sudoku, Christmas sudoku and a 110-puzzle Christmas variety book. Print free sample pages today.",
     SITE + "christmas-puzzles-for-seniors-printable/", XMAS),
    ("12-16", "v6-mystery-series.jpg", lambda f: covers_pin(f, INK, G, "FOR MYSTERY FANS", ["A Mystery Puzzle", "Gift Set"],
                                                           [WH, W2, NO], "Name the culprit • Free sample cases"),
     "Murder Mystery Puzzle Books Gift Set for Adults",
     "A gift set for mystery fans: Whodunit Logic Puzzles Books 1 and 2, plus picture-logic murder mysteries. Cozy cases, never gory, with full solutions. Print a free case from each.",
     SITE, MYST),
    ("12-17", "v6-witty-quotes.jpg", lambda f: puzzle_pin(f, WINE, G, "FREE PRINTABLE", ["Crack a Clever Quote", "in Large Print"],
                                                         "witty-cryptograms-free-sample.pdf", 3, (0.04, 0.03, 0.96, 0.52), WI,
                                                         "Large print cryptograms • Hints included"),
     "Clever Quote Cryptograms for Adults (Free Printable, Large Print)",
     "Large print cryptograms that hide clever quotes from Mark Twain, Oscar Wilde and Benjamin Franklin. Hint letters get you started. Print three free puzzles today.",
     SITE + "cryptograms-large-print-printable/", WORD),
    ("12-18", "v6-calm-coloring.jpg", lambda f: covers_pin(f, (34, 84, 74), G, "A QUIET HOUR", ["Calm Coloring for", "the Busy Holidays"],
                                                          [SC, BB], "Thick lines • Big shapes • Free pages"),
     "Calm Coloring Pages for Adults During the Busy Holidays",
     "Take a quiet hour for yourself this holiday season: bold and easy coloring pages for adults and seniors, with thick lines and big, simple shapes. Print free pages to try.",
     SITE + "bold-easy-coloring-pages-seasons-printable/", COLOR),
    ("12-19", "v6-snowfall-sudoku.jpg", lambda f: puzzle_pin(f, NAVY, G, "FREE PRINTABLE • LARGE PRINT", ["Christmas Sudoku", "to Print at Home"],
                                                            "snowfall-sudoku-free-sample.pdf", 3, (0.05, 0.03, 0.95, 0.76), XS,
                                                            "One puzzle per page • Answers included"),
     "Free Printable Large Print Christmas Sudoku",
     "Print large print Christmas sudoku at home: big digits, roomy squares and one puzzle per page, with answers. A calm puzzle break for the week before Christmas. From Snowfall Sudoku.",
     SITE + "large-print-christmas-sudoku-printable/", XMAS),
    ("12-20", "v6-new-year-puzzles.jpg", lambda f: covers_pin(f, (28, 28, 34), G, "NEW YEAR, NEW PUZZLES", ["Puzzle Books for", "the Year Ahead"],
                                                             [WS, RR, W2, BS], "Not just for Christmas • Free samples"),
     "Puzzle Books to Enjoy All Year Long",
     "Puzzle books that last well past Christmas: winter sudoku, a garden word search, new murder mystery logic puzzles and a big book of large print sudoku. Try a free printable sample of each.",
     SITE, GIFT),
]

records = []
for date, name, make, title, desc, link, board in PINS:
    make(name)
    shutil.copy(OUT / name, STAGE / name)
    assert len(title) <= 100 and len(desc) <= 500, name
    records.append({"date": date, "file": name, "title": title, "desc": desc, "link": link, "board": board})
(HERE / "pins_v6.json").write_text(json.dumps(records, indent=1), encoding="utf-8")
print(len(records), "pins")
