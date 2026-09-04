#!/usr/bin/env python3
"""Render the site from data.py + manifest.json.

    python3 extract.py && python3 build.py

Writes index.html and projects/<slug>.html.
"""
import json, os

import data

import collections

ROOT = os.path.dirname(os.path.abspath(__file__))
MANIFEST = json.load(open(os.path.join(ROOT, "manifest.json")))

# A deck page that split into several pieces gives each the page's caption, so
# adjacent images can carry byte-identical alt text. Number those for screen
# readers, which otherwise announce the same thing three times in a row.
ALT_SUFFIX = {}
for _slug, _items in MANIFEST.items():
    _counts = collections.Counter(i["caption"] for i in _items)
    _seen = collections.Counter()
    for _i in _items:
        _cap = _i["caption"]
        if _counts[_cap] > 1:
            _seen[_cap] += 1
            ALT_SUFFIX[(_slug, _i["stem"])] = f" ({_seen[_cap]} of {_counts[_cap]})"

# A project whose source images have not landed yet would otherwise render as
# an empty page and a dead link in the pager. Leave it out until it has art.
SKIPPED = [p["slug"] for p in data.PROJECTS if not MANIFEST.get(p["slug"])]
PROJECTS = [p for p in data.PROJECTS if MANIFEST.get(p["slug"])]

# Stamp the stylesheet so a browser (or the preview server) cannot serve a
# stale one after an edit.
CSS_V = int(os.path.getmtime(os.path.join(ROOT, "css", "style.css")))
JS_V = int(os.path.getmtime(os.path.join(ROOT, "js", "site.js")))

# extract.py wipes and regenerates assets/ on every run, sometimes rewriting a
# file's pixels under the same name (a re-crop, a new DPR rendition). Without a
# version stamp the browser cache keeps serving the old bytes at that URL
# forever, which is what "the images went blurry again" always turns out to be.
ASSET_V = int(os.path.getmtime(os.path.join(ROOT, "manifest.json")))

# Phone mockups and posters are tall and narrow. Left alone they would fill a
# whole grid column and tower over the landscape shots, so they are capped and
# centred instead of blown up to full width.
PORTRAIT_RATIO = 0.8



def no_orphan(text):
    """Bind the last two words so a line cannot end on one word alone.

    text-wrap: pretty asks the browser to avoid it, but it works to a budget
    and gives up on long paragraphs. A non-breaking space between the final two
    words is not a request.
    """
    if not text:
        return text
    # the last space that is not inside a tag
    depth, last = 0, -1
    for i, ch in enumerate(text):
        if ch == "<":
            depth += 1
        elif ch == ">":
            depth -= 1
        elif ch == " " and depth == 0:
            last = i
    if last != -1:
        text = text[:last] + "\u00a0" + text[last + 1:]
    return bind_sentence_start(text)


def bind_sentence_start(text):
    """Bind the first two words of every sentence, so a line cannot end with
    just the opening word of the next sentence stranded there alone."""
    if not text:
        return text
    out = list(text)
    depth = 0
    at_sentence_start = True
    in_word = False
    word_num = 0
    for i, ch in enumerate(text):
        if ch == "<":
            depth += 1
            in_word = False
            continue
        if ch == ">":
            depth -= 1
            continue
        if depth > 0:
            continue
        if ch in " \t\n":
            if in_word and at_sentence_start and word_num == 1:
                out[i] = "\u00a0"
                at_sentence_start = False
            in_word = False
        elif ch in ".!?":
            in_word = False
            at_sentence_start = True
            word_num = 0
        else:
            if not in_word:
                in_word = True
                if at_sentence_start:
                    word_num += 1
    return "".join(out)

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def head(title, depth, desc):
    pre = "../" * depth
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{esc(desc)}">
<link rel="icon" href="{pre}favicon.svg?v={CSS_V}" type="image/svg+xml">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="{pre}og.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="preload" href="{pre}fonts/PPTelegraf-Regular.otf" as="font" type="font/otf" crossorigin>
<link rel="stylesheet" href="{pre}css/style.css?v={CSS_V}">
<script>
(function(){{var t=localStorage.getItem('theme');if(t)document.documentElement.dataset.theme=t;}})();
</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
"""


def nav(depth, here="work"):
    pre = "../" * depth

    def link(key, href, label):
        if key == here:
            return f'<a class="nav-link is-active" href="{href}" aria-current="page">{label}</a>'
        return f'<a class="nav-link" href="{href}">{label}</a>'

    return f"""<header class="nav">
  <a class="nav-name" href="{pre}index.html">{data.NAME}</a>
  {link("work", pre + "index.html", "Work")}
  {link("about", pre + "about.html", "About")}
  {link("contact", pre + "contact.html", "Contact")}
  <button class="theme-toggle" type="button" role="switch" aria-checked="false"
          aria-label="Dark mode">
    <span class="switch" aria-hidden="true"><span class="knob"></span></span>
    <span class="switch-label">Dark mode</span>
  </button>
