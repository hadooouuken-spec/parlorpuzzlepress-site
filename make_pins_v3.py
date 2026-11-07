"""Christmas pin round (2026-11-07), using the newer books. Helpers come from make_pins_v2.

Output: dist/pins/v3-*.jpg (1000x1500). Run after build_site.py, which wipes dist/.
Importing make_pins_v2 also rebuilds the v2 pins, so one run restores both sets.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from make_pins_v2 import covers_pin, puzzle_pin  # noqa: E402

made = [
    covers_pin("v3-gifts-seniors.jpg", (120, 24, 30), (240, 204, 120), "LARGE PRINT CHRISTMAS GIFTS",
               ["Puzzle Gifts for", "Mom, Dad & Grandparents"],
               ["cover_xmas_parlor_front.png", "cover_xmas_sudoku_front.png",
                "coloring_cover_front.png", "cover_xmas_wordsearch_front.png"],
               "Try a free sample of each before you buy"),
    puzzle_pin("v3-snowfall-challenge.jpg", (22, 48, 74), (236, 204, 124), "FREE PRINTABLE • LARGE PRINT",
               ["Christmas Sudoku", "You Can Actually Read"], "snowfall-sudoku-free-sample.pdf", 2,
               (0.06, 0.05, 0.94, 0.76), "cover_xmas_sudoku_front.png",
               "Big digits • One puzzle per page • Easy to Very Hard"),
    puzzle_pin("v3-parlor-wordsearch.jpg", (24, 60, 44), (240, 204, 120), "FREE PRINTABLE CHRISTMAS PUZZLES",
               ["Cozy Puzzles for", "Quiet Winter Days"], "christmas-parlor-free-sample.pdf", 2,
               (0.05, 0.05, 0.95, 0.88), "cover_xmas_parlor_front.png",
               "Word searches, codes, mazes & sudoku for seniors"),
    puzzle_pin("v3-nonogram-gift.jpg", (18, 26, 44), (232, 192, 104), "A GIFT FOR MYSTERY LOVERS",
               ["Shade the Grid,", "Name the Culprit"], "whodunit-nonograms-free-sample.pdf", 4,
               (0.05, 0.05, 0.95, 0.82), "cover_nonograms_front.png",
               "Cozy murder mystery picture puzzles • Free sample"),
    puzzle_pin("v3-advent-countdown.jpg", (86, 26, 22), (236, 196, 116), "READY FOR DECEMBER 1?",
               ["A New Mystery Every", "Day Until Christmas"], "advent-whodunits-free-sample.pdf", 2,
               (0.04, 0.03, 0.96, 0.595), "cover_advent_front.png",
               "24 cozy cases • Try December 1 free"),
]
print("\n".join(made))
