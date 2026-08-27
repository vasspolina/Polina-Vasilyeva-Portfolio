# Antislop — the copy prompt for this site

Load this before writing or editing any word that ships on the site: the hero,
the about page, project `meta` and `desc` in `data.py`, captions, tags, alt
text, the contact page, page titles and meta descriptions.

The rule the rest of this file serves: **the words are Polina's, not the
model's.** Copy is assembled from the CV and the decks. Sentences that exist
only because a slot looked empty are the failure this file prevents.

## 1. Sources, in precedence order

| # | Source | Authority |
|---|---|---|
| 1 | `~/Desktop/Vasilyeva, Polina_CV 2026.pdf` | Every fact: titles, employers, dates, locations, scope, numbers, education, teaching. The CV wins over everything. |
| 2 | `~/Downloads/Portfolio_Polina_Vasilyeva_2026.pdf` (81 slides) | What each project *is*: the work shown, its parts, its names. |
| 3 | `~/Downloads/Polina_Vasilyeva_2026_Senior_Digital_Interactive_Designer.pdf` (107 slides) | Same, deeper on AW / Haworth / Verizon and the passion projects. |
| 4 | `source/_decks/haworth-brand-guidelines.pdf`, `SOURCES["C"]`, `SOURCES["D"]` in `data.py` | Project-specific detail. |
| 5 | The imagery in `drop/` | Last resort, and only for what is plainly visible. |

**The deck bio is stale — it says she works for Apple. Never quote it.** Bio
facts come from the CV only.

Existing `desc` blocks in `data.py` are already source-derived and approved.
Treat them as the reference recording of the voice, not as raw material to
rewrite.

## 2. Sourcing, in practice

- Every clause must trace to a source line. Before proposing copy, quote the
  source line it came from and name the file and page.
- Prefer the source's own nouns, verbs and product names, lightly re-cut for
  the page. Paraphrase to fit; do not "improve".
- New connective words are for grammar only: joining two source facts,
  introducing a list. They carry no claim.
- **When the source is silent, write nothing.** A caption plus the image is a
  finished unit. Ask; do not fill.
- When the CV and a deck disagree, the CV wins and you say so in the message,
  not on the page.

## 3. Fixed facts

- Name: **Polina Vasilyeva**. Title: **Senior Interactive, Product, UX &
  Visual Designer**. Based **New York / Madrid**.
- `vasilievapolli@gmail.com` · `+1 203 909 8496`
- **10+ years** — the CV's figure. Not "over a decade", not "15 years".
- Apple ran **Jan 2025–Apr 2026**; PayPal **Apr–Jul 2026**. Both are past.
  **Never name a current employer** and never write "currently at". What is
  present tense: the freelance practice (2017–present) and NYU (2021–present).
- Numbers appear only if the CV states them: 3B+ users, a cross-functional
  team of 5–6, three launched features. No invented metrics, no percentages,
  no "resulting in a 40% lift".