</header>
"""


def footer(depth):
    pre = "../" * depth
    return f"""<footer class="footer">
  <p><a href="mailto:{data.EMAIL}">{data.EMAIL}</a></p>
  <p><a href="tel:+1{data.PHONE.replace(' ', '')}">+1 {data.PHONE}</a> ·
     <a href="{data.LINKEDIN}" rel="me noopener">LinkedIn</a></p>
  <p class="footer-copy">{data.LOCATION} · © 2026 {data.NAME}</p>
</footer>
<script src="{pre}js/site.js?v={JS_V}"></script>
</body>
</html>"""


def picture(slug, item, alt, depth, sizes, eager=False):
    pre = "../" * depth
    alt += ALT_SUFFIX.get((slug, item["stem"]), "")
    loading = "eager" if eager else "lazy"
    base = f"{pre}assets/{slug}/{item['stem']}"
    srcset = [f"{base}-{n}.webp?v={ASSET_V} {n}w" for n in item["widths"]]
    src = f'{base}-{item["widths"][-1]}.webp?v={ASSET_V}'
    return (f'<img src="{src}" srcset="{", ".join(srcset)}" '
            f'sizes="{sizes}" width="{item["w"]}" height="{item["h"]}" '
            f'loading="{loading}" decoding="async" alt="{esc(alt)}">')


def is_portrait(item):
    return item["w"] / item["h"] < PORTRAIT_RATIO


# Tell the browser the real rendered width, so a phone mockup capped at 300px
# fetches the small rendition instead of the full-column one.
# These have to describe the width an image actually renders at, or the browser
# picks a rendition too small and upscales it. The page is no longer a 1200px
# measure: it runs full width inside --page-pad, so a cell is a fraction of the
# viewport, not a fixed number. Getting this wrong made every image soft.
#
#   content   = 100vw - 2*36            = 100vw - 72px
#   span-1    = (content - 3*36) / 4    = (100vw - 180px) / 4
#   span-2    = span-1 * 2 + 36         = (100vw - 180px) / 2 + 36px
#   span-4    = content                 = 100vw - 72px
#   index col = (content - 36) / 2      = (100vw - 108px) / 2
GRID_SIZES = "(max-width: 767px) 100vw, calc((100vw - 108px) / 2)"
# Portrait tiles cap at 415px (css .grid-item.is-portrait img); a few carry a
# per-tile cap in the stylesheet, mirrored here so the srcset hint matches.
PORTRAIT_TILE_PX = {"verizon/i001": 312, "verizon/drop12": 374, "isaac-howell/drop10": 913}
def portrait_sizes(key):
    return f"(max-width: 767px) 62vw, {PORTRAIT_TILE_PX.get(key, 415)}px"
# Twelve columns with a 36px gutter: a cell of n columns measures
#   n/12 of (100vw - 72px - 11*36) plus (n-1) gutters.
PAGE_SPAN_SIZES = {
    3:  "(max-width: 767px) 45vw, calc((100vw - 468px) / 4 + 72px)",
    4:  "(max-width: 767px) 45vw, calc((100vw - 468px) / 3 + 108px)",
    6:  "(max-width: 767px) 92vw, calc((100vw - 468px) / 2 + 180px)",
    12: "(max-width: 1279px) 100vw, calc(100vw - 72px)",
}
# An overview cover is set to a fixed height with its width left free, so the
# rendered width depends on its proportion. 500px covers the usual landscape
# cover at --ov-h; a narrow one simply loads a little more than it needs.
# An overview cover is set to a fixed height with its width left free, so the
# width it renders at is that height times its own proportion. A flat figure
# here under-declares a wide cover and the browser fetches a rendition too
# small for it, which is what made the landscape covers soft.
OV_H = {"desktop": 456, "tablet": 336, "phone": 252}
# Cards whose frame the stylesheet makes taller from 768px up
# (css .ov-card[href$=...] .ov-frame): the hint has to match, or the browser
# sizes the image to the shorter frame and the taller one stays empty.
OV_FRAME_SCALE = {"isaac-howell": 1.3}
ROW_H = 620          # matches --row-h: the common height a row of pieces takes


def ov_sizes(item, slug):
    r = item["w"] / item["h"]
    k = OV_FRAME_SCALE.get(slug, 1)
    return (f'(max-width: 599px) {round(OV_H["phone"] * r)}px, '
            f'(max-width: 1023px) {round(OV_H["tablet"] * r * k)}px, '
            f'{round(OV_H["desktop"] * r * k)}px')


# ---------------------------------------------------------------- index
tiles = []
for proj in PROJECTS:
    slug, title = proj["slug"], proj["title"]
    for item in MANIFEST[slug]:
        if item["stem"] in (proj.get("page_only") or ()):
            continue
        alt = f"{title}, {item['caption']}"
        port = is_portrait(item)
        wide = item["w"] > 4 * item["h"]
        cls = "grid-item is-portrait" if port else ("grid-item is-wide" if wide else "grid-item")
        sizes = portrait_sizes(f"{slug}/{item['stem']}") if port else GRID_SIZES
        tiles.append(
            f'<a class="{cls}" href="projects/{slug}.html" '
            f'data-tile="{slug}/{item["stem"]}" '
            f'data-tags="{",".join(item["tags"])}">\n'
            f'  {picture(slug, item, alt, 0, sizes)}\n'
            f'  <span class="caption">{esc(alt)}</span>\n'
            f'</a>')

def badge(label):
    """Sentence case, but UX keeps its capitals."""
    if label.startswith("ux"):
        return "UX" + label[2:]
    return label[0].upper() + label[1:]


filters = "\n".join(
    f'<button type="button" class="filter{" is-active" if k == "all" else ""}" '
    f'data-filter="{k}" aria-pressed="{"true" if k == "all" else "false"}">{badge(label)}</button>'
    for k, label in data.FILTERS)

# One cover per project, gathered under its group — a way in before the
# 200-odd tiles below, which are a lot to land on cold.
groups = []
for key, label in data.GROUPS:
    members = [p for p in PROJECTS if p.get("group") == key]
    if not members:
        continue
    cards = []
    for p in members:
        # The first row of the first group is the page's largest paint; do not
        # defer it behind the lazy-load observer.
        eager = key == data.GROUPS[0][0] and len(cards) < 3
        by_stem = {it["stem"]: it for it in MANIFEST[p["slug"]]}
        cover = by_stem.get(p.get("cover"), MANIFEST[p["slug"]][0])
        # Every discipline the project's pieces are tagged with, in the order
        # the filter bar lists them so two cards never disagree on sequence.
        got = {t for it in MANIFEST[p["slug"]] for t in it["tags"]}
        keys = [k for k, _ in data.FILTERS if k != "all" and k in got]
        chips = "".join(
            f'<span class="ov-tag">{badge(dict(data.FILTERS)[k])}</span>'
            for k in keys)
        cards.append(
            f'    <a class="ov-card" href="projects/{p["slug"]}.html" '
            f'data-tags="{",".join(keys)}">\n'
            f'      <span class="ov-frame">'
            f'{picture(p["slug"], cover, p["title"], 0, ov_sizes(cover, p["slug"]), eager)}</span>\n'
            f'      <span class="ov-name">{p["title"]}</span>\n'
            f'      <span class="ov-short">{p["short"]}</span>\n'
            f'      <span class="ov-tags">{chips}</span>\n'
            f'    </a>')
    groups.append(
        f'  <section class="ov-group">\n'
        f'    <h2 class="ov-h">{label}</h2>\n'
        f'    <div class="ov-grid">\n{chr(10).join(cards)}\n    </div>\n'
        f'  </section>')

# An index of the same work: name, disciplines, year. It carries the same
# data-tags as the cards, so one filter drives both views.
rows = []
for p in PROJECTS:
    got = {t for it in MANIFEST[p["slug"]] for t in it["tags"]}
    keys = [k for k, _ in data.FILTERS if k != "all" and k in got]
    labels = ", ".join(dict(data.FILTERS)[k] for k in keys)
    rows.append(
        f'  <a class="idx-row" href="projects/{p["slug"]}.html" '
        f'data-tags="{",".join(keys)}">\n'
        f'    <span class="idx-name">{p["title"]}</span>\n'
        f'    <span class="idx-work">{labels}</span>\n'
        f'    <span class="idx-year">{p.get("year", "")}</span>\n'
        f'  </a>')
index_rows = "\n".join(rows)

index = head(f"{data.NAME}, Work", 0, data.INTRO) + nav(0) + f"""<main id="main">
<p class="intro">{no_orphan(data.INTRO)}</p>
<p class="intro-note">{no_orphan(data.INTRO_NOTE)}</p>

