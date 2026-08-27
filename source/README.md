# source/

Scans and photographs that are not from the decks.

`data.py` refers to these with an `IMG` entry:

    ("IMG", "sarah-crowner/cover.jpg", "Cover", ["editorial"], {"split": False, "rotate": -90})

- the path is relative to this folder
- `rotate` turns a spread scanned on its side upright (degrees, counter-clockwise)
- `split: False` keeps a spread whole; without it the extractor may cut on the
  book's gutter

Then: `python3 extract.py <slug> && python3 build.py`
