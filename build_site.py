"""Static site: free printable puzzle samples, one page per book, plus Pinterest pin images.

Edit books.json (set "amazon_url" once a book is live), then run: python build_site.py
Output goes to site/dist/ (deploy that folder).
"""
import json, shutil, pathlib, html, datetime
import pymupdf
from PIL import Image, ImageDraw, ImageFont

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
DIST = HERE / "dist"
CFG = json.loads((HERE / "books.json").read_text(encoding="utf-8"))
SITE_URL = CFG["site_url"].rstrip("/")
F = "C:/Windows/Fonts/"

if DIST.exists():
    shutil.rmtree(DIST)
(DIST / "printables").mkdir(parents=True)
(DIST / "img").mkdir()
(DIST / "pins").mkdir()

CSS = """
:root{--bg:#fbf8f2;--ink:#1f2328;--muted:#5b616b;--accent:#8a1c2b;--card:#ffffff;--line:#e6dfd2;--btn:#8a1c2b;--btnink:#fff}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#15171a;--ink:#ece8e1;--muted:#a9adb4;--accent:#e2a3ad;--card:#1e2125;--line:#30343a;--btn:#e2a3ad;--btnink:#15171a}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:18px/1.6 Georgia,'Times New Roman',serif}
a{color:var(--accent)}header,main,footer{max-width:980px;margin:0 auto;padding:0 16px}
header{padding-top:28px}header a.brand{font:700 20px/1.2 system-ui,sans-serif;color:var(--ink);text-decoration:none}
h1{font:700 clamp(28px,5vw,42px)/1.15 system-ui,sans-serif;margin:24px 0 8px}h2{font:700 24px/1.25 system-ui,sans-serif;margin:32px 0 8px}
.lede{color:var(--muted);font-size:20px;max-width:720px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:20px;margin:24px 0}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;overflow:hidden;display:flex;flex-direction:column}
.card img{width:100%;height:auto;display:block;border-bottom:1px solid var(--line)}.card .body{padding:14px 16px 18px;flex:1;display:flex;flex-direction:column}
.card h3{font:700 19px/1.3 system-ui,sans-serif;margin:0 0 6px}.card p{margin:0 0 12px;color:var(--muted);font-size:16px;flex:1}
.btn{display:inline-block;background:var(--btn);color:var(--btnink);padding:12px 18px;border-radius:8px;text-decoration:none;font:600 17px/1 system-ui,sans-serif}
.btn.alt{background:transparent;color:var(--accent);border:2px solid var(--accent)}
.book{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.3fr);gap:28px;align-items:start;margin-top:12px}
.book img.cover{width:100%;max-width:340px;border-radius:6px;box-shadow:0 6px 24px rgba(0,0,0,.18)}
.previews{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:12px;margin:12px 0}
.previews img{width:100%;border:1px solid var(--line);border-radius:6px;background:#fff}
ul.facts{padding-left:22px}ul.facts li{margin:4px 0}
.note{font-size:15px;color:var(--muted)}footer{border-top:1px solid var(--line);margin-top:48px;padding:20px 16px 40px;color:var(--muted);font-size:15px}
@media (max-width:720px){.book{grid-template-columns:1fr}}
"""


