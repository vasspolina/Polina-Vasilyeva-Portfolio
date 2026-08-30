"""Portfolio content. Edit this file, then run:  python3 extract.py && python3 build.py

SOURCES     — the decks the imagery is cut from.
PROJECTS    — ordered. Each page entry is (source, page_number, caption, [tags]).
              extract.py cuts each deck page into its individual artworks, so one
              page entry can produce several images on the site.
"""

NAME = "Polina Vasilyeva"
ROLE = "Senior Interactive, Product, UX &amp; Visual Designer"
EMAIL = "vasilievapolli@gmail.com"
PHONE = "203 909 8496"
LOCATION = "New York / Madrid"
LINKEDIN = "https://www.linkedin.com/in/polina-vasilyeva-265aa031/"

ABOUT = [
    "I’m a senior interactive, product, UX and visual designer working "
    "between New York and Madrid. Ten years across accessible and friendly "
    "visual and interactive design, digital strategy, art direction, and "
    "concept development, helping companies and individuals focus and build "
    "on their advantage.",
    "Most recently I designed product experiences for PayPal’s loyalty "
    "program, adapting rewards mechanics and partner offers to the UK and "
    "German markets. Before that, at Apple, I led design on an AI-powered "
    "shopping assistant for the global storefront, redesigned the AppleCare "
    "support and coverage-selection flows, and built a personalized "
    "carrier-offer experience, embedding WCAG standards into every stage "
    "from concept through QA.",
    "Earlier: product design and design-system work at Optum, Fitbit "
    "features with Google through HUGE, component libraries and product "
    "strategy for McKinsey, brand standards for Verizon across digital and "
    "retail, campaigns and packaging as Senior Designer and Art Director at "
    "Alexander Wang, UX and visual design for Florida Blue with frog "
    "design, and a re-brand strategy for Showtime at Wolff Olins.",
    "I hold an MFA from Yale School of Art and a BFA from Gerrit Rietveld "
    "Academie, and I teach, currently as a visiting critic at NYU, "
    "previously adjunct professor at Pratt Institute and The New School, "
    "and visiting critic at RISD.",
]

CLIENTS = ["PayPal", "Apple", "Optum", "Google / Fitbit", "McKinsey", "Verizon",
           "Alexander Wang", "WSJ", "Haworth", "Apartamento Studios",
           "frog design",
           "Florida Blue", "Wolff Olins", "HUGE", "Chobani", "Furniture.com",
           "Tomo", "Pratt Institute"]

TEACHING = [
    ("NYU", "Visiting Critic, 2021–present"),
    ("Pratt Institute", "Adjunct Professor, 2017–2020"),
    ("The New School", "Adjunct Professor, 2017–2018"),
    ("RISD", "Visiting Critic, 2017–2021"),
]

EDUCATION = [
    ("Yale School of Art", "MFA, Graphic and Digital Product Design, 2015–2017"),
    ("Gerrit Rietveld Academie", "BFA, Graphic and Interaction Design, 2010–2015"),
]

INTRO = ("Selected work in product, web, brand, and editorial design for "
         "Verizon, Haworth, Alexander Wang, Chobani, and Florida Blue.")

# The recent product work is not shown here; say so rather than let the hero
# promise names the grid does not contain.
INTRO_NOTE = ("Recent product design for PayPal, Apple, Optum, and Google is "
              "described on the <a href=\"about.html\">about page</a>.")

SOURCES = {
    "A": "/Users/polinavasilyeva/Downloads/Portfolio_Polina_Vasilyeva_2026.pdf",
    "B": "/Users/polinavasilyeva/Downloads/"
         "Polina_Vasilyeva_2026_Senior_Digital_Interactive_Designer.pdf",
    "C": "/Users/polinavasilyeva/Desktop/Verizon portfolio .pdf",
    "D": "/Users/polinavasilyeva/Desktop/Polina_Vasilyeva_2023_Watson_portfolio.pdf",
    "E": "source/_decks/haworth-brand-guidelines.pdf",
    "F": "source/_decks/furniture-final-design.pdf",
    "G": "source/_decks/furniture-color-typography.pdf",
    "H": "source/_decks/furniture-final-design-full.pdf",
}

FILTERS = [
    ("all", "all"),
    ("web", "web"),
    ("mobile", "mobile"),
    ("ecommerce", "e-commerce"),
    ("brand", "brand"),
    ("product", "ux &amp; product"),
    ("editorial", "editorial"),
    ("strategy", "strategy"),
    ("social", "social"),
]

# The overview section at the top of the index, one image per project.
GROUPS = [
    ("brand",   "Brand &amp; campaign"),
    ("product", "Product &amp; web"),
    ("book",    "Books &amp; print"),
    ("type",    "Type"),
]

