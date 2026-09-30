# Parlor Puzzle Press — free printables site

Static site: one page per puzzle book with a free printable sample PDF and a Pinterest pin image.

- Edit `books.json` (set each book's `amazon_url` once it is live on Amazon).
- Rebuild: `python build_site.py` (needs pymupdf + pillow; reads ../printables and ../covers).
- `dist/` is the published folder (Netlify publish directory; no build command).