def page(title, desc, body, path, image=None):
    canonical = f"{SITE_URL}/{path}".rstrip("/")
    og = f'<meta property="og:image" content="{SITE_URL}/{image}">' if image else ""
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title><meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{canonical}"><meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">{og}
<meta name="p:domain_verify" content="{CFG.get('pinterest_verify','')}">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🧩</text></svg>">
<style>{CSS}</style></head><body>
<header><a class="brand" href="/">🧩 {html.escape(CFG['brand'])}</a></header>
<main>{body}</main>
<footer>© {datetime.date.today().year} {html.escape(CFG['brand'])}. Free printables are for personal, classroom and activity-group use.
As an independent publisher, we link to our own books on Amazon.</footer></body></html>"""


def render_previews(pdf_path, slug, max_pages=3):
    d = pymupdf.open(pdf_path)
    out = []
    for i in range(min(max_pages, d.page_count - 1)):
        fn = f"img/{slug}-p{i + 1}.png"
        d[i + 1 if d.page_count > 2 else i].get_pixmap(dpi=60).save(str(DIST / fn))
        out.append(fn)
    return out


def buy_button(b):
    if b.get("amazon_url"):
        return f'<a class="btn alt" href="{html.escape(b["amazon_url"])}" rel="noopener">See the full book on Amazon</a>'
    return '<span class="note">Full book coming soon on Amazon.</span>'


def pin_image(b, cover_path, preview_path, out):
    W, H = 1000, 1500
    img = Image.new("RGB", (W, H), tuple(b["pin_bg"]))
    d = ImageDraw.Draw(img)
    fb = ImageFont.truetype(F + "arialbd.ttf", 74)
    fm = ImageFont.truetype(F + "arialbd.ttf", 40)
    fs = ImageFont.truetype(F + "arial.ttf", 34)
    d.rounded_rectangle([60, 50, W - 60, 130], 18, fill=tuple(b["pin_accent"]))
    tag = "FREE PRINTABLE"
    d.text(((W - d.textlength(tag, font=fm)) / 2, 66), tag, font=fm, fill=(25, 25, 25))
    y = 170
    for line in b["pin_headline"]:
        d.text(((W - d.textlength(line, font=fb)) / 2, y), line, font=fb, fill=(255, 255, 255))
        y += 86
    prev = Image.open(preview_path).convert("RGB")
    pw = 620
    prev = prev.resize((pw, int(prev.height * pw / prev.width)))
    ph = min(prev.height, H - y - 330)
    prev = prev.crop((0, 0, pw, ph))
    px, py = 60, y + 30
    d.rectangle([px - 6, py - 6, px + pw + 6, py + ph + 6], fill=(255, 255, 255))
    img.paste(prev, (px, py))
    cov = Image.open(cover_path).convert("RGB")
    cw = 300
    cov = cov.resize((cw, int(cov.height * cw / cov.width)))
    img.paste(cov, (W - cw - 40, py + ph - cov.height + 40))
    line = b["pin_footer"]
    d.text(((W - d.textlength(line, font=fs)) / 2, H - 150), line, font=fs, fill=(240, 236, 228))
    site = SITE_URL.replace("https://", "")
    d.text(((W - d.textlength(site, font=fs)) / 2, H - 95), site, font=fs, fill=tuple(b["pin_accent"]))
    img.save(out, quality=90)


cards, urls = [], [""]
for b in CFG["books"]:
    slug = b["slug"]
    sample = ROOT / "printables" / b["sample_pdf"]
    shutil.copy(sample, DIST / "printables" / b["sample_pdf"])
    cover_src = ROOT / "covers" / b["cover_front"]
    Image.open(cover_src).convert("RGB").save(DIST / f"img/{slug}-cover.jpg", quality=85)
    previews = render_previews(sample, slug)
    pin_image(b, cover_src, DIST / previews[0], DIST / f"pins/{slug}-pin.jpg")
    facts = "".join(f"<li>{html.escape(f)}</li>" for f in b["facts"])
    prev_html = "".join(f'<img src="/{p}" alt="Preview page {k + 1} of the free {html.escape(b["short"])} sample" loading="lazy">' for k, p in enumerate(previews))
    body = f"""<h1>{html.escape(b['h1'])}</h1><p class="lede">{html.escape(b['lede'])}</p>
<div class="book"><div><img class="cover" src="/img/{slug}-cover.jpg" alt="Cover of {html.escape(b['title'])}"></div>
<div><h2>Free sample to print</h2><p>{html.escape(b['sample_text'])}</p>
<p><a class="btn" href="/printables/{b['sample_pdf']}" download>Download the free PDF</a></p>
<div class="previews">{prev_html}</div>
<h2>About the full book</h2><p><strong>{html.escape(b['title'])}</strong></p><ul class="facts">{facts}</ul>
<p>{buy_button(b)}</p>
<p class="note">Printing tip: print at "actual size" (100%) on US Letter paper for the intended large print.</p></div></div>"""
    (DIST / slug).mkdir()
    (DIST / slug / "index.html").write_text(page(b["seo_title"], b["seo_desc"], body, f"{slug}/", f"img/{slug}-cover.jpg"), encoding="utf-8")
    urls.append(f"{slug}/")
    cards.append(f"""<div class="card"><a href="/{slug}/"><img src="/img/{slug}-cover.jpg" alt="{html.escape(b['title'])}" loading="lazy"></a>
