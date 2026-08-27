# Portfolio site — project constraints

Static site, no framework. `data.py` holds the content, `extract.py` cuts the
imagery, `build.py` writes the HTML. Rebuild with:

    python3 extract.py && python3 build.py

## Type
- **PP Telegraf Light (300) only.** One weight across the whole site. Medium
  and Regular are not declared at all: leaving them declared once let a blanket
  edit register Medium as 300, where it won and the site rendered Medium.
- No bold and no italic. `strong` and `b` inherit their weight, `em`, `i` and
  `cite` are upright. Emphasis comes from wording.
- Font sizes are **literal px in the markup** — never tokens or variables for
  size, weight or tracking.
- Four sizes across the site: **16, 18, 24, 36**. Two labels sit outside it and
  are meant to: the tag badges, and the type specimen, which exists to show
  the face at many sizes.
- Letter-spacing is **0.01em** everywhere, except the role line on the about
  page, set at 1pt as a standfirst.
- Line height is **1.2** everywhere, except the tag badge, which is one line
  and sits at 1 so the pill is not inflated by leading.
- On a phone every size collapses to **16px**, badges to 14px. The four-size
  scale is a desktop measure.
- No orphans. `text-wrap: pretty` asks; a non-breaking space between the last
  two words, added at build time, settles it.
- Dada is capitals and figures only and has one weight; the specimen page
  uppercases whatever is typed so it never falls back to Helvetica lowercase.

## Colour
- `--bg` #e3e2dd, `--fg` #000
- `--muted` #236237, a green, for all secondary text. Not grey.
- `--rule` #4a3428, a brown, for section headings and their 1px rules.
- `--accent` #0861ca for links and the current page.
- `--chip` #d5d4ce, the ground under a filter pill. Each filter carries its
  own colour; the tag badges are violet #4a3fd6 on green #a6ef9e.
- Every pair must clear WCAG AA. The greens and blues here were darkened from
  what was sampled precisely to reach 4.5:1 at 15px — do not lighten them back
  without re-measuring.
- Spacing, radius and motion stay `var(--…)`.

## Images
- Never upscale a source. DROP_LONG is a ceiling, not a target: enlarging a
  small file invents detail it does not have and makes it soft and heavy at
  once. A small source publishes at its own size.
- **Never pin one dimension and cap the other.** Use max-height and max-width
  together with width:auto and height:auto, or the picture is squashed to fit.
  A piece sized by width must be released from the row-height cap.
- Paste new work into `drop/<project>/`, never `assets/`. `assets/` is
  generated and `extract.py` empties it on every run.
- A filename becomes the caption. Two or more words, em dash as separator. A
  camera or screenshot name falls back to the project title.
- `sizes` must describe the width an image really renders at, and that means
  the **treatment**, not the grid span. A deck slide and a website screenshot
  each take half the measure; a row piece is sized by height, so its width is
  `--row-h` times its own proportion; an overview cover is `--ov-h` times its
  proportion. Declaring the span instead is what has made images soft every
  time it has happened.

## Copy
- **Read `ANTISLOP.md` before writing any word that ships.** Copy is
  assembled from the CV and the decks, not written by the model.
- No dashes in any body text: the intro, the about page, project descriptions.
  The em dash is a separator and belongs only in captions, meta lines and
  titles.
- It is a portfolio, never an "archive".