<div class="filter-bar">
<span class="filter-label" id="filter-label">Show me:</span>
<div class="filter-row">
<div class="filters" role="group" aria-labelledby="filter-label">
{filters}
</div>
<div class="views" role="group" aria-label="How to show the work">
<button type="button" class="view is-on" data-view="grid" aria-pressed="true">Gallery</button>
<button type="button" class="view" data-view="index" aria-pressed="false">Index</button>
</div>
</div>
</div>

<section class="index-view" hidden aria-label="Index of work">
<div class="idx-head">
  <span class="idx-name">Project</span>
  <span class="idx-work">Work</span>
  <span class="idx-year">Year</span>
</div>
{index_rows}
</section>

<div class="overview">
{chr(10).join(groups)}
</div>

<h2 class="all-h" id="all">Everything</h2>
<div class="grid">
{chr(10).join(tiles)}
</div>
<p class="empty" hidden>Nothing in this discipline yet.</p>
</main>
""" + footer(0)

open(os.path.join(ROOT, "index.html"), "w").write(index)

# ---------------------------------------------------------------- about
bio = "\n".join(f"    <p>{no_orphan(p)}</p>" for p in data.ABOUT)
clients = "\n".join(f"      <li>{c}</li>" for c in data.CLIENTS)
teaching = "\n".join(
    f"      <li>{where}<span class=\"about-note\">{no_orphan(what)}</span></li>"
    for where, what in data.TEACHING)
education = "\n".join(
    f"      <li>{where}<span class=\"about-note\">{no_orphan(what)}</span></li>"
    for where, what in data.EDUCATION)

about = head(f"About, {data.NAME}", 0, data.ABOUT[0]) + nav(0, "about") + f"""<main id="main">
<article class="about">
  <h1 class="about-role">{data.ROLE}, {data.LOCATION}</h1>
  <div class="about-bio">
{bio}
  </div>
  <div class="about-cols">
    <section class="about-col">
      <h2 class="about-h">Selected clients and studios</h2>
      <ul class="about-list">
{clients}
      </ul>
    </section>
    <section class="about-col">
      <h2 class="about-h">Teaching</h2>
      <ul class="about-list">
{teaching}
      </ul>
    </section>
    <section class="about-col">
      <h2 class="about-h">Education</h2>
      <ul class="about-list">
{education}
      </ul>
    </section>
    <section class="about-col">
      <h2 class="about-h">Contact</h2>
      <ul class="about-list">
        <li><a href="mailto:{data.EMAIL}">{data.EMAIL}</a></li>
        <li><a href="tel:+1{data.PHONE.replace(' ', '')}">+1 {data.PHONE}</a></li>
        <li><a href="{data.LINKEDIN}" rel="me noopener">LinkedIn</a></li>
      </ul>
    </section>
  </div>