<div class="body"><h3><a href="/{slug}/">{html.escape(b['card_title'])}</a></h3><p>{html.escape(b['card_text'])}</p>
<a class="btn" href="/{slug}/">Get the free printable</a></div></div>""")

# ---- free coloring pages: a hub plus one page per design, each with its own pin ----
COL = CFG.get("coloring")
if COL:
    CDIR = ROOT / "coloring"
    (DIST / "printables" / "coloring").mkdir()
    hub = COL["slug"]
    Image.open(ROOT / "covers" / COL["cover_front"]).convert("RGB").save(DIST / f"img/{hub}-cover.jpg", quality=85)
    RED, GREEN, CREAM, GOLD = (150, 28, 34), (24, 72, 48), (252, 246, 232), (236, 196, 106)

    def coloring_pin(p, out):
        W, H = 1000, 1500
        img = Image.new("RGB", (W, H), CREAM)
        d = ImageDraw.Draw(img)
        d.rectangle([0, 0, W, 330], fill=RED)
        fm = ImageFont.truetype(F + "arialbd.ttf", 38)
        fb = ImageFont.truetype(F + "georgiab.ttf", 66)
        fs = ImageFont.truetype(F + "arial.ttf", 32)
        tag = "FREE PRINTABLE"
        tw = d.textlength(tag, font=fm)
        d.rounded_rectangle([(W - tw) / 2 - 30, 40, (W + tw) / 2 + 30, 104], 16, fill=GOLD)
        d.text(((W - tw) / 2, 50), tag, font=fm, fill=(30, 20, 10))
        for k, line in enumerate([p["name"], "Christmas Coloring Page"]):
            s = 66
            while d.textlength(line, font=ImageFont.truetype(F + "georgiab.ttf", s)) > W - 80:
                s -= 2
            f = ImageFont.truetype(F + "georgiab.ttf", s)
            d.text(((W - d.textlength(line, font=f)) / 2, 128 + k * 86), line, font=f, fill=CREAM)
        line_art = Image.open(CDIR / "clean" / f"p{p['id']:02d}.png").convert("RGB")
        if p.get("colored"):
            col = Image.open(CDIR / p["colored"]).convert("RGB").resize((760, 760), Image.LANCZOS)
            d.rounded_rectangle([110, 370, 890, 1150], 24, fill=(255, 255, 255), outline=GREEN, width=6)
            img.paste(col, (120, 380))
            la = line_art.copy(); la.thumbnail((330, 330), Image.LANCZOS)
            bx, by = 40, 1000
            d.rounded_rectangle([bx, by, bx + 350, by + 340], 18, fill=(255, 255, 255), outline=RED, width=6)
            img.paste(la, (bx + (350 - la.width) // 2, by + (340 - la.height) // 2))
            fl = ImageFont.truetype(F + "arialbd.ttf", 40)
            d.text((430, 1190), "Print it & color it!", font=fl, fill=RED)
            d.text((430, 1245), "Bold lines, big spaces", font=fs, fill=GREEN)
        else:
            la = line_art.copy(); la.thumbnail((820, 820), Image.LANCZOS)
            d.rounded_rectangle([70, 370, 930, 1230], 24, fill=(255, 255, 255), outline=GREEN, width=6)
            img.paste(la, ((W - la.width) // 2, 370 + (860 - la.height) // 2))
            fl = ImageFont.truetype(F + "arialbd.ttf", 40)
            d.text(((W - d.textlength("Print it & color it!", font=fl)) / 2, 1265), "Print it & color it!", font=fl, fill=RED)
        d.rectangle([0, H - 150, W, H], fill=GREEN)
        foot = "Bold & easy  •  For adults & seniors  •  Free PDF"
        d.text(((W - d.textlength(foot, font=fs)) / 2, H - 130), foot, font=fs, fill=CREAM)
        site = SITE_URL.replace("https://", "")
        d.text(((W - d.textlength(site, font=fs)) / 2, H - 80), site, font=fs, fill=GOLD)
        img.save(out, quality=90)

    def hub_pin(out):
        W, H = 1000, 1500
        img = Image.new("RGB", (W, H), CREAM)
        d = ImageDraw.Draw(img)
        d.rectangle([0, 0, W, 360], fill=RED)
        fb = ImageFont.truetype(F + "georgiab.ttf", 70)
        fm = ImageFont.truetype(F + "arialbd.ttf", 38)
        fs = ImageFont.truetype(F + "arial.ttf", 32)
        n = len(COL["pages"])
        for k, line in enumerate([f"{n} Free Christmas", "Coloring Pages", "for Adults"]):
            d.text(((W - d.textlength(line, font=fb)) / 2, 40 + k * 100), line, font=fb, fill=CREAM)
        tiles = [p for p in COL["pages"] if p.get("colored")][:6]
        T, G = 300, 20
        x0 = (W - 3 * T - 2 * G) // 2
        for k, p in enumerate(tiles):
            src = Image.open(CDIR / p["colored"]).convert("RGB") if k % 2 == 0 else Image.open(CDIR / "clean" / f"p{p['id']:02d}.png").convert("RGB")
            src.thumbnail((T - 16, T - 16), Image.LANCZOS)
            x = x0 + (k % 3) * (T + G); y = 400 + (k // 3) * (T + G)
            d.rounded_rectangle([x, y, x + T, y + T], 16, fill=(255, 255, 255), outline=GREEN, width=4)
            img.paste(src, (x + (T - src.width) // 2, y + (T - src.height) // 2))
        tag = "PRINT FREE  •  BOLD & EASY"
        d.text(((W - d.textlength(tag, font=fm)) / 2, 1100), tag, font=fm, fill=RED)
        sub = "Thick lines and big spaces, made to relax"
        d.text(((W - d.textlength(sub, font=fs)) / 2, 1160), sub, font=fs, fill=GREEN)
        d.rectangle([0, H - 150, W, H], fill=GREEN)
        site = SITE_URL.replace("https://", "")
        d.text(((W - d.textlength(site, font=fm)) / 2, H - 100), site, font=fm, fill=GOLD)
        img.save(out, quality=90)

    book_btn = (f'<a class="btn alt" href="{html.escape(COL["amazon_url"])}" rel="noopener">Get all 50 designs on Amazon</a>'
                if COL.get("amazon_url") else '<span class="note">The full 50-design book is coming soon on Amazon.</span>')
    facts = "".join(f"<li>{html.escape(f)}</li>" for f in COL["facts"])
    about = f"""<h2>Want all 50?</h2><div class="book"><div><img class="cover" src="/img/{hub}-cover.jpg" alt="Cover of {html.escape(COL['book_title'])}"></div>