PROJECTS = [
 {
  "slug": "verizon", "title": "Verizon",
  "year": "2022–2023",
  # The signage slices come off pages of different heights; one width
  # sets them level, two to a row.
  "piece_width": {"c003-1": 48, "c003-2": 48, "c004-1": 48, "c004-2": 48},
  "drops_first": True,
  "cover": "p01",
  "group": "brand", "short": "Web, retail &amp; brand design",
  "meta": "Verizon — Senior Design Consultant, 2022–2023 — Web, Retail &amp; Brand Design",
  "desc": ["Research, then a single set of design standards unified "
           "across digital, retail, and UX. Within Brand 3.0: the 5G "
           "homepage, the chat and voice assistant with its full set of "
           "speech states, and the application of NHG Thin, Vivid Red, "
           "and soft grays across screens in-store and online.",
            "Brand design for national retail: one type system holding "
           "every printed asset together, from rate sheets and plan "
           "comparisons to price cards and window and header signage, so "
           "a Prepaid sheet, an Unlimited plan grid and an <em>Ultra</em> "
           "header all read as the same voice at any size. The system "
           "carries into the stores as three tiers of wayfinding, the "
           "Home and Business walls, Express Pickup Lockers, and "
           "packaging. Every asset was reviewed against accessibility "
           "best practice.",
            "Streamlining the standards raised designer productivity, "
           "shortened turnaround on retail projects, and improved print "
           "quality.",
            "Built components for Verizon's own design library, and ran "
           "audits and workshops to improve the system from within, "
           "managing several projects at once across retail and digital."],
  "pages": [
    # The deck's own title slide carries the wordmark on the slide ground, and
    # the Retail SEM title exists only at 1020px — too small to be a cover.
    # The Retail SEM working deck, published whole: the system, the
    # wayfinding tiers, and the store as it was built and as it will be.
    ("IMG", "verizon-sem/p01.jpg", "Retail SEM — the working deck", ["brand"], {"crop": False, "split": False}),
    ("A", 26, "Verizon.com homepage — connecting you with what matters", ["web"], {"dechrome": True}),
    ("A", 28, "Chat assistant on mobile", ["web", "mobile"], {"crop": False}),
    ("A", 27, "Voice assistant states — idle, waiting, listening, thinking, done, error", ["web", "product"]),
    ("A", 29, "NHG Thin in application — in-store and online", ["brand", "web"]),
    ("A", 30, "Vivid Red — digital color use", ["brand"]),
    ("A", 31, "Gray as a subtle accent on-screen", ["brand", "web"]),
    ("B", 85, "Express Pickup Lockers — retail brand design", ["brand"]),
    ("C", 2,  "Printed assets for national retail — one type system across every format",
              ["brand"], {"rows": True, "keep": [1, 2]}),
    ("C", 3,  ["Ultra signage — the counter unit",
               "Nuestros mejores planes — the wall"], ["brand"],
              {"slices": [(0.024, 0.404), (0.404, 0.914)]}),
    ("C", 4,  ["Our best plan ever — the light box",
               "The Ultra table"], ["brand"],
              {"slices": [(0.024, 0.331), (0.404, 0.914)]}),
    ("C", 20, ["The store, looking in", "Product table merchandising",
               "The storefront"], ["brand"], {"rows": True, "keep": [3]}),
    ("A", 32, "Executing growth across five vectors — strategy deck", ["strategy"]),
    ("IMG", "verizon-sem/p02.jpg", "Agenda — the retail design system and the reset", ["brand", "strategy"], {"crop": False, "split": False}),
    ("IMG", "verizon-sem/p04.jpg", "Optimizing the retail design system", ["strategy"], {"crop": False, "split": False}),
    ("IMG", "verizon-sem/p05.jpg", "Towards a responsive retail environment", ["strategy"], {"crop": False, "split": False}),
    ("IMG", "verizon-sem/p07.jpg", "What is happening, when — the roadmap", ["strategy"], {"crop": False, "split": False}),
    ("IMG", "verizon-sem/p09.jpg", "Entry", ["brand"], {"crop": False, "split": False}),
    ("IMG", "verizon-sem/p10.jpg", "The floor, looking in", ["brand"], {"crop": False, "split": False}),
    ("IMG", "verizon-sem/p11.jpg", "The floor, with the wall behind it", ["brand"], {"crop": False, "split": False}),
    ("IMG", "verizon-sem/p12.jpg", "Wayfinding", ["brand"], {"crop": False, "split": False}),
    ("IMG", "verizon-sem/p13.jpg", "Three tiers of wayfinding in the store", ["brand"], {"crop": False, "split": False}),
    ("IMG", "verizon-sem/p14.jpg", "Back Wall", ["brand"], {"crop": False, "split": False}),
    ("IMG", "verizon-sem/p17.jpg", "Business", ["brand"], {"crop": False, "split": False}),
    ("IMG", "verizon-sem/p18.jpg", "The Business bay and its aisle fixture", ["brand"], {"crop": False, "split": False}),
    ("IMG", "verizon-sem/p19.jpg", "Live Try", ["brand"], {"crop": False, "split": False}),
    ("IMG", "verizon-sem/p20.jpg", "Live Try — the wall without the gradient", ["brand"], {"crop": False, "split": False}),
    ("IMG", "verizon-sem/p23.jpg", "Aisle Fixtures", ["brand"], {"crop": False, "split": False}),
    ("IMG", "verizon-sem/p24.jpg", "Aisle fixtures — the frame and the paper-white stage", ["brand"], {"crop": False, "split": False}),
    ("IMG", "verizon-sem/p25.jpg", "Aisle headers, by category", ["brand", "editorial"], {"crop": False, "split": False}),
    ("IMG", "verizon-sem/p27.jpg", "Future state — the grey back wall today", ["brand"], {"crop": False, "split": False}),
    ("IMG", "verizon-sem/p28.jpg", "Future state — digital carried through", ["brand"], {"crop": False, "split": False}),
    ("IMG", "verizon-sem/p29.jpg", "The Home wall", ["brand"], {"crop": False, "split": False}),
    ("IMG", "verizon-sem/p30.jpg", "The floor from the entry", ["brand"], {"crop": False, "split": False}),
    ("IMG", "verizon-sem/p31.jpg", "Digital replaces print at Live Try", ["brand", "product"], {"crop": False, "split": False}),
    ("IMG", "verizon-sem/p32.jpg", "The collaboration table", ["brand"], {"crop": False, "split": False}),
    ("IMG", "verizon-sem/p33.jpg", "The floor, wide", ["brand"], {"crop": False, "split": False}),
    ("IMG", "verizon-sem/p34.jpg", "Express Pickup Lockers and the Business wall", ["brand"], {"crop": False, "split": False}),
  ],
 },
 {
  "slug": "haworth", "title": "Haworth",
  "year": "2019",
  # The logo slide reads tighter than 16:9: the wordmark sits in a
  # narrower field, so the slide ground is taken in from both sides.
  # The slide carries its own header and footer in small type; the mark
  # alone is the cover, so both bands come off.
  "piece_crop": {"b062": (0.14, 0.0875, 0.14, 0.0875),
                 "collection-lockup": (0.14, 0.0875, 0.14, 0.0875)},
  # The research pages are spreads of type; two to a row keeps them
  # readable without letting one fill the measure alone.
  "piece_width": {"drop05": 48, "drop06": 48, "drop07": 48,
                  "a060": 30, "b064-2": 30, "b065-1": 30, "b065-2": 30},
  "cover": "b062",
  "group": "brand", "short": "Brand, e-commerce &amp; strategy",
  "meta": "Haworth — with Apartamento Studios — Brand, E-commerce &amp; Digital Strategy",
  "desc": ["E-commerce design and digital strategy for the Haworth "
           "platform: the homepage as a central portal for brand stories, "
           "editorial modules built on workplace research, and mobile "
           "storytelling for Social Spaces and Organic Workspace.",
            "With Apartamento Studios: the logo and the brand guidelines "
           "themselves, covering logotype evolution, clearspace and "
           "minimum size, the sub-brand lock-ups for Collection and "
           "Health, Founders Grotesk paired with Plantin MT Pro, the "
           "colour system and its expressive combinations, the modular "
           "layout grid, photography direction, the icon set drawn on one "
           "grid, and the applications from business cards to invitations "
           "and premium products.",
            "Also art direction for the New York headquarters, and print "
           "work from workplace research reports to the Interior Design "
           "Hall of Fame Awards.",
            "The strategy work frames Haworth's shift from furniture "
           "manufacturer to office solutions provider. The brand design "
           "system unites strategy, design, and technology, and extends "
           "into a social media system spanning NeoCon and Orgatec.",
            "The rebrand reaffirmed Haworth's leadership in contract "
           "furnishings: it won new customers, grew the audience by 20%, "
           "and lifted sales by 10%."],
  "pages": [
    ("B", 62, "Haworth — logo design", ["brand"], {"crop": False}),
    ("IMG", "haworth/collection-lockup.png", "Haworth Collection lockup on navy",
     ["brand"], {"crop": False}),
    ("A", 59, "Haworth.com homepage — Inspired Design", ["ecommerce", "web"],
     {"dechrome": True, "span": 6}),
    ("IMG", "haworth/social-five-screens.png",
     "Instagram posts and stories — five screens", ["social"],
     {"crop": False, "split": False, "span": 12}),
    ("A", 60, "Editorial modules — workplace research stories", ["ecommerce", "web"],
     {"dechrome": True, "span": 6}),
    # b063 and the first half of b064 are dropped: one repeats the shoot, the
    # other carries the "Art Direction" divider band across its foot.
    ("B", 64, "New York headquarters — art direction", ["brand"], {"keep": [2]}),
    ("B", 65, "Apartamento Studios — art direction", ["brand"]),
    ("B", 66, "Designing the Workplace for Innovation — print", ["editorial"]),
    # Both pieces repeat what the folder holds: drop04 and drop03.
    ("B", 68, "Interior Design Hall of Fame Awards — print", ["editorial"]),
    ("E", 5, "Brand book — brand strategy", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 6, "Brand book — brand strategy", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 7, "Brand book — brand strategy", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 8, "Brand book — brand strategy", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 9, "Brand book — brand strategy", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 10, "Brand book — brand strategy", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 12, "Brand book — visual identity", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 13, "Brand book — visual identity", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 15, "Brand book — the logotype", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 16, "Brand book — the logotype", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 17, "Brand book — the logotype", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 18, "Brand book — the logotype", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 19, "Brand book — the logotype", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 20, "Brand book — the logotype", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 21, "Brand book — the logotype", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 22, "Brand book — the logotype", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 23, "Brand book — the logotype", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 24, "Brand book — the logotype", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 25, "Brand book — the logotype", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 26, "Brand book — typography", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 27, "Brand book — typography", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 28, "Brand book — colour", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 29, "Brand book — colour", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 30, "Brand book — colour", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 31, "Brand book — colour", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 32, "Brand book — colour", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 33, "Brand book — colour", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 34, "Brand book — colour", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 35, "Brand book — colour", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 36, "Brand book — colour", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 39, "Brand book — the layout system", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 40, "Brand book — the layout system", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 41, "Brand book — the layout system", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 42, "Brand book — the layout system", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 43, "Brand book — the layout system", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 44, "Brand book — the layout system", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 45, "Brand book — the layout system", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 46, "Brand book — the layout system", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 47, "Brand book — the layout system", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 48, "Brand book — the layout system", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 50, "Brand book — art direction", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 51, "Brand book — art direction", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 52, "Brand book — art direction", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 53, "Brand book — art direction", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 54, "Brand book — art direction", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 55, "Brand book — art direction", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 56, "Brand book — art direction", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 57, "Brand book — art direction", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 58, "Brand book — art direction", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 59, "Brand book — art direction", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 60, "Brand book — art direction", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 61, "Brand book — art direction", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 62, "Brand book — art direction", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 63, "Brand book — art direction", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 64, "Brand book — art direction", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 65, "Brand book — art direction", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 66, "Brand book — art direction", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 68, "Brand book — verbal identity", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 69, "Brand book — verbal identity", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 70, "Brand book — verbal identity", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 71, "Brand book — verbal identity", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 72, "Brand book — verbal identity", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 76, "Brand book — corporate materials", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 77, "Brand book — corporate materials", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 78, "Brand book — corporate materials", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 79, "Brand book — corporate materials", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 80, "Brand book — corporate materials", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 81, "Brand book — corporate materials", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 82, "Brand book — corporate materials", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 83, "Brand book — corporate materials", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 84, "Brand book — corporate materials", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 85, "Brand book — corporate materials", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 86, "Brand book — corporate materials", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 87, "Brand book — corporate materials", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 88, "Brand book — corporate materials", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 89, "Brand book — corporate materials", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 90, "Brand book — corporate materials", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 91, "Brand book — document templates", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 92, "Brand book — document templates", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 93, "Brand book — document templates", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 94, "Brand book — document templates", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 95, "Brand book — document templates", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 96, "Brand book — document templates", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 97, "Brand book — document templates", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 98, "Brand book — document templates", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 99, "Brand book — document templates", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 100, "Brand book — document templates", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 101, "Brand book — document templates", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 102, "Brand book — document templates", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 103, "Brand book — document templates", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 104, "Brand book — document templates", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 105, "Brand book — document templates", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 106, "Brand book — print and premium products", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 107, "Brand book — print and premium products", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 108, "Brand book — print and premium products", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 109, "Brand book — print and premium products", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 110, "Brand book — print and premium products", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("E", 112, "Brand book — digital", ["brand", "editorial"],
     {"crop": False, "split": False, "span": 2}),
    ("VID", "haworth-opening-title.mp4", "Opening title", ["brand"],
     {"src": "/Volumes/Expansion/opening_title_2_HAWORTH.mov",
      "start": 0, "duration": 17.4, "width": 1280, "kbps": 1400}),
    ("VID", "haworth-motion.mp4", "Motion graphics", ["brand"],
     {"src": "/Volumes/Expansion/Motion Graphics HAWORTH_6.mov",
      "start": 0, "duration": 69.2, "width": 1280, "kbps": 1100}),
  ],
 },
 {
  "slug": "alexander-wang", "title": "Alexander Wang",
  # The lockup alone: the slide's own caption line sits below it.
  "piece_width": {"b031-1": 30, "b031-2": 30, "b033": 30,
                  "b035-1": 30, "b035-2": 30},
  "piece_crop": {"b003": (0.02, 0.088, 0.10, 0.088)},
  "year": "2021–2022",
  "cover": "b037",
  "group": "brand", "short": "Brand, packaging &amp; art direction",
  "meta": "Alexander Wang — Senior Designer &amp; Art Director, 2021–2022 — Brand, Packaging &amp; E-commerce",
  "desc": ["Branding, campaign, and packaging design for Alexander Wang "
           "bodywear, originated and launched: clothing and care labels, "
           "red and blue stripes nodding to classic Americana, and a "
           "packaging system that borrows the visual language of the "
           "grocery aisle in cartons, mylar, and magnetic boxes, all "
           "recyclable.",
            "The idea carries into retail as display units built to look "
           "like refrigerated cases, and into video installation and art "
           "direction for the flagships in Beijing, Sanya Haitang Bay, "
           "and New York.",
            "Promo campaigns across spring, summer, and autumn in static "
           "and dynamic digital media alongside print: <em>Whenever. "
           "Wherever.</em> shot by Todd Oldham, and the <em>SISTERS</em> "
           "identity with its cast cards and OOH posters. Styling "
           "direction for Julia Fox, drop titles carrying each release "
           "through social and email, and the e-commerce side, where I "
           "designed the vault site for special-offer sales."],
  "pages": [
    ("B", 3,  "bodywear — brand lockup", ["brand"], {"crop": False}),
    ("B", 5,  "The a mark", ["brand"], {"pad": 0.14}),
    ("B", 9,  "Care label — designed and supervised through production", ["brand"]),
    ("B", 13, "Packaging — the Classic Briefs bag", ["brand"], {"split": False}),
    ("B", 14, "Packaging — bag, carton, and box", ["brand"], {"split": False}),
    ("B", 15, "Packaging — red stripe across the range", ["brand"], {"split": False}),
    ("B", 16, "Packaging — range variants", ["brand"], {"split": False}),
    ("B", 17, "Packaging — mylar bags", ["brand"], {"split": False}),
    ("B", 18, "Packaging — clear bags", ["brand"], {"split": False}),
    ("B", 19, "bodywear retail units", ["brand"]),
    ("B", 20, "Art direction for flagship display units", ["brand"]),
    ("B", 21, "Displays built to read as grocery refrigeration units", ["brand"]),
    ("B", 22, "Flagship display units", ["brand"]),
    ("B", 23, "Flagship display units", ["brand"]),
    ("B", 24, "Flagship display units", ["brand"]),
    ("B", 25, "Flagship display units", ["brand"]),
    ("B", 28, "Tiered display units", ["brand"], {"debg": True, "pad": 0.4}),
    ("B", 29, "Whenever. Wherever. — SM and OOH campaign", ["brand", "social"]),
    ("B", 30, "Everyday activities with a cheeky, sensual twist", ["brand", "social"]),
    ("B", 31, "Whenever. Wherever. — shot by Todd Oldham", ["brand"]),
    ("B", 32, "Art direction for SM and OOH", ["brand", "social"]),
    ("B", 33, "3D animation series for social media", ["brand", "social"]),
    ("B", 34, "Intimate wear as outerwear — creative direction", ["brand"]),
    ("B", 35, "Styling direction for Julia Fox", ["brand"]),
    ("B", 36, "Intimate wear as outerwear — creative direction", ["brand"]),
    ("B", 37, "Beijing flagship — façade animation", ["brand"]),
    ("VID", "beijing-gradient.mp4",
     "Beijing flagship — the gradient, running", ["brand"],
     {"src": "/Volumes/Expansion/32bpc 2.mp4",
      "start": 190, "duration": 40, "width": 800, "kbps": 450,
      "autoplay": True}),   # only 1MB, and an installation loop wants to run
    ("B", 38, "Beijing flagship — gradient video installation", ["brand"]),
    ("B", 39, "Beijing flagship — gradient installation in the store", ["brand"]),
    ("B", 40, "Retail — video installation, animation", ["brand"]),
    ("B", 41, "Retail — video installation, animation", ["brand"]),
    ("B", 42, "Retail — video installation, animation", ["brand"]),
    ("B", 43, "Retail — video installation, animation", ["brand"]),
    ("B", 44, "Sanya Haitang Bay — 3D catwalk animation", ["brand"]),
    ("B", 45, "Sanya Haitang Bay — storefront", ["brand"]),
    ("B", 46, "New York flagship — 3D avatar", ["brand"]),
    ("B", 47, "Retail — video installation, animation", ["brand"]),
    ("B", 48, "Autumn drop campaign — art direction", ["brand"]),
    ("B", 49, "Email design, with the marketing team", ["brand", "social"]),
    ("B", 51, "Velour Couture — social and email assets", ["brand", "social"]),
    ("B", 52, "SISTERS — campaign identity", ["brand"]),
    ("B", 53, "SISTERS — campaign identity and social assets", ["brand", "social"]),
    ("IMG", "alexander-wang/sisters-teaser.png",
     "SISTERS — teaser, three faces above the title", ["brand", "social"],
     {"crop": False}),
    ("IMG", "alexander-wang/sisters-bus-shelter.png",
     "SISTERS — bus shelter poster, excellence runs in the family", ["brand"],
     {"crop": False}),
    ("IMG", "alexander-wang/heiress-bag-3d.png",
     "The Heiress bag — 3D animation stills", ["brand", "social"],
     {"crop": False, "split": False}),
    ("B", 60, "vault — archive sale gate", ["ecommerce", "web"], {"dechrome": True}),
    ("B", 61, "vault — archive shopping grid", ["ecommerce", "web"], {"dechrome": True}),
  ],
 },
 {
  "slug": "wsj", "title": "WSJ",
  "year": "2024",
  # Emails and display units at one width, so the set reads as a set
  # rather than as pieces of different importance.
  "piece_width": {**{f"drop{n:02d}": 23 for n in range(1, 15)},
                  "ad-tall": 23},
  "cover": "ad-tall",
  "group": "brand", "short": "Subscription campaign design",
  "meta": "The Wall Street Journal — Subscription Campaign Design",
  "desc": ["Subscription acquisition design for The Wall Street Journal, "
           "across the marketing funnel: display advertising at the top, "
           "email further down, and the offer pages that close. Each stage "
           "asks for one thing, and the ask gets more specific as the reader "
           "moves through.",
           "One campaign set to run at more than one ratio: the masthead, an "
           "editorial image, and the offer hold their relationship as the "
           "frame changes shape.",
           "The email carries the middle of the funnel. Podcast titles are "
           "the subject, one colour to a show, and the price is stated as "
           "the picture rather than beside it: a green four, a red one, a "
           "field of dollar signs. Set in the paper's own Escrow, with the "
           "subscribe action and the price carried in a band at the foot of "
           "every size."],
  "pages": [
    ("IMG", "wsj/ad-tall.png", "Make Art Feuds Your Business — tall unit",
     ["brand"], {"crop": False}),
  ],
 },
 {
  "slug": "clinique", "title": "Clinique",
  "year": "2020",
  "drop_tags": ["ecommerce", "web"],
  # Four grabs kept the whole Chrome window: tab strip, address bar and
  # a personal bookmarks bar. The page begins about 6.8% down.
  "piece_crop": {"drop05": (0.068, 0, 0, 0), "drop06": (0.068, 0, 0, 0),
                 "drop07": (0.068, 0, 0, 0), "drop08": (0.068, 0, 0, 0)},
  "cover": "drop01",
  "group": "product", "short": "E-commerce &amp; campaign design",
  "meta": "Clinique — clinique iD, E-commerce &amp; Campaign Design",
  "desc": ["Campaign and e-commerce design for clinique iD, a hydrator built in "
           "two parts: a base, and a cartridge of concentrate dropped into it. "
           "The product page sells the idea as an equation, base plus cartridge "
           "equals the bottle you end up with.",
           "Each concern gets its own colour and its own texture, green for "
           "irritation, blue for pores and uneven texture, purple for lines and "
           "wrinkles, orange for fatigue, so the range reads at a glance and a "
           "shopper can pick a base and a cartridge without reading a word."],
  "pages": [
    # Everything comes from drop/clinique/.
  ],
 },
 {
  "slug": "chobani", "title": "Chobani",
  "year": "2020",
  "cover": "drop09",
  "group": "product", "short": "UX/UI, visual design &amp; research",
  "meta": "Chobani — UX/UI, Visual Design &amp; Research",
  "desc": ["UX/UI, visual design, and research for chobani.com: landing "
           "systems for every product line, including Greek Yogurt, Flip, "
           "Complete, Less Sugar and Drinks, plus foodservice, a recipe "
           "library with a step-by-step cooking mode, and product detail "
           "pages with nutritional highlights.",
            "Designed across desktop and mobile as one continuous system."],
  "pages": [
    # The site pages here were screen grabs of the live site; the component
    # files below carry the same work at the size it was drawn.
  ],
 },
 {
  "slug": "furniture", "title": "Furniture.com",
  "year": "2022",
  # The single mobile screens read as a set when they sit three to a row,
  # the same rhythm as the story slides that show three phones at once.
  "piece_width": {"mobile-set-1": 48, "mobile-set-2": 48, "mobile-set-3": 48},
  # A hairline of the page white survives on two edges of this slide.
  "piece_crop": {"f004": (0, 0, 0.010, 0.006)},
  "cover": "f012",
  "group": "product", "short": "Web design &amp; digital accessibility",
  "meta": "Furniture.com — with McKinsey &amp; studio Dumbar, 2022 — Web Design &amp; Digital Accessibility",
  "desc": ["Web design and digital accessibility for Furniture.com, with "
           "McKinsey and studio Dumbar: a search-led shopping experience "
           "built around finding your sofa, browsing rooms, and the chair "
           "that fits, carried by a warm identity and a bespoke furniture "
           "icon system.",
            "Eight colors, one per furniture category, each icon and "
           "campaign module built on the same palette and checked against "
           "black, white, and every neutral base for contrast.",
            "Designed responsively from large-screen heroes down to the "
           "mobile browsing flows."],
  "pages": [
    ("IMG", "furniture/mobile-set-1.png", "Mobile — home, categories, and the little ones",
     ["mobile"], {"crop": False, "split": False}),
    ("IMG", "furniture/mobile-set-2.png", "Mobile — browse rooms and the living room",
     ["mobile"], {"crop": False, "split": False}),
    ("IMG", "furniture/mobile-set-3.png", "Mobile — the product page and its details",
     ["mobile", "ecommerce"], {"crop": False, "split": False}),
    # Published whole. The black slide ground is the deck's own presentation
    # of the work, not a margin to be trimmed away.
    ("F", 1,  "Find it… — campaign banner", ["brand", "web"], {"crop": False}),
    ("F", 3,  "Everything for your living room — campaign", ["brand", "web"], {"crop": False}),
    ("F", 4,  "Room for the whole family — campaign", ["brand", "web"], {"crop": False}),
    ("F", 12, "Homepage — find your sofa", ["web"], {"crop": False}),
    ("F", 18, "Featured categories, by color", ["web"], {"crop": False}),
    ("F", 19, "Furniture for your little ones", ["web"], {"crop": False}),
    ("F", 21, "Featured — Sofas &amp; Sectionals", ["web", "product"], {"crop": False}),
    ("F", 22, "Browse rooms", ["web"], {"crop": False}),
    ("G", 3,  "Color update — before and after", ["brand"], {"crop": False}),
    ("G", 5,  "Color values — furniture, neutral, and action", ["brand"], {"crop": False}),
    ("G", 6,  "Color contrast, tested across the palette", ["brand"], {"crop": False}),
    ("G", 7,  "Icons and color — category campaign cards", ["brand", "web"], {"crop": False}),
    ("G", 9,  "Typography — Pangea with Reckless, and the spacing spec", ["brand", "editorial"], {"crop": False}),
    ("G", 11, "Hero type — Pangea Medium for the CTA", ["brand"], {"crop": False}),
    ("G", 13, "Hero type — the solid call to action", ["brand"], {"crop": False}),
    ("G", 12, "Hero type on the green ground", ["brand"], {"crop": False}),
    # The fuller cut of the same presentation: the category and product pages,
    # the mobile flows, and the campaign as it ran in social, display and OOH.
    ("H", 1,  "Seating — the category page", ["web"], {"crop": False}),
    ("H", 2,  "Category page — the chair that fits", ["web"], {"crop": False}),
    ("H", 8,  "Highland Sunflower Sofa — product page", ["web", "ecommerce"], {"crop": False}),
    ("H", 9,  "Product page — browse to go", ["web", "ecommerce"], {"crop": False}),
    ("H", 12, "Product page — you may also like", ["web", "ecommerce"], {"crop": False}),
    ("H", 19, "Search it, Find it, Buy it — story set", ["social"], {"crop": False}),
    ("H", 20, "Search it, Find it, Buy it — the second set", ["social"], {"crop": False}),
    ("H", 21, "Search it, Find it, Buy it — the third set", ["social"], {"crop": False}),
    ("IMG", "furniture/story-set-1.png", "Build your space, and Search it Find it Buy it — stories",
     ["social"], {"crop": False, "split": False}),
    ("H", 24, "The perfect chair for you — story", ["social"], {"crop": False}),
    ("H", 25, "Search it. Find it. Buy it. — story on red", ["social"], {"crop": False}),
    ("H", 26, "Your new sofa is waiting — social post", ["social"], {"crop": False}),
    ("H", 27, "Everything for your bedroom — social post", ["social"], {"crop": False}),
    ("H", 28, "Autumn sale — the icon grid", ["social", "brand"], {"crop": False}),
    ("H", 31, "Display — your new chair is waiting", ["brand", "web"], {"crop": False}),
    ("H", 33, "Display — room for the whole family", ["brand", "web"], {"crop": False}),
    ("H", 37, "Out of home — Search it, Find it, Buy it", ["brand"], {"crop": False}),
    ("H", 39, "Out of home — the second run", ["brand"], {"crop": False}),
  ],
 },
 {
  "slug": "lenka-ilic", "title": "Lenka Ilic",
  "year": "2024",
  "drop_tags": ["brand", "web"],
  "cover": "drop01",
  "group": "brand", "short": "Identity, website &amp; art direction",
  "meta": "Lenka Ilic Studio — Identity, Website &amp; Art Direction",
  # Everything stated here is on the pieces themselves or on the studio's own
  # pages: the material, the maker, the city, the year of founding.
  "desc": ["Identity, website and art direction for Lenka Ilic Studio, a "
           "furniture practice in Miami and New York. The objects are folded "
           "from recycled aluminium and made by hand in Delanson, New York, "
           "and each carries a debossed signature and a serial number.",
           "The mark is set in one weight and left alone. It sits small in "
           "the corner of the page and small on the metal, so the object is "
           "what is looked at: a grid of white forms on white, photographed "
           "against the roofline and in the rooms they are made for."],
  "pages": [
    # Everything comes from drop/lenka-ilic/.
  ],
 },
 {
  "slug": "bts-advocaten", "title": "Bektesevic Ter Steeg Advocaten",
  "year": "2026",
  "drop_tags": ["web", "brand"],
  # Two pages, each with its phone, to a row.
  "piece_width": {"drop02": 48, "drop03": 48, "drop04": 48, "drop05": 48},
  "cover": "drop01",
  "group": "product", "short": "Website &amp; identity",
  "meta": "Bektesevic Ter Steeg Advocaten — Website &amp; Identity",
  # The site is designed but the copy on it is the firm's own; nothing here
  # describes the practice beyond what the pages themselves state.
  "desc": ["Website and identity for Bektesevic Ter Steeg Advocaten, a "
           "criminal defence practice in Amsterdam. The wordmark sets the "
           "two names in a grotesque and the word <em>advocaten</em> in a "
           "serif, and the pages hold that pairing: the sentence runs "
           "between the two faces, so the emphasis falls inside the line "
           "rather than on a heading above it.",
           "Bands of pale blue and white carry the argument down the page, "
           "and the type is set large enough to be read at arm's length. "
           "Designed for the desktop and the phone, with expertise, "
           "lawyers and contact each taking the same structure."],
  "pages": [
    # Everything comes from drop/bts-advocaten/.
  ],
 },
 {
  "slug": "florida-blue", "title": "Florida Blue",
  "year": "2018–2019",
  "drop_tags": ["product"],
  "cover": "drop04",
  "group": "product", "short": "UI strategy &amp; design",
  "meta": "Florida Blue — with frog design, 2018–2019 — UX &amp; Visual Design",
  "desc": ["UI strategy and design with frog design for Florida Blue's "
           "member experience: Loom, an on-the-go companion that reads "
           "sentiment and triages urgency; Promise Card, a payment card "
           "that rewards health activity; and Health Hub, a member's "
           "healthcare in one view.",
            "I led the user research and testing, set the core UX and "
           "visual principles, and delivered the design system and visual "
           "libraries behind it, tested for accessibility throughout. "
           "Concepts extend into CareBuddies peer support, rewards and "
           "discounts, provider profiles, and the marketing site.",
            "The strategy sits underneath: each concept defined on its own "
           "terms, and the experience objectives mapped over time and "
           "scored, so the order of the roadmap can be argued for rather "
           "than asserted."],
  "pages": [
    # Every piece comes from drop/florida-blue/.

  ],
 },
 {
  "slug": "compass", "title": "Compass",
  "year": "2018",
  # The deck runs one slide to a line at 70% of the measure, which is 40% more
  # than the half page a deck slide normally takes. The business card is the
  # same 40% the other way, since a card is a small object.
  # drop09 arrived inside a PDF viewer's grey artboard.
  "piece_crop": {"drop09": (0.047, 0.12, 0.047, 0.12)},
  "piece_width": {"d005": 70, "d006": 70, "d007": 70, "d008": 70,
                  # both cards are small objects and are shown as such
                  "drop02": 30, "drop03": 30,
                  # the listing map is dense and needs the room
                  "drop09": 47},
  "cover": "d004-1",
  "group": "brand", "short": "Real estate marketing design",
  "meta": "Compass — Real Estate Marketing Design",
  "desc": ["Marketing design for the real estate brokerage Compass: the "
           "wordmark set against its field of dashes, the For Sale card "
           "in both black and white, and a digital banner system sized "
           "for every placement.",
            "A data-visualisation language for listings and market "
           "reports, covering call-out stats, inventory tables and "
           "summary figures, built to stay legible from a phone banner up "
           "to a printed sheet.",
            "Per-listing collateral too: neighborhood points-of-interest "
           "maps that place a building among its restaurants, galleries, "
           "parks, gyms and transit, alongside the everyday pieces an "
           "agent hands over, business cards, announcement cards, an "
           "agent introduction, and the <em>Compass and you</em> "
           "brochure."],
  "pages": [
    ("D", 4, "Graphic approach — the For Sale card", ["brand"]),
    ("D", 5, "Digital banner system", ["brand", "web"]),
    ("D", 6, "Data visualisation — call-out stats", ["brand", "product"]),
    ("D", 7, "Data visualisation — inventory tables", ["brand", "product"]),
    ("D", 8, "Data visualisation — tables", ["brand", "product"]),
    ("IMG", "compass/map.jpg", "245 10th Avenue — neighborhood points of interest", ["brand", "editorial"], {"crop": False}),
  ],
 },
 {
  "slug": "pratt", "title": "Pratt",
  # b087 kept a live browser toolbar, address bar and all.
  "piece_crop": {"b087": (0.075, 0, 0, 0)},
  "year": "2017–2020",
  "cover": "b090",
  "group": "book", "short": "Books, print &amp; cultural institution identity",
  "meta": "Pratt Institute — Adjunct Professor, 2017–2020 — Website, Video Art Direction &amp; Publication",
  "desc": ["Website design for Pratt Shows, the institute's annual "
           "end-of-year exhibition: an index of every school and programme "
           "held together by a soft-edged mask that lets the work bleed "
           "through the interface.",
            "That mask is the identity. It changes colour with the season, "
           "yellow, then white on grey, then grey on pink for Spring "
           "2018, and crops whatever sits inside it, so a rotating banner "
           "frames a plaster sculpture one week and a field of cast forms "
           "the next.",
            "Alongside it, video art direction for the show, print from "
           "the show postcards to the SCPS Fall 2019 brochure, and "
           "publication design for Prattfolio, the alumni magazine of "
           "Pratt Institute."],
  "pages": [
    ("B", 87, "Pratt Shows — programme index", ["web"], {"dechrome": 120}),  # tab strip + URL bar; taller than the auto-detect finds
    ("B", 88, "Pratt Shows — exhibition page", ["web"], {"dechrome": True}),
    ("B", 89, "Pratt Shows — video art direction", ["brand"]),
    ("B", 90, "Prattfolio — alumni magazine", ["editorial"]),
    ("IMG", "pratt/postcard-yellow.png", "Pratt Shows Spring 2018 — postcard", ["brand", "editorial"], {"crop": False}),
    ("IMG", "pratt/postcard-mint.png", "Pratt Shows Spring 2018 — postcard", ["brand", "editorial"], {"crop": False}),
    ("IMG", "pratt/postcard-pink.png", "Pratt Shows Spring 2018 — postcard", ["brand", "editorial"], {"crop": False}),
  ],
 },
 {
  "slug": "sasha-sedelnikov", "title": "Sasha Sedelnikov",
  "cover": "b091",
  "group": "book", "short": "Publication &amp; show identity",
  "meta": "Sasha Sedelnikov — Publication Design &amp; Show Identity",
  "desc": ["Publication design for <em>See you later</em>, a photobook by "
           "Sasha Sedelnikov, held in the Garage Museum of Contemporary "
           "Art, Moscow. Black-and-white and colour sequences are paced "
           "against the paper so the images set their own rhythm.",
            "The show identity for <em>Пучки серебряного света</em> "
           "(Bundles of Silver Light) at the Museum of the History of "
           "Yekaterinburg runs the title vertically down the poster, "
           "letting each photograph take the rest of the sheet."],
  "pages": [
    ("B", 91, "See you later — landscape spread", ["editorial"], {"cutout": 45}),
    ("B", 92, "See you later — horizon spread", ["editorial"], {"cutout": 45}),
    ("B", 93, "See you later — water spread", ["editorial"], {"cutout": 45}),
    ("B", 94, "See you later — portrait spread", ["editorial"], {"cutout": 45}),
    ("B", 95, "Пучки серебряного света — one poster, four images, on the street",
     ["brand", "editorial"]),
    ("B", 96, "Пучки серебряного света — one poster, four images, on the street",
     ["brand", "editorial"]),
  ],
 },
 {
  "slug": "sarah-crowner", "title": "Sarah Crowner",
  "year": "2016",
  "layout": "row",
  "group": "book", "short": "Monograph design",
  "meta": "Sarah Crowner — Monograph — Publication Design",
  "desc": ["Design of the complete monograph on the painter Sarah "
           "Crowner, whose sewn canvases and cut-and-stitched panels "
           "straddle the divide between fine and applied art. Cover, "
           "typography, grid, and the sequencing of essays and plates.",
            "Susan Cross's essay <em>Beetle in the Leaves</em> runs tight "
           "to the margin against installation views and figures, while "
           "the paintings take full spreads. The layout borrows the logic "
           "the work is built on: panels butted edge to edge, colour "
           "meeting colour without a seam."],
  "pages": [
    ("IMG", "sarah-crowner/cover.jpg", "Cover", ["editorial", "brand"], {"split": False, "rotate": 90}),
    ("IMG", "sarah-crowner/beetle-in-the-leaves.jpg", "Beetle in the Leaves — essay opening", ["editorial"], {"split": False, "rotate": -90}),
    ("IMG", "sarah-crowner/standing-totems.jpg", "Standing Totem 1 and 2, 2015 — plates", ["editorial"], {"split": False, "rotate": -90}),
    ("IMG", "sarah-crowner/rotated-commas.jpg", "Experienz #2 and Rotated Commas — figures", ["editorial"], {"split": False, "rotate": -90}),
  ],
 },
 {
  "slug": "dada", "title": "Dada",
  "year": "2016",
  "cover": "charset",
  "group": "type", "short": "Typeface",
  "meta": "Dada — Typeface — Passion Project",
  "kind": "specimen",
  "font": {"family": "Dada", "file": "Dada-Regular",
           "caps": "ACIMOPQRXY", "glyphs": 387, "chars": 370, "year": "2020",
           "sample": "MOMA QUARTZ PARIS",
           "ladder": "DADA IS NOT DEAD, IT SMELLS OF LAUGHTER"},
  "desc": ["A Dada intervention on a grotesque, drawn as capitals and "
           "figures only. Ten of the twenty-six, <em>A C I M O P Q R X "
           "Y</em>, are cut out and redrawn as biomorphic forms in the "
           "manner of Arp and Taeuber-Arp: blobs with eyes, tentacles, "
           "stray dots. The other sixteen are left exactly as they were.",
            "Set a word and the typeface behaves; set a name and it comes "
           "apart. <em>QUARTZ</em> keeps its U, T and Z and loses the "
           "rest to the shapes. The joke only works because the neutral "
           "letters stay neutral. The ransom-note effect comes from the "
           "collision, not from the drawing.",
            "Built from Helvetica Neue LT Com, whose outlines are "
           "Linotype’s. A private experiment, never released."],
  "pages": [
    ("IMG", "dada/hero.png",     "DADA", ["brand", "editorial"], {"crop": False}),
    ("IMG", "dada/capitals.png", "The ten redrawn capitals", ["brand", "editorial"], {"crop": False}),
    ("IMG", "dada/words.png",    "MOMA, QUARTZ, PARIS", ["brand", "editorial"], {"crop": False}),
    ("IMG", "dada/charset.png",  "Capitals and figures — the whole set", ["brand", "editorial"], {"crop": False}),
    ("IMG", "dada/setting.png",  "Set at text size, all caps", ["editorial"], {"crop": False}),
    ("IMG", "dada/ladder.png",   "One line at falling sizes", ["editorial"], {"crop": False}),
    ("IMG", "dada/inverted.png", "DADA, reversed", ["brand"], {"crop": False}),
  ],
 },
 {
  "slug": "spiritual-labour", "title": "Spiritual Labour",
  "year": "2014",
  "cover": "wordmark",
  "group": "type", "short": "Typeface",
  "meta": "Spiritual Labour — Typeface — Passion Project",
  "kind": "specimen",
  "font": {"family": "Spiritual Labour", "file": "SpiritualLabour-Regular",
           "glyphs": 92, "chars": 91, "year": "2014",
           "set": "Capitals &amp; figures",
           "sample": "SPIRITUAL LABOUR",
           "rows": ["ABCDEFGHIJKLM", "NOPQRSTUVWXYZ",
                    "0123456789", "?!.,;:"],
           "ladder": "SPIRITUAL LABOUR"},
  "desc": ["A display face of capitals and figures, drawn as one weight. The "
           "letters are cut on a curve rather than a stem: bowls swell and "
           "close, terminals turn back on themselves, and several capitals "
           "give up their counters entirely.",
           "Ninety-two glyphs. There is no lowercase, so the page sets "
           "everything typed into it as capitals."],
  "pages": [
    ("IMG", "spirituallabour/wordmark.png", "The wordmark", ["brand"], {"crop": False}),
    ("IMG", "spirituallabour/charset.png", "Capitals and figures", ["brand"], {"crop": False}),
  ],
 },
 {
  "slug": "isaac-howell", "title": "Isaac Howell",
  "year": "Ongoing",
  # Each poster beside its own reverse, two to a row. The Rome scans that
  # used to sit here are gone: the print PDFs carry the same sheets at
  # twice the size and the hash kept those.
  "piece_width": {"b098-1": 48, "b098-2": 48, "rome1": 48, "rome2": 48,
                  "pit2": 48, "pit1": 48},
  "cover": "b098-1",
  "group": "book", "short": "Exhibition identity &amp; publication",
  "meta": "Isaac Howell — Exhibition Identity, Poster &amp; Publication",
  "desc": ["Identity and one-page publications for solo shows of the "
           "artist Isaac Soh Fujita Howell, across Public Gallery in "
           "London and T293 in Rome. For <em>A rabid dog has no choice "
           "but to bite</em> at Public Gallery the title circles the "
           "poster edge as a frame, leaving the painting to hold the "
           "centre.",
            "Two shows at T293 followed. <em>By order from above (and we "
           "are all dutiful citizens)</em> sets the details on "
           "overlapping black cards that lock into one another like a "
           "puzzle. <em>Malign Influence on the Information "
           "Interchange</em> rings the sheet with its own title, then "
           "runs the same sheet inverted with photographs set into the "
           "ring.",
            "The run extends into newsprint, where the text turns with the "
           "page, and into <em>The Man Who Turned into a Wall</em>, which "
           "sequences drawings against script."],
  "pages": [
    # b097 is this same poster photographed on a phone; the flat artwork below
    # says it better, so only one of the two is published.
    ("B", 99, "T293, Rome — poster", ["brand"], {"cutout": 60, "span": 6}),
    ("B", 98, ["A rabid dog has no choice but to bite — poster",
               "Publication — spread"], ["editorial"], {"span": 6}),
    ("IMG", "isaac-howell/rome1.png", "Malign Influence on the Information Interchange — poster",
     ["brand"], {"crop": False}),
    ("IMG", "isaac-howell/rome2.png", "Malign Influence — the sheet reversed",
     ["brand"], {"crop": False}),
    ("IMG", "isaac-howell/pit2.png", "Audiovisual, Geneva — poster",
     ["brand"], {"crop": False}),
    ("IMG", "isaac-howell/pit1.png", "Audiovisual — the sheet reversed",
     ["editorial"], {"crop": False}),
  ],
 },
 {
  "slug": "willow-and-wu", "title": "Willow and Wu",
  "year": "2024",
  "cover": "b101",
  "group": "brand", "short": "Film identity, poster &amp; titles",
  "meta": "Kathy Meng — Film Identity, Poster &amp; Titles",
  "desc": ["Identity for <em>Willow and Wu</em>, a short independent film "
           "directed by Kathy Meng: a heavy condensed wordmark that stacks "
           "into a block, set against stills and a full credit line.",
           "Carried through the poster and the on-screen title sequence."],
  "pages": [
    ("B", 100, "Willow and Wu — wordmark", ["brand"], {"crop": False}),
    ("B", 101, "Poster design", ["brand"], {"frac": 35}),
    ("B", 102, "Movie titles", ["brand"], {"split": False, "bleed": True}),
  ],
 },
 {
  "slug": "literature-paper", "title": "Literature Paper",
  "year": "2016",
  "cover": "drop01",
  "group": "book", "short": "Publication design &amp; concept",
  "meta": "Yale Literature Paper — Publication Design &amp; Concept",
  "desc": ["Publication design and concept for the first issue of the "
           "Yale School of Art literature paper: cut-paper forms in "
           "orange, blue, and yellow crashing through the grid, with text "
           "setting itself into and around the shapes.",
            "Each spread treats its subject as an object to be pulled "
           "apart: a gourd, a garlic house, a table of contents that "
           "refuses to sit still."],
  "pages": [
    # The four spreads come from drop/ as flat scans; the deck
    # reproductions of the same pages were lower resolution.
  ],
 },
]