</article>
</main>
""" + footer(0)
open(os.path.join(ROOT, "about.html"), "w").write(about)

def span_of(item):
    """How many of the project grid's four columns a piece should occupy.

    A tall photograph stacked full-width towers over the page; four of them in
    a row read as a set. Wide work still runs the full measure.
    """
    ratio = item["w"] / item["h"]
    if item.get("video"):
        return 6                      # a small player is unusable
    if ratio < 0.6:
        return 3                      # a phone screenshot, four to a row
    if ratio < 0.95:
        return 4                      # a poster or a printed sheet, three up
    if ratio < 2.5:
        return 6                      # the ordinary case, two to a row
    return 12                         # panoramic only: a browser strip, a
                                      # brochure opened flat


def figure(slug, item, eager=False, widths=None, show_caption=True, label=None):
    """One piece on a project page — a picture, or a player if it is a clip."""
    port = is_portrait(item)
    span = item.get("span") or (12 if item.get("frac") else span_of(item))
    if span not in PAGE_SPAN_SIZES:
        # A manifest written before the grid changed carries a span in the old
        # units. Fall back to the proportion rather than guessing a conversion.
        span = span_of(item)
    cls = f"work-figure span-{span}" + (" is-portrait" if port else "")
    if item.get("frac"):
        cls += " is-frac"
    if item.get("bleed"):
        cls += " is-bleed"
    # A deck slide is a 16:9 page of a presentation. It carries dense type and
    # is unreadable at half measure, so it runs the full width of the page.
    ratio = item["w"] / item["h"]
    # An explicit width wins over every rule below: the piece runs alone on its
    # line at that share of the measure, centred.
    pct = (widths or {}).get(item["stem"])
    if pct:
        cls += " is-set"
        # Centring is for a piece that really does run alone. Three 30% pieces
        # share a line, and the auto margins that centre a lone piece would
        # each swallow the leftover measure instead, so the gaps between them
        # come out unequal. Only a piece too wide to have company is centred.
        if pct > 50:
            cls += " is-alone"
    elif "web" in item.get("tags", []) and ratio >= 1.2:
        cls += " is-site"
    elif 1.62 <= ratio <= 2.6 and "is-bleed" not in cls:
        # A page of a presentation, whichever deck it came from. The Retail SEM
        # pages arrive through the drop folder rather than a source letter, so
        # matching on the proportion catches those too. A piece asked to bleed
        # is not one of these: is-deck pins it to half the measure and the
        # bleed never happens.
        cls += " is-deck"
    tags = " ".join(item.get("tags", []))
    if item.get("video"):
        poster = f'../assets/{slug}/{item["stem"]}-{item["widths"][-1]}.webp'
        # Short loops start on their own, muted and inline. A long piece gets
        # a poster and preload=none instead, so its megabytes only move when
        # someone actually presses play.
        auto = ' autoplay loop' if item.get("autoplay") else ''
        media = (f'<video class="work-video" src="../assets/{slug}/{item["video"]}" '
                 f'poster="{poster}" width="{item["w"]}" height="{item["h"]}" '
                 f'muted playsinline controls preload="none"{auto} '
                 f'aria-label="{esc(item["caption"])}"></video>')
    else:
        # The sizes must describe the treatment, not the span. is-site and
        # is-deck override the width in CSS, so taking the span's figure here
        # declared 586px for a piece rendering at 1208 and the browser fetched
        # a 1200px file for a 2416px slot. That was the blur.
        if pct:
            sizes = f"(max-width: 767px) 92vw, calc((100vw - 72px) * {pct / 100})"
        elif "is-bleed" in cls:
            sizes = "100vw"
        elif "is-site" in cls or "is-deck" in cls:
            sizes = "(max-width: 767px) 100vw, calc((100vw - 108px) / 2)"
        else:
            # A row piece is sized by height, so its width is the row height
            # times its own proportion. The span figure describes a grid that
            # no longer lays these out.
            sizes = (f"(max-width: 767px) 92vw, {round(ROW_H * ratio)}px")
        if item.get("frac"):
            # style="width:70%" on the image: it occupies that share of the span.
            sizes = sizes.replace("calc(", f"calc({item['frac']} / 100 * (").replace(")", "))", 1) \
                if "calc(" in sizes else sizes
        media = picture(slug, item, item["caption"], 1, sizes, eager)
        if item.get("frac"):
            media = media.replace('<img ', f'<img style="width:{item["frac"]}%" ', 1)
    style = f' style="width:{pct}%"' if pct else ''
    # A slide that split into several crops (see ALT_SUFFIX) is one piece, not
    # several — the caption names it once, on the first crop, instead of
    # repeating the same line under every half.
    caption = (f'\n  <figcaption class="caption">{esc(label or item["caption"])}</figcaption>'
               if show_caption else '')
    return (f'<figure class="{cls}"{style} data-piece="{slug}/{item["stem"]}" '
            f'data-tags="{tags}">\n  {media}{caption}\n'
            f'</figure>')


def specimen(proj, desc, pager):
    """A type specimen page: the typeface shown live rather than as pictures.

    A grid of screenshots cannot show a typeface — you have to be able to set
    your own word in it — so this page loads the font and renders real text.
    """
    f = proj["font"]
    caps = "\n".join(f'      <span class="spec-cap">{c}</span>' for c in f.get("caps", ""))
    # Capitals and figures only. There is no lowercase in these faces — typing
    # any would silently fall through to the face they were cut from.
    rows = f.get("rows", ["ABCDEFGHIJKLM", "NOPQRSTUVWXYZ",
                          "0123456789", "&amp;?!@#$%*() .,;:"])
    redrawn = (f'<dt>Redrawn</dt><dd>{len(f["caps"])} capitals</dd>\n      '
               if f.get("caps") else "")
    caps_block = (f"""  <section class="spec-block">
    <h2 class="about-h">The {len(f["caps"])} redrawn capitals</h2>
    <div class="spec-caps">
{caps}
    </div>
  </section>