<div><p><strong>{html.escape(COL['book_title'])}</strong></p><ul class="facts">{facts}</ul><p>{book_btn}</p></div></div>"""
    hub_cards = []
    for p in COL["pages"]:
        shutil.copy(ROOT / "printables" / "coloring" / p["pdf"], DIST / "printables" / "coloring" / p["pdf"])
        la = Image.open(CDIR / "clean" / f"p{p['id']:02d}.png").convert("L"); la.thumbnail((700, 700), Image.LANCZOS)
        la.convert("RGB").save(DIST / f"img/{p['slug']}.jpg", quality=88)
        if p.get("colored"):
            Image.open(CDIR / p["colored"]).convert("RGB").resize((700, 700), Image.LANCZOS).save(DIST / f"img/{p['slug']}-colored.jpg", quality=85)
        coloring_pin(p, DIST / f"pins/{p['slug']}-pin.jpg")
        col_html = (f'<p class="note">Colored in, it can look like this:</p><img src="/img/{p["slug"]}-colored.jpg" alt="{html.escape(p["alt"])}, colored in" loading="lazy" style="max-width:340px;width:100%;border-radius:8px;border:1px solid var(--line)">'
                    if p.get("colored") else "")
        body = f"""<h1>Free {html.escape(p['name'].lower())} Christmas coloring page</h1><p class="lede">{html.escape(p['text'])}</p>
