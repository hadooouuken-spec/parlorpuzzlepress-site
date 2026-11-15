"""Daily pin batch v5 (2026-11-15). New angles on existing site pages.

Output: dist/pins/v5-*.jpg plus pins_v5.json (title, description, link, board, date) for posting.
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

W2, LJ = "cover_wd2_front.png", "cover_mem_front.png"
TEAL = (22, 78, 76)

PINS = [
    ("11-16", "v5-whodunit2-new.jpg", lambda f: puzzle_pin(f, INK, G, "NEW: BOOK 2", ["80 New Murder", "Mysteries to Solve"],
                                                          "whodunit-book-2-free-sample.pdf", 1, (0.04, 0.03, 0.96, 0.62), W2,
                                                          "Free printable case  •  Logic grid included"),
     "New Murder Mystery Logic Puzzles for Adults (Free Printable Case)",
     "Whodunit Logic Puzzles Book 2 is here: 80 brand-new cozy murder mysteries in 16 new settings, from an observatory to an airship. Print a free case with its logic grid and name the killer.",
     SITE + "murder-mystery-logic-puzzles-book-2-printable/", MYST),
    ("11-18", "v5-lemonade-new.jpg", lambda f: puzzle_pin(f, TEAL, G, "FREE PRINTABLE • LARGE PRINT", ["Nostalgic Word Search", "for Seniors"],
                                                         "lemonade-jukeboxes-free-sample.pdf", 2, (0.05, 0.03, 0.95, 0.88), LJ,
                                                         "Soda fountains, drive-ins & more • Answers included"),
     "Nostalgic Large Print Word Search for Seniors (Free Printable)",
     "Large print word searches full of memories: the soda fountain, drive-in movies, the five-and-dime and Sunday dinner. Bold letters and only 16 words per puzzle. Print two free puzzles with answers.",
     SITE + "nostalgic-word-search-large-print-printable/", WORD),
    ("11-25", "v5-thanksgiving-quiet.jpg", lambda f: covers_pin(f, (92, 46, 22), G, "AFTER THE BIG DINNER", ["Quiet Puzzles for", "a Cozy Afternoon"],
                                                               [W2, LJ, XS, XP], "Large print • Free samples to try"),
     "Cozy Puzzle Books for a Quiet Holiday Afternoon",
     "After the big dinner, settle in with a puzzle: cozy murder mysteries, a nostalgic large print word search, Christmas sudoku and a 110-puzzle variety book. Try free printable samples of each.",
     SITE, GIFT),
    ("11-27", "v5-gifts-grandparents.jpg", lambda f: covers_pin(f, RED, G, "CHRISTMAS GIFT IDEAS", ["Gifts for Grandparents", "Who Love Puzzles"],
                                                               [LJ, XW, XS, SC], "Large print • Under $15 • Free samples"),
     "Christmas Gifts for Grandparents Who Love Puzzles",
     "Christmas gifts for grandma and grandpa: large print word searches full of memories, Christmas sudoku and a bold, easy coloring book. All under $15, with free samples to try.",
     SITE, GIFT),
    ("11-29", "v5-mystery-series.jpg", lambda f: covers_pin(f, INK, G, "A SERIES FOR MYSTERY FANS", ["Whodunit Logic Puzzles", "Books 1 and 2"],
                                                           [WH, W2], "160 cozy cases • Free sample of each"),
     "Whodunit Logic Puzzles: A Murder Mystery Puzzle Book Series",
     "Two books of cozy murder mystery logic puzzles: 160 cases in all, each with suspects, motives, real clues and a logic grid. Every case has exactly one solution. Print a free case from each book.",
     SITE + "murder-mystery-logic-puzzles-book-2-printable/", MYST),
    ("12-01", "v5-advent-today.jpg", lambda f: puzzle_pin(f, (16, 28, 58), G, "STARTS DECEMBER 1", ["A Christmas Mystery", "for Every Day of Advent"],
                                                         "advent-whodunits-free-sample.pdf", 2, (0.04, 0.03, 0.96, 0.595), AD,
                                                         "Print the December 1 case free"),
     "Advent Mystery Puzzles: A Cozy Christmas Case for Every Day",
     "Advent starts today. Solve a cozy Christmas mystery each day from December 1 to 24, family-friendly and never gory. Print the December 1 case free, with its logic grid.",
     SITE + "christmas-mystery-puzzle-printable/", XMAS),
    ("12-03", "v5-sudoku-seniors.jpg", lambda f: puzzle_pin(f, (22, 48, 74), G, "LARGE PRINT SUDOKU", ["Big Digits,", "Easy on the Eyes"],
                                                           "snowfall-sudoku-free-sample.pdf", 2, (0.06, 0.05, 0.94, 0.76), XS,
                                                           "Free printable puzzles with answers"),
     "Large Print Christmas Sudoku That's Easy on the Eyes",
     "Christmas sudoku with big, clear digits and thick box lines, one puzzle per page. Print two free puzzles with answers. A cozy holiday brain teaser for adults and seniors.",
     SITE + "large-print-christmas-sudoku-printable/", XMAS),
    ("12-05", "v5-word-lovers-xmas.jpg", lambda f: covers_pin(f, GREEN, G, "STOCKING STUFFERS", ["For the Word Lover", "on Your List"],
                                                             [XC, WI, LJ], "Codes, quotes & word searches • Free samples"),
     "Stocking Stuffers for Word Lovers: Cryptograms and Word Searches",
     "Stocking stuffers for word lovers: Christmas cryptograms from holiday classics, witty quotes from Twain and Wilde, and nostalgic large print word searches. Free printable samples of each.",
     SITE, GIFT),
    ("12-07", "v5-coloring-winter.jpg", lambda f: covers_pin(f, (34, 84, 74), G, "BOLD & EASY", ["Christmas Coloring", "for Adults and Seniors"],
                                                            [SC, BB], "Thick lines • Big shapes • Free pages"),
     "Bold and Easy Christmas Coloring for Adults and Seniors",
     "Bold and easy coloring with thick lines and big, simple shapes: a Christmas book and a four-seasons book. A calm gift for mom or grandma. Print some free pages to try first.",
     SITE + "free-christmas-coloring-pages/", COLOR),
    ("12-09", "v5-last-minute.jpg", lambda f: covers_pin(f, RED, G, "CHRISTMAS GIFT IDEAS", ["Puzzle Gifts to Put", "Under the Tree"],
                                                        [XP, XS, AD, W2], "Large print • Free samples to try"),
     "Puzzle Book Gifts to Put Under the Tree",
     "Puzzle book gifts to put under the tree: a 110-puzzle variety book, Christmas sudoku, an Advent mystery calendar and new murder mystery logic puzzles. Try free printable samples of each.",
     SITE, GIFT),
]

records = []
for date, name, make, title, desc, link, board in PINS:
    make(name)
    shutil.copy(OUT / name, STAGE / name)
    assert len(title) <= 100 and len(desc) <= 500, name
    records.append({"date": date, "file": name, "title": title, "desc": desc, "link": link, "board": board})
(HERE / "pins_v5.json").write_text(json.dumps(records, indent=1), encoding="utf-8")
print(len(records), "pins")