""" if f.get("caps") else "")
    charset = "\n".join(f'      <div class="spec-row">{r}</div>' for r in rows)
    ladder = "\n".join(
        f'      <p class="spec-line" style="font-size:{sz}px">{f["ladder"]}</p>'
        for sz in (96, 64, 44, 30, 21))

    return f"""<article class="project specimen" style="--spec-face:'{f["family"]}'">
  <h1 class="spec-name">{proj["title"].upper()}</h1>
  <div class="spec-head">
    <div class="project-desc">
{desc}
    </div>
    <dl class="spec-facts">
      <dt>Set</dt><dd>{f.get("set", "Capitals and figures")}</dd>
      <dt>Styles</dt><dd>1, Regular</dd>
      <dt>Glyphs</dt><dd>{f["glyphs"]}</dd>
      <dt>Characters</dt><dd>{f["chars"]}</dd>
      {redrawn}<dt>Year</dt><dd>{f["year"]}</dd>
      <dt>Status</dt><dd>Unreleased</dd>
    </dl>
  </div>

  <section class="spec-block">
    <div class="spec-bar">
      <h2 class="about-h">Type it yourself</h2>
      <label class="spec-slider">Size
        <input type="range" id="spec-size" min="28" max="200" value="110"
               aria-label="Specimen size in pixels">
        <output for="spec-size" id="spec-size-out">110px</output>
      </label>
    </div>
    <div class="spec-stage" id="spec-stage" contenteditable="true"
         spellcheck="false" role="textbox" aria-multiline="true"
         aria-label="Editable specimen">{f.get("sample", "MOMA QUARTZ PARIS")}</div>
  </section>