**House spellings** (these win over the CV's own casing): `frog design`,
`clinique iD`, `Google / Fitbit`, `Alexander Wang`, `Apartamento Studios`,
`The Wall Street Journal` on first use and `WSJ` in lists, `Yale School of
Art`, `Gerrit Rietveld Academie`, `The New School`, `Pratt Institute`.

**Never the word "archive"** for this site — it is a portfolio. The one
exception is the Alexander Wang *vault — archive sale*, a real product name.

## 4. Banned vocabulary

Never ship these, in any inflection:

> passionate · driven · seamless · seamlessly · elevate · empower · leverage ·
> robust · cutting-edge · innovative · solutions · crafted · crafting ·
> curated · thoughtful · holistic · impactful · transformative ·
> game-changing · best-in-class · world-class · next-level · unlock ·
> supercharge · resonate · delightful · delight · magic · beautiful ·
> stunning · pixel-perfect · user-centric · human-centered · storytelling ·
> narrative (as a synonym for design) · journey (as a synonym for flow) ·
> ecosystem (unless it is the CV's "partner ecosystems") · deep dive ·
> bridging the gap · at the intersection of · obsessed with · love for ·
> excited to · in today's fast-paced world · ever-evolving landscape

Also banned: any adjective doing the work a noun should do. "A bold,
expressive system" says nothing; "one type system holding every printed asset
together, from rate sheets to window signage" says it.

## 5. Banned constructions

- **The rule of three.** "Research, strategy, and delight." Cut it to what is true.
- **"Not just X, but Y."** And its cousin "It's not about X. It's about Y."
- **The turn.** A short dramatic fragment after a full sentence. "The result?"
- **Rhetorical questions.** Any question mark in body copy is a defect.
- **Second person.** No "imagine", no "you'll notice".
- **First-person feeling.** "I believe", "I'm fascinated by", "I care deeply".
  The about page may use "I" for actions the CV states; never for interiority.
- **Effect-on-the-viewer claims.** "Draws the eye", "creates a sense of
  calm", "invites exploration". Describe what is on the page and the decision
  that produced it.
- **Process theatre.** No "we started by asking", no discovery-to-delivery arc,
  unless the CV or deck records that specific work.
- Exclamation marks. Emoji. ALL-CAPS for emphasis. Bold or italic for
  emphasis — the type has one weight and emphasis comes from wording.
- **Dashes inside project descriptions**, per `CLAUDE.md`. The em dash is a
  separator, and only in captions and `meta` lines.

## 6. Person, tense, credit

- Past tense for finished roles. Present only for 2017–present and
  2021–present.
- Project `desc` is written impersonally — the work, not the worker.
  "Branding, campaign, and packaging design for Alexander Wang bodywear",
  not "I designed…". The about page is the only place "I" appears.
- Credit follows the CV's verb. "Led design of" means led; "Partnering with"
  means partnered. Never promote a contribution into ownership, and never
  demote solo work into "we".
- Collaborators stay named where the source names them: with Apartamento
  Studios, with frog design, through HUGE.

## 7. Shape, by slot

| Slot | Length | Notes |
|---|---|---|
| `INTRO` | one sentence | Names only clients the grid actually shows. |
| `INTRO_NOTE` | one sentence | Where the unshown recent work is described. |
| About | 4 paragraphs, 2–4 sentences | Now, then earlier, then education and teaching. |
| `meta` | one line | `Client — Role, Years — Disciplines`, em dashes. |
| `desc` | 1–3 blocks, 2–4 sentences each | Concrete nouns; see `verizon`, `haworth`, `clinique` in `data.py`. |
| Caption | 2+ words, em dash separator | Comes from the filename. |
| `short` / tags | 2–4 words | Discipline, lowercase. |
| Alt text | one clause | What is depicted. Never "image of". |

## 8. Two tests, applied to every sentence

1. **The substitution test.** Could this sentence sit on any other designer's
   site with the client name swapped? Then it is slop. Replace it with a
   specific noun from the source: *speech states*, *rate sheets*, *clearspace
   and minimum size*, *the offer card*, *Express Pickup Lockers*, *mylar and
   magnetic boxes*, *Escrow on the WSJ green*.
2. **The deletion test.** Delete the sentence. If nothing factual is lost, it
   was decoration. Leave it deleted.

## 9. Calibration

Slop, and what the site actually says:

> ✗ A bold new brand vision that seamlessly unifies digital and retail
> touchpoints, elevating the customer journey.
> ✓ Research, then a single set of design standards unified across digital,
> retail, and UX.

> ✗ Thoughtfully crafted packaging that tells the story of the brand.
> ✓ A packaging system that borrows the visual language of the grocery aisle
> in cartons, mylar, and magnetic boxes, all recyclable.

> ✗ I'm a passionate designer who loves solving complex problems at the
> intersection of brand and product.
> ✓ Ten years across accessible and friendly visual and interactive design,
> digital strategy, art direction, and concept development — helping companies
> and individuals focus and build on their advantage.

The third is the CV's own line, moved onto the page. That is the method.

## 10. Before showing any copy

Run this and report it:

- [ ] Every clause traces to CV, deck, or visible image — sources named.
- [ ] No banned word, no banned construction, no dash inside a `desc`.
- [ ] No current employer asserted; every date matches the CV.
- [ ] Every number appears in the CV.
- [ ] Names spelled the house way; the word "archive" absent.
- [ ] Substitution test and deletion test passed, sentence by sentence.
- [ ] Nothing invented to fill a slot; gaps raised as questions instead.

Show the diff and the source trace. Do not rebuild until the copy is approved.