<div class="book"><div><img src="/img/{p['slug']}.jpg" alt="{html.escape(p['alt'])}, coloring page" style="width:100%;max-width:420px;background:#fff;border:1px solid var(--line);border-radius:8px"></div>
<div><h2>Print it free</h2><p>A bold, easy design with thick lines, sized for US Letter paper. Free for personal, classroom and activity-group use.</p>
<p><a class="btn" href="/printables/coloring/{p['pdf']}" download>Download the free PDF</a></p>{col_html}
<p><a href="/{hub}/">See all {len(COL['pages'])} free Christmas coloring pages</a></p></div></div>{about}"""
        title = f"Free {p['name']} Christmas Coloring Page for Adults (Printable PDF)"
        desc = f"Free printable {p['name'].lower()} Christmas coloring page for adults and seniors. Bold, easy design with thick lines. Download the PDF."
        (DIST / p["slug"]).mkdir()
        (DIST / p["slug"] / "index.html").write_text(page(title, desc, body, f"{p['slug']}/", f"pins/{p['slug']}-pin.jpg"), encoding="utf-8")
        urls.append(f"{p['slug']}/")
        hub_cards.append(f"""<div class="card"><a href="/{p['slug']}/"><img src="/img/{p['slug']}.jpg" alt="{html.escape(p['alt'])}" loading="lazy" style="background:#fff"></a>
<div class="body"><h3><a href="/{p['slug']}/">{html.escape(p['name'])}</a></h3><a class="btn" href="/printables/coloring/{p['pdf']}" download>Free PDF</a></div></div>""")
    hub_pin(DIST / f"pins/{hub}-pin.jpg")
    body = f"""<h1>{html.escape(COL['h1'])}</h1><p class="lede">{html.escape(COL['lede'])}</p>
<div class="grid">{''.join(hub_cards)}</div>
<p class="note">Printing tip: print at "actual size" (100%). Markers can bleed through thin paper, so card stock works best.</p>{about}"""
    (DIST / hub).mkdir()
    (DIST / hub / "index.html").write_text(page(COL["seo_title"], COL["seo_desc"], body, f"{hub}/", f"pins/{hub}-pin.jpg"), encoding="utf-8")
    urls.append(f"{hub}/")
    cards.insert(0, f"""<div class="card"><a href="/{hub}/"><img src="/img/{COL['pages'][1]['slug']}-colored.jpg" alt="Free Christmas coloring pages for adults" loading="lazy"></a>
<div class="body"><h3><a href="/{hub}/">Christmas coloring pages</a></h3><p>{len(COL['pages'])} bold, easy holiday designs for adults and seniors. Free PDFs.</p>
<a class="btn" href="/{hub}/">Get the free pages</a></div></div>""")

home = f"""<h1>{html.escape(CFG['home_h1'])}</h1><p class="lede">{html.escape(CFG['home_lede'])}</p>
<div class="grid">{''.join(cards)}</div>
<h2>Made for real solvers</h2><p>{html.escape(CFG['home_about'])}</p>"""
(DIST / "index.html").write_text(page(CFG["home_title"], CFG["home_desc"], home, ""), encoding="utf-8")
sm = "".join(f"<url><loc>{SITE_URL}/{u}</loc></url>" for u in urls)
(DIST / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>', encoding="utf-8")
(DIST / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n", encoding="utf-8")
(DIST / "404.html").write_text(page("Page not found", "Page not found", '<h1>Page not found</h1><p><a href="/">Back to the free printables</a></p>', "404"), encoding="utf-8")
print("built", len(CFG["books"]), "book pages ->", DIST)