{caps_block}
  <section class="spec-block">
    <h2 class="about-h">Character set</h2>
    <div class="spec-charset">
{charset}
    </div>
  </section>

  <section class="spec-block">
    <h2 class="about-h">Settings</h2>
    <div class="spec-ladder">
{ladder}
    </div>
  </section>

  <p class="project-meta">{proj["meta"]}</p>
{pager}
</article>"""


# -------------------------------------------------------------- contact
contact = head(f"Contact, {data.NAME}", 0,
               f"Get in touch with {data.NAME} at {data.EMAIL}") + nav(0, "contact") + f"""<main id="main">
<article class="about contact">
  <h1 class="project-title">Contact</h1>
  <div class="about-bio">
    <p>Open to senior product, interactive and brand work. I take a full time
       role, a contract, or a single project with a clear brief. I am based
       between New York and Madrid and I work across time zones.</p>
  </div>
  <div class="about-cols">
    <section class="about-col">
      <h2 class="about-h">Email</h2>
      <ul class="about-list">
        <li><a href="mailto:{data.EMAIL}">{data.EMAIL}</a></li>
      </ul>
    </section>
    <section class="about-col">
      <h2 class="about-h">Phone</h2>
      <ul class="about-list">
        <li><a href="tel:+1{data.PHONE.replace(' ', '')}">+1 {data.PHONE}</a></li>
      </ul>
    </section>
    <section class="about-col">
      <h2 class="about-h">Elsewhere</h2>
      <ul class="about-list">
        <li><a href="{data.LINKEDIN}" rel="me noopener">LinkedIn</a></li>
      </ul>
    </section>
    <section class="about-col">
      <h2 class="about-h">Based</h2>
      <ul class="about-list"><li>{data.LOCATION}</li></ul>
    </section>
  </div>
</article>
</main>
""" + footer(0)
open(os.path.join(ROOT, "contact.html"), "w").write(contact)

# ------------------------------------------------------------- projects
os.makedirs(os.path.join(ROOT, "projects"), exist_ok=True)
for i, proj in enumerate(PROJECTS):
    slug = proj["slug"]
    prev_p = PROJECTS[i - 1]
    next_p = PROJECTS[(i + 1) % len(PROJECTS)]

    items = [i for i in MANIFEST[slug] if i["stem"] not in (proj.get("index_only") or ())]
    # A slide that split into several crops shares one caption across all of
    # them (see ALT_SUFFIX, grouped the same way, by caption within the
    # project) — show it once, on the first crop, not once per crop.
    seen_captions = set()
    figures = []
    # A run of pieces from one series names the series once. "Brand book,
    # colour" after "Brand book, typography" shows as "Colour": the leading
    # segment is stated on the first of the run and dropped on the rest. The
    # alt text keeps the full caption.
    prev_series = None
    for item in items:
        cap = item["caption"]
        series, sep, rest = cap.partition(", ")
        label = rest[0].upper() + rest[1:] if sep and series == prev_series else None
        prev_series = series if sep else None
        # A project can opt out of captions entirely: the pictures are the
        # point and a line naming what is visible under each one adds nothing.
        figures.append(figure(slug, item, len(figures) < 4, proj.get("piece_width"),
                               show_caption=proj.get("captions", True)
                               and cap not in seen_captions, label=label))
        seen_captions.add(cap)
    figures = "\n".join(figures)

    desc = "\n".join(f"<p>{no_orphan(d)}</p>" for d in proj["desc"])
    plain = (proj["desc"][0] if proj["desc"] else proj["short"]).replace("<em>", "").replace("</em>", "")

    pager = f"""  <nav class="pager" aria-label="More projects">
    <a href="{prev_p["slug"]}.html"><span class="arrow">←</span>{prev_p["title"]}</a>
    <a href="{next_p["slug"]}.html"><span class="arrow">→</span>{next_p["title"]}</a>
  </nav>"""

    if proj.get("kind") == "specimen":
        body = specimen(proj, desc, pager)
    else:
        body = f"""<article class="project">
  <h1 class="project-title">{proj["title"]}</h1>
  <div class="project-desc">
{desc}
  </div>
  <p class="project-meta">{proj["meta"]}</p>
  <div class="project-images{" is-row" if proj.get("layout") == "row" else ""}">
{figures}
  </div>
{pager}
</article>"""

    page = head(f'{proj["title"]}, {data.NAME}', 1, plain) + nav(1) + f"""<main id="main">
{body}
</main>
""" + footer(1)
    open(os.path.join(ROOT, "projects", slug + ".html"), "w").write(page)

n = sum(len(MANIFEST[p["slug"]]) for p in PROJECTS)
print(f"built index.html ({n} images) + {len(PROJECTS)} project pages")
if SKIPPED:
    print("waiting on source images:", ", ".join(SKIPPED))
