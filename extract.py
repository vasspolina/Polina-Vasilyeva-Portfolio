#!/usr/bin/env python3
"""Cut the individual artworks out of each deck page.

Deck slides often carry two or three separate images on a flat background with
a gutter between them. Trimming the whole slide would keep that gutter as a
black or white stripe, so instead each page is split on its background gutters
and every artwork is written out as its own image.

Writes assets/<slug>/*.jpg (full size) + *-1200.jpg (display) and manifest.json.

    python3 extract.py            # all projects
    python3 extract.py verizon    # just one
"""
import json, os, re, sys
from collections import Counter
import numpy as np
import pypdfium2 as pdfium
from PIL import Image, ImageDraw, ImageFilter

import data

ROOT = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(ROOT, "assets")
SOURCE = os.path.join(ROOT, "source")   # scans and photographs, for "IMG" entries

RENDER_SCALE = 2.0     # 1920x1080 slide -> 3840x2160
TARGET_PX = 2400       # a piece should carry enough pixels for the top rendition
MAX_PAGE_PX = 9000     # ceiling on a re-render, so a tiny crop cannot ask for a
                       # 100-megapixel page
BAND = 0.045           # shave the slide edge before anything else
BG_TOL = 20            # colour distance that still counts as background
MIN_GAP = 0.012        # a gutter must be this fraction of the axis to split artworks on
ROW_GAP = 0.003        # the slide leaves only a hairline above its caption
MAX_PARTS = 6          # more pieces than this reads as one composition
MIN_SHARE = 0.10       # each piece must hold this share of the page's content
JUNK_SHARE = 0.03      # ...below this it is a stray label, not a piece at all
MIN_PX = 60            # smallest artwork worth keeping, in rendered pixels
NOISE = 0.002          # a row/column needs this share of pixels to count as content
TEXT_H = 0.08          # a row band shorter than this is slide chrome, not artwork
EDGE = 0.10            # ...and only when it sits this close to the top or bottom
# Display renditions, in WebP. The raw crop (up to ~3800px) is deliberately not
# published: at DPR 2 a 604px column asks for ~1208px, and if the only larger
# candidate is the original the browser downloads all 3800px of it.
WIDTHS = (600, 1200, 1600, 2400)
QUALITY = 80


def content_mask(arr, bg):
    """True where the pixel differs from the slide background."""
    return np.abs(arr.astype(np.int16) - np.array(bg, dtype=np.int16)).max(axis=2) > BG_TOL


def filled_along(mask, axis):
    """Content profile plus a boolean of which lines really carry content.

    PDF rendering leaves a few stray off-background pixels in otherwise empty
    gutters; without a noise floor a single one of them makes a gutter look
    occupied and no page ever splits.
    """
    profile = mask.sum(axis=0 if axis == 0 else 1)
    other = mask.shape[0] if axis == 0 else mask.shape[1]
    return profile, profile > max(2, int(NOISE * other))


def segments(mask, axis, min_gap=MIN_GAP):
    """Every run of content along an axis, split on pure-background gutters.

    axis=0 scans columns, axis=1 scans rows. Returns [(start, end), ...].
    """
    profile, filled = filled_along(mask, axis)
    n = len(profile)
    if not filled.any():
        return [], profile

    out, start, run = [], None, 0
    gap_min = max(5, int(n * min_gap))
    for i, f in enumerate(filled):
        if f:
            if run and start is not None and run >= gap_min:
                out.append((start, i - run))
                start = i
            elif start is None:
                start = i
            run = 0
        else:
            run += 1
    if start is not None:
        out.append((start, n - run if run else n))
    return out, profile


def drop_chrome(bands, h):
    """Discard the slide's own header, caption, and page number.

    Chrome is a short band pinned to the top or bottom edge. Height alone is
    not enough — a slide whose whole subject is a logo has only a short band —
    so position decides it, and a centred mark is always kept.
    """
    if len(bands) < 2:
        return bands
    keep = [(a, b) for a, b in bands
            if (b - a) >= TEXT_H * h or EDGE * h <= (a + b) / 2 <= (1 - EDGE) * h]
    return keep or bands


def tight(mask, box):
    """Shrink a box to its content, ignoring stray pixels."""
    x0, y0, x1, y1 = box
    sub = mask[y0:y1, x0:x1]
    _, rows_f = filled_along(sub, axis=1)
    _, cols_f = filled_along(sub, axis=0)
    rows = np.where(rows_f)[0]
    cols = np.where(cols_f)[0]
    if not len(rows) or not len(cols):
        return None
    return (x0 + cols[0], y0 + rows[0], x0 + cols[-1] + 1, y0 + rows[-1] + 1)


def drop_backdrop(im, tol=50, pad=2):
    """Replace a flat black photographic backdrop with white.

    Only the black actually connected to the border is removed, so black
    *inside* the subject survives. Opt-in per page (debg=True): plenty of this
    work is black by design — the vault site, the SISTERS screens, the Willow
    and Wu wordmark — and keying those out would erase the artwork.
    """
    a = np.asarray(im)
    dark = (a.max(axis=2) <= tol).astype(np.uint8) * 255
    h, w = dark.shape

    # Flood the dark mask inward from the border via ImageDraw's bucket fill:
    # seed a 1px frame that is guaranteed to be inside the mask.
    m = Image.fromarray(dark, "L")
    framed = Image.new("L", (w + 2, h + 2), 255)
    framed.paste(m, (1, 1))
    ImageDraw.floodfill(framed, (0, 0), 128, thresh=0)
    connected = np.asarray(framed)[1:h + 1, 1:w + 1] == 128

    if not connected.any():
        return im
    grow = Image.fromarray((connected * 255).astype(np.uint8), "L")
    grow = grow.filter(ImageFilter.MaxFilter(2 * pad + 1))   # bite past the halo
    out = np.array(a, copy=True)
    out[np.asarray(grow) > 0] = (255, 255, 255)

    # Removing a phone bezel leaves the screen ringed in white; pull the frame
    # back in to whatever is still not paper-white.
    ink = out.min(axis=2) < 248
    rows = np.where(ink.any(axis=1))[0]
    cols = np.where(ink.any(axis=0))[0]
    if len(rows) and len(cols):
        out = out[rows[0]:rows[-1] + 1, cols[0]:cols[-1] + 1]
    return Image.fromarray(out, "RGB")


def peel_frame(out, tol, cap=0.06, run=5):
    """Shave the residual top strip left after the median crop.

    The median measures the frame at the middle of each side, but the corners
    are thicker, so a band of device survives along the top. Peel whole
    mostly-dark rows off the top only, and never more than `cap` of the height.
    `run` light rows end the peel, so the single anti-aliased row at the very
    edge cannot stop it before it starts.

    Deliberately top-only: peeling the other three sides ate a screenshot's own
    full-width maroon panel and 100px of its width. A dark band elsewhere is
    the artwork, not the device.
    """
    prof = (out.max(axis=2) < tol).mean(axis=1)
    limit = int(len(prof) * cap)
    lo = 0
    for n in range(limit):
        if (prof[n:n + run] <= 0.5).all():
            break
        lo = n + 1
    return out[lo:] if lo else out


def crop_screen(im, tol=160, inset=None):
    """Crop a phone mockup down to the screen inside its device frame.

    Measuring the frame means walking in from each side and taking a low
    percentile of the dark run — low, not median, because a run only ever
    *grows* when dark artwork sits against the bezel, so the small values are
    the honest ones. `tol` sits above the bezel's specular rim: that rim peaks
    at 137 on this device, so a 140 threshold lands on a knife edge and the
    measurement flips per row, which is what tore one of the mockups.

    Pass `inset` as (left, top, right, bottom) to skip measuring. Screenshot
    content that reaches the bezel on every row defeats any statistic, and a
    set of mockups sharing one device template is better pinned once than
    guessed five times.
    """
    a = np.asarray(im)
    dark = a.max(axis=2) < tol
    if not dark.any():
        return im

    dr = np.where(dark.any(axis=1))[0]
    dc = np.where(dark.any(axis=0))[0]
    y0, y1, x0, x1 = dr[0], dr[-1] + 1, dc[0], dc[-1] + 1
    body = dark[y0:y1, x0:x1]
    h, w = body.shape

    def lead(lines):
        """25th-percentile count of dark pixels before the first light one."""
        runs = [int(np.argmin(line)) if line.any() and not line.all() else 0
                for line in lines]
        return int(np.percentile(runs, 25)) if runs else 0

    if inset:
        left, top, right, bottom = inset
    else:
        # Sample the middle of each axis: the rounded corners make the
        # outermost lines unrepresentative of the frame's real thickness.
        ry = slice(int(h * 0.2), int(h * 0.8))
        rx = slice(int(w * 0.2), int(w * 0.8))
        left = lead(body[ry, :])
        right = lead(body[ry, ::-1])
        top = lead(body.T[rx, :])
        bottom = lead(body.T[rx, ::-1])

    box = (x0 + left, y0 + top, x1 - right, y1 - bottom)
    if box[2] - box[0] < w * 0.5 or box[3] - box[1] < h * 0.5:
        return im
    out = np.array(im.crop(box))
    out = peel_frame(out, tol)

    # A rectangular crop of a rounded screen keeps a dark wedge in each top
    # corner. Shave it row by row — whiten only the dark run reaching in from
    # each end — rather than blanking a fixed corner square, whose size never
    # matches the arc. Bounded on both axes so a dark row of artwork is safe,
    # and top-only because the bottom corners often hold photography.
    ch, cw = out.shape[0], out.shape[1]
    reach = max(4, int(cw * 0.15))
    edge_tol = 200        # the arc fades to mid-grey; the status bar is far lighter
    for y in range(min(ch, max(4, int(ch * 0.10)))):
        row = out[y]
        dark = row.max(axis=1) < edge_tol
        if not dark[:reach].all():
            n = int(np.argmin(dark[:reach]))
            row[:n] = (255, 255, 255)
        if not dark[-reach:].all():
            n = int(np.argmin(dark[::-1][:reach]))
            if n:
                row[cw - n:] = (255, 255, 255)
        out[y] = row
    return Image.fromarray(out, "RGB")


def encode_video(src, dest, start, duration, width=1280, kbps=1200):
    """Trim and compress a clip with avconvert, and pull a poster frame.

    The masters are long and heavy — the Beijing gradient is ten minutes and
    75MB — so the site carries a short excerpt. Returns the poster as a PIL
    image. Re-encoding is skipped when the output is already newer than the
    source, since it is slow and the input rarely changes.
    """
    import encode as enc
    # The masters live on an external drive. When it is not mounted, keep the
    # encode already in assets rather than failing the whole run — the crash
    # left the manifest unwritten and silently stale.
    if not os.path.exists(src):
        if not os.path.exists(dest):
            raise FileNotFoundError(f"no source and no existing encode: {src}")
        print(f"{'':18} {'':4} {'':18}  -- source offline, keeping {os.path.basename(dest)}")
    elif not (os.path.exists(dest) and os.path.getmtime(dest) > os.path.getmtime(src)):
        if os.path.exists(dest):
            os.remove(dest)                       # AVAssetWriter will not overwrite
        enc.encode(src, dest, width=width, kbps=kbps,
                   start=start, duration=duration)

    # Quartz must be imported before the frame is copied: it registers the
    # CGImage type, and without it the generator hands back an unbridged
    # pointer that CGImageDestination silently refuses to write.
    from Quartz import (CGImageDestinationCreateWithURL, CGImageDestinationAddImage,
                        CGImageDestinationFinalize)
    from AVFoundation import AVURLAsset, AVAssetImageGenerator
    from Foundation import NSURL
    import CoreMedia
    asset = AVURLAsset.URLAssetWithURL_options_(
        NSURL.fileURLWithPath_(os.path.abspath(dest)), None)
    gen = AVAssetImageGenerator.assetImageGeneratorWithAsset_(asset)
    gen.setAppliesPreferredTrackTransform_(True)
    d = asset.duration()
    mid = (d.value / d.timescale) / 2 if d.timescale else 0
    img = gen.copyCGImageAtTime_actualTime_error_(
        CoreMedia.CMTimeMakeWithSeconds(mid, 600), None, None)[0]

    tmp = dest + ".poster.png"
    out = CGImageDestinationCreateWithURL(
        NSURL.fileURLWithPath_(os.path.abspath(tmp)), "public.png", 1, None)
    CGImageDestinationAddImage(out, img, None)
    CGImageDestinationFinalize(out)
    poster = Image.open(tmp).convert("RGB")
    poster.load()
    os.remove(tmp)
    return poster


def cut_out(im, tol=26, pad=1, dark=None):
    """Make the ground behind a subject transparent.

    Same flood fill as drop_backdrop, but keyed to whatever colour the border
    actually is and writing alpha rather than white — a white card on a grey
    page reads as a card, and these are product shots, not cards.

    `dark` switches from "within tol of the corner colour" to "darker than
    this", which is what a photographic backdrop needs: it is lit unevenly, so
    matching a single corner sample spreads a couple of percent and stops.
    """
    rgb = im.convert("RGB")
    a = np.asarray(rgb)
    if dark:
        flat = (a.max(axis=2) <= dark).astype(np.uint8) * 255
    else:
        bg = np.array(rgb.getpixel((2, 2)), dtype=np.int16)
        flat = (np.abs(a.astype(np.int16) - bg).max(axis=2) <= tol).astype(np.uint8) * 255
    h, w = flat.shape

    m = Image.fromarray(flat, "L")
    framed = Image.new("L", (w + 2, h + 2), 255)
    framed.paste(m, (1, 1))
    ImageDraw.floodfill(framed, (0, 0), 128, thresh=0)
    ground = np.asarray(framed)[1:h + 1, 1:w + 1] == 128
    if not ground.any() or ground.mean() > 0.985:
        return im

    grow = Image.fromarray((ground * 255).astype(np.uint8), "L")
    grow = grow.filter(ImageFilter.MaxFilter(2 * pad + 1))
    out = np.dstack([a, np.full((h, w), 255, np.uint8)])
    out[np.asarray(grow) > 0, 3] = 0

    # Trim the margin that keying just emptied, or the piece keeps carrying a
    # band of nothing where the backdrop used to be.
    # Trim to where the artwork actually is. A row has to carry real content
    # to count: keying a screenshot leaves stray light specks behind — carousel
    # dots, a status-bar glyph — and `any()` would let one of them hold the
    # whole margin open.
    # A row counts if it carries a real share of what the densest row carries.
    # An absolute floor would cut a tall narrow object — a packaging bag stood
    # on end — down to a sliver, while a relative one still drops the specks
    # keying leaves behind: a carousel dot, a line of caption.
    solid = out[:, :, 3] > 0
    rw, cw = solid.mean(axis=1), solid.mean(axis=0)
    rows = np.where(rw > rw.max() * 0.06)[0]
    cols = np.where(cw > cw.max() * 0.06)[0]
    if len(rows) and len(cols):
        out = out[rows[0]:rows[-1] + 1, cols[0]:cols[-1] + 1]
    return Image.fromarray(out, "RGBA")


def ahash(im, n=10):
    """Small perceptual hash, for spotting the same artwork cut twice.

    Flatten alpha onto white first: converting RGBA straight to L discards the
    alpha, so every cut-out shape hashes as the same near-empty square and the
    whole type specimen looked like one repeated image.
    """
    if im.mode in ("RGBA", "LA"):
        flat = Image.new("RGB", im.size, "white")
        flat.paste(im, mask=im.split()[-1])
        im = flat
    g = np.asarray(im.convert("L").resize((n, n), Image.LANCZOS), dtype=float)
    return (g > g.mean()).tobytes()





def embedded_ceiling(page):
    """The widest bitmap actually placed on a slide.

    A deck page is vector, so it will render at any scale asked of it, but the
    photograph or screenshot inside it has a fixed size. Rendering past that
    enlarges the bitmap and returns a file that is heavier without being
    sharper. Zero means nothing was found, and no ceiling is applied.
    """
    widest = 0
    try:
        for obj in page.get_objects():
            if obj.type != 3:            # 3 is an image object
                continue
            try:
                widest = max(widest, obj.get_bitmap().to_pil().width)
            except Exception:
                continue
    except Exception:
        return 0
    return widest


def whiten_corners(im, thresh=48):
    """Flood the dark wedges a rounded window screenshot leaves in its corners.

    A grab of a browser window keeps the window's rounded corners, and what
    sits outside the curve is black. Cropping it away would take a bite out of
    the page; flooding from each corner over the connected dark region takes
    the wedge and nothing else, because the wedge does not touch the artwork.
    """
    rgb = im.convert("RGB")
    w, h = rgb.size
    before = np.asarray(rgb).copy()
    # On a light picture the wedge can be a grey shadow rather than true black,
    # and there is no dark artwork for a wider threshold to eat into.
    if before.mean() > 170:
        thresh = 110
    for xy in ((0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)):
        if max(rgb.getpixel(xy)) < thresh:
            ImageDraw.floodfill(rgb, xy, (255, 255, 255), thresh=thresh)
    after = np.asarray(rgb)
    # A wedge is a sliver. If the flood ran on past it the picture was dark by
    # design, not a window grab, and the original stands.
    if (before != after).any(axis=2).mean() > 0.08:
        return im.convert("RGB")
    return rgb


def flatten_white(im):
    """Flatten a keyed cutout onto white before it is published.

    drop_backdrop and cut_out remove a studio ground and leave the piece on a
    transparent field, meant to sit on the page the artwork was printed for —
    white. Left transparent, the site's own background shows through instead:
    correct on the light theme by coincidence, but a dark smudge around the
    piece in dark mode, since the browser paints the page colour behind it.
    """
    if im.mode in ("RGBA", "LA"):
        bg = Image.new("RGB", im.size, (255, 255, 255))
        bg.paste(im, mask=im.split()[-1])
        return bg
    return im.convert("RGB")


def pad_out(im, frac):
    """Set a mark on a field of its own ground.

    A tight crop is right for a photograph, which fills its frame, but a
    wordmark's clearspace is part of the drawing. frac is a share of the
    longer edge, added on all four sides in the colour the corners already
    hold.
    """
    rgb = im.convert("RGB")
    ground = tuple(np.median(
        np.array([rgb.getpixel(p) for p in
                  ((1, 1), (rgb.width - 2, 1), (1, rgb.height - 2),
                   (rgb.width - 2, rgb.height - 2))]), axis=0).astype(int))
    m = round(max(im.size) * frac)
    out = Image.new("RGB", (im.width + 2 * m, im.height + 2 * m), ground)
    out.paste(rgb, (m, m))
    return out

def trim_edge_lines(im, limit=12):
    """Shave a thin uniform band off the edges.

    Cropping leaves a strip of whatever the piece was cut from: a hairline of
    white or black, or a mid grey from a window frame. The band is measured
    first, then judged by the line just past it.

    Flatness is judged by majority rather than by variance. A sliver of a black
    slide ground running down the side of a browser screenshot is black for
    96% of its length and white where the window's own chrome meets it, and a
    variance test reads that as texture and leaves the sliver in place.
    """
    a = np.asarray(im.convert("RGB")).astype(np.int16)
    h, w = a.shape[:2]

    def flat(line):
        """The dominant value, and how much of the line holds it."""
        med = np.median(line, axis=0)
        share = (np.abs(line - med).max(axis=1) <= 18).mean()
        return med, share

    def depth(get, n):
        cap = min(limit, n // 4)
        first, share0 = flat(get(0))
        if share0 < 0.9:
            return 0
        k = 0
        while k < cap:
            med, share = flat(get(k))
            if share < 0.9 or np.abs(med - first).max() > 24:
                break
            k += 1
        if not k or k >= cap:
            return 0
        beyond, _ = flat(get(k))
        return k if np.abs(beyond - first).max() > 34 else 0

    top = depth(lambda i: a[i], h)
    bot = depth(lambda i: a[h - 1 - i], h)
    left = depth(lambda i: a[:, i], w)
    right = depth(lambda i: a[:, w - 1 - i], w)
    if not (top or bot or left or right):
        return im
    return trim_edge_lines(im.crop((left, top, w - right, h - bot)), limit)


def trim_white_margin(im, tol=248):
    """Trim a plain white margin of any depth from all four sides.

    A "slices" band is cut by fraction of the page, full width — honest about
    the seam between two photos, but blind to a photograph that is narrower
    than the page and sits centred in its own white margin. trim_edge_lines
    caps at a hairline depth on purpose; this has no cap, because the margin
    here can run to a sixth of the frame.
    """
    a = np.asarray(im.convert("RGB"))
    h, w = a.shape[:2]

    def white(line):
        # By share, not by minimum: the seam between two photographs on one
        # slide can run the full width as a thin dark rule, and a single row
        # of it crossing an otherwise blank margin should not stop the trim.
        return (line.min(axis=-1) >= tol).mean() >= 0.97

    top = 0
    while top < h and white(a[top]):
        top += 1
    bot = 0
    while bot < h - top and white(a[h - 1 - bot]):
        bot += 1
    left = 0
    while left < w and white(a[:, left]):
        left += 1
    right = 0
    while right < w - left and white(a[:, w - 1 - right]):
        right += 1
    if not (top or bot or left or right):
        return im
    return im.crop((left, top, w - right, h - bot))


def trim_corners(im, thresh=0.03, limit=0.05):
    """Shave the dark wedges a rounded device corner leaves behind.

    Cropping inside the bezel gives a rectangle, but the screen's corners are
    round, so each corner keeps a small dark triangle. Walk in from every edge
    while that edge line still carries a share of near-black, capped so a
    genuinely dark screenshot cannot be eaten away.
    """
    a = np.asarray(im.convert("RGB"))
    h, w, _ = a.shape
    dark = a.max(axis=2) < 40

    def walk(get, n):
        cap = int(n * limit)
        i = 0
        while i < cap and get(i).mean() > thresh:
            i += 1
        return i

    top = walk(lambda i: dark[i], h)
    bot = walk(lambda i: dark[h - 1 - i], h)
    left = walk(lambda i: dark[:, i], w)
    right = walk(lambda i: dark[:, w - 1 - i], w)
    if not (top or bot or left or right):
        return im
    return im.crop((left, top, w - right, h - bot))

def drop_chrome_bar(im, cap=0.25, run=12):
    """Cut the browser window's title bar off a website mockup.

    The bar is whatever sits above the page itself, so find the page rather
    than the bar: walk down from the top to the first row that is almost
    entirely the page's own dominant colour and stays that way for `run` rows.
    Detecting the bar directly does not work — its traffic-light dots and URL
    strip differ per template, and a flatness test cannot tell a white toolbar
    from a white page.
    """
    a = np.asarray(im.convert("RGB"))
    h, w = a.shape[:2]
    body = a[int(h * 0.35):int(h * 0.9)].reshape(-1, 3)
    vals, counts = np.unique(body[::7], axis=0, return_counts=True)
    page = vals[counts.argmax()].astype(int)

    near = (np.abs(a.astype(int) - page).max(axis=2) <= 14).mean(axis=1)
    limit = int(h * cap)
    for y in range(limit):
        if (near[y:y + run] > 0.92).all():
            return im.crop((0, y, w, h)) if y else im

    # The page may open on a photograph rather than its own flat ground, in
    # which case there is no page-coloured row to find. Fall back to following
    # the bar itself: it starts at row zero and is flat across its width.
    bar = np.median(a[1, int(w * 0.35):int(w * 0.65)], axis=0).astype(int)
    y = 0
    while y < limit:
        row = a[y]
        if (np.abs(row.astype(int) - bar).max(axis=1) <= 18).mean() < 0.55:
            break
        y += 1
    return im.crop((0, y, w, h)) if 4 < y < limit else im


def regions(im, split=True, crop=True, rows=False):
    """Return one box per artwork on the page.

    Slide chrome is stripped first, so a caption running the full width can no
    longer bridge the gutter between two artworks and defeat the split. Only
    vertical gutters then separate artworks — splitting on horizontal ones
    would cut stacked wordmarks in half.
    """
    arr = np.asarray(im)
    bg = im.getpixel((2, 2))
    mask = content_mask(arr, bg)
    h, w = mask.shape

    all_bands, _ = segments(mask, axis=1, min_gap=ROW_GAP)
    bands = drop_chrome(all_bands, h)
    if not bands:
        return [(0, 0, w, h)]
    top = min(a for a, _ in bands)
    bot = max(b for _, b in bands)

    # Only trust the slide's margins when chrome was actually identified. On a
    # dark slide the header, artwork and caption can merge into one band, and
    # reaching out to the frame then drags the header and page number back in.
    chrome_found = len(bands) < len(all_bands)

    def field():
        """The slide's own margins: everything between header and caption."""
        if not chrome_found:
            return (0, top, w, bot)
        above = [b for a, b in all_bands if b <= top]
        below = [a for a, b in all_bands if a >= bot]
        return (0, max(above) if above else 0, w, min(below) if below else h)

    # crop=False keeps the slide's own ground around the artwork — right when
    # the background is part of the composition. Reach out to the chrome that
    # was dropped rather than stopping at the ink, otherwise a wordmark still
    # ends up flush against the edge of its own field.
    if not crop:
        return [field()]

    if rows:
        # Some slides stack their images instead of setting them side by side.
        # Splitting on horizontal gutters is opt-in because it would otherwise
        # cut a stacked wordmark, or a page from its own caption.
        segs, prof = segments(mask[top:bot, :], axis=1, min_gap=0.005)
        tot = float(prof.sum()) or 1.0
        segs = [c for c in segs if prof[c[0]:c[1]].sum() / tot >= JUNK_SHARE]

        if len(segs) < 2:
            # Two photographs butted straight together leave no gutter to find,
            # so cut at the sharpest change in row colour instead.
            band = np.asarray(im)[top:bot].mean(axis=1)
            step = np.linalg.norm(np.diff(band, axis=0), axis=1)
            lo, hi = int(len(step) * 0.15), int(len(step) * 0.85)
            if hi > lo:
                k = lo + int(step[lo:hi].argmax())
                if step[k] > 24:
                    segs = [(0, k), (k + 1, bot - top)]
        if 2 <= len(segs) <= MAX_PARTS:
            out = []
            for a, b in segs:
                t = tight(mask, (0, top + a, w, top + b))
                if t and (t[2] - t[0]) >= MIN_PX and (t[3] - t[1]) >= MIN_PX:
                    out.append(t)
            if out:
                return out

    cols, profile = segments(mask[top:bot, :], axis=0)
    total = float(profile.sum()) or 1.0
    share = lambda a, b: profile[a:b].sum() / total

    # A caption or page number stranded beside the artwork is its own tiny
    # column. Drop those outright rather than letting them veto the split or
    # pad the artwork out with background.
    cols = [c for c in cols if share(*c) >= JUNK_SHARE] or cols
    if not split or not (2 <= len(cols) <= MAX_PARTS) or \
       any(share(*c) < MIN_SHARE for c in cols):
        cols = [(min(a for a, _ in cols), max(b for _, b in cols))]
    boxes = [(a, top, b, bot) for a, b in cols]

    tights = []
    for b in boxes:
        t = tight(mask, b)
        if t and (t[2] - t[0]) >= MIN_PX and (t[3] - t[1]) >= MIN_PX:
            tights.append(t)
    if not tights:
        return [(0, 0, w, h)]

    # A mark alone on its slide keeps the slide's own margins, the way it is
    # presented in the deck. A computed pad is derived from the mark's short
    # side, which for a wide lockup is its cap height — nowhere near the air
    # the deck gives it. Only when the mark is alone: siblings would each
    # expand to the full width and land on top of each other.
    if len(tights) == 1 and is_sparse(mask, tights[0]) and chrome_found:
        return [field()]

    return [clearspace(mask, t, top, bot, w) for t in tights]


SPARSE = 0.75          # ink density below this reads as a mark, not a photograph
DROP = os.path.join(ROOT, "drop")   # hand-picked images, one folder per project
DROP_LONG = 2600       # keep enough pixels for the 2400 rendition


def is_sparse(mask, box):
    """True for a wordmark or logo, false for a photograph or screenshot.

    Measured across this archive the two groups separate cleanly: marks and
    wordmarks land at 0.20-0.59 ink density inside their box, photographs and
    screenshots at 0.90-1.00.
    """
    x0, y0, x1, y1 = box
    return mask[y0:y1, x0:x1].mean() < SPARSE


def clearspace(mask, box, top, bot, w, frac=0.35):
    """Give a wordmark or logo back the air the tight crop took off it.

    Cropping to the ink is right for a photograph, which fills its own frame,
    but wrong for a mark: the space around it is part of the drawing, and
    without it the letters run into the edge of the tile. Sparse pieces —
    less than `thresh` ink inside their box — are padded; dense ones are left
    alone. Padding stays inside the artwork band, so it cannot pull a caption
    or a header back into frame.

    Measured across this archive the two groups separate cleanly: marks and
    wordmarks land at 0.20-0.59, photographs and screenshots at 0.90-1.00.
    """
    if not is_sparse(mask, box):
        return box
    x0, y0, x1, y1 = box
    pad = int(frac * min(x1 - x0, y1 - y0))
    return (max(0, x0 - pad), max(top, y0 - pad),
            min(w, x1 + pad), min(bot, y1 + pad))


# A filename that is a camera dump, a screenshot, a deck export or a scratch
# name carries no caption. Publishing it would put "Screen Shot 2022-11-28 at
# 6.14.14 PM" under a piece of work.
JUNK = re.compile(
    r"^(screen ?shot|screenshot|img|dsc|photo|image|untitled)\b"
    r"|\d{4}-\d{2}-\d{2}"          # a date stamp
    r"|\bpage \d+$"                 # a slide number off a deck export
    r"|\bcopy\b"
    r"|presentation|audit|final design",
    re.I)


def is_label(text):
    """Does this filename read as a caption someone wrote, or as a dump?

    Two words is the test that does the work: anyone naming a file to caption
    it writes "Exhibition poster", while every scratch name in the folders —
    ysoa97, Haworthggf, ccc — is a single run of characters.
    """
    if not text or JUNK.search(text):
        return False
    if len(set(text.lower().replace(" ", ""))) <= 2:      # "ssss", "ccc"
        return False
    return len([w for w in re.split(r"\W+", text) if w]) >= 2


def dropped(slug, title, tags):
    """Images Polina put in drop/<slug>/ by hand.

    They are finished artwork, not deck slides: nothing is detected, split or
    cropped. Each is scaled so its long edge matches a deck piece, so a pasted
    image sits at the same size in the grid as everything cut from the PDFs.
    A leading number orders the folder and is dropped from the caption:
    "02 Exhibition poster.png" -> "Exhibition poster".
    """
    folder = os.path.join(DROP, slug)
    os.makedirs(folder, exist_ok=True)
    out = []
    for name in sorted(os.listdir(folder)):
        stem, ext = os.path.splitext(name)
        if ext.lower() not in (".png", ".jpg", ".jpeg", ".webp", ".tif", ".tiff"):
            continue
        im = Image.open(os.path.join(folder, name))
        im = im.convert("RGBA") if im.mode in ("RGBA", "LA") else im.convert("RGB")
        # A spread photographed on a black studio ground arrives with the
        # ground attached. If most of the border is near-black, key it out so
        # the piece sits on the page rather than in a black box.
        edge = np.asarray(im.convert("RGB"))
        border = np.concatenate([edge[0], edge[-1], edge[:, 0], edge[:, -1]])
        # Only when the border is overwhelmingly black: a studio ground runs
        # right around the object, whereas a photograph that merely happens to
        # be dark does not.
        if (border.max(axis=1) < 50).mean() > 0.85:
            keyed = cut_out(im, dark=60)
            # Only a ground, never the artwork. If keying would take most of
            # the picture, the black was the design, not the surface it was
            # photographed on, and the original stands.
            ka = np.asarray(keyed.convert("RGBA"))
            solid = ka[:, :, 3] > 8
            kept = solid.mean()
            # And never when what survives is light: a white wordmark reversed
            # out of black needs that black to be visible at all, so removing
            # it would leave the mark floating invisibly on a pale page.
            light = ka[:, :, :3][solid].mean() > 170 if solid.any() else False
            # And only when it takes a margin rather than a quarter of the
            # picture. Keying 44% of an Instagram story ate the model's face.
            if kept > 0.75 and not light:
                im = keyed
        # Before the resize, not after: scaling softens the boundary between a
        # stray line and the picture, and the trim needs that edge sharp to
        # tell one from the other.
        im = trim_edge_lines(im)
        # A cap, not a target. Scaling a small file up to the working size
        # invents detail that is not in it: the result is soft and heavy at
        # once. A source smaller than the cap is published at its own size and
        # the rendition ladder simply starts lower.
        long_edge = max(im.size)
        if long_edge > DROP_LONG:
            k = DROP_LONG / long_edge
            im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
        # Strip only the ordering prefix. A character class of digits and
        # spaces would be greedy and eat the caption's own first word:
        # "05 5G Ultra Wideband" would come back as "G Ultra Wideband".
        caption = re.sub(r"^\d{1,3}[._\-\s]+", "", stem).replace("_", " ").strip()
        # Fall back to the project's own name, which is never wrong; renaming
        # the file to something with two words in it sets the caption instead.
        out.append((im, caption if is_label(caption) else title, tags))
    return out


def main():
    only = sys.argv[1:]
    # Read the file in Python and hand pdfium the bytes. Given a path, pdfium
    # opens it through its own C library, which is refused for anything outside
    # the project directory; Python's own open() is not. Same document, and it
    # no longer depends on where the deck happens to live.
    def load(path):
        # A deck can live on a drive that is not plugged in. Report it and
        # carry on: the projects that do not read it still rebuild, and the
        # ones that do keep the assets and manifest entries they already have.
        try:
            with open(os.path.expanduser(path), "rb") as fh:
                return pdfium.PdfDocument(fh.read())
        except FileNotFoundError:
            print(f"source unavailable, skipping what needs it: {path}")
            return None

    docs = {k: load(v) for k, v in data.SOURCES.items()}
    os.makedirs(SOURCE, exist_ok=True)
    manifest = {}

    for proj in data.PROJECTS:
        slug = proj["slug"]
        if only and slug not in only:
            continue
        needed = {e[0] for e in proj["pages"] if e[0] in docs}
        missing = sorted(k for k in needed if docs[k] is None)
        if missing:
            print(f"{slug:18} skipped, source {', '.join(missing)} unavailable")
            continue
        d = os.path.join(ASSETS, slug)
        os.makedirs(d, exist_ok=True)
        for f in os.listdir(d):                      # start clean
            if f.endswith(".mp4"):                   # keep encodes; they are slow
                continue
            os.remove(os.path.join(d, f))

        items = []
        for entry in proj["pages"]:
            src, page, caption, tags = entry[:4]
            opts = entry[4] if len(entry) > 4 else {}

            if src == "VID":
                # A clip: encode it into the project's assets and use its
                # poster frame as the still that carries it in the grid.
                dest = os.path.join(d, os.path.basename(page))
                try:
                    im = encode_video(opts["src"], dest,
                                      opts.get("start", 0), opts.get("duration", 30),
                                      width=opts.get("width", 1280),
                                      kbps=opts.get("kbps", 1200))
                except FileNotFoundError as exc:
                    # The clip lives on an external drive. Losing it should
                    # cost this one piece, not the whole site: say so loudly
                    # and carry on, and it returns when the drive is plugged in.
                    print(f"{slug:18} SKIPPED  {os.path.basename(page)} "
                          f"— {exc}")
                    continue
                key = os.path.splitext(os.path.basename(page))[0]
                video = os.path.basename(page)
            elif src == "IMG":
                # A photograph or scan, not a deck slide: `page` is a path under
                # source/. No BAND is shaved — there is no slide chrome to lose —
                # and rotate= turns a spread scanned on its side upright.
                path = os.path.join(SOURCE, page)
                if not os.path.exists(path):
                    print(f"{slug:18} MISSING  {page}")
                    continue
                im = Image.open(path)
                # Keep alpha when the source has it: the type specimens are
                # drawn on a transparent ground so the letterforms sit on the
                # page instead of on a white card.
                im = im.convert("RGBA") if im.mode in ("RGBA", "LA") else im.convert("RGB")
                if opts.get("rotate"):
                    im = im.rotate(opts["rotate"], expand=True)
                key = os.path.splitext(os.path.basename(page))[0]
                video = None
            else:
                im = docs[src][page - 1].render(
                    scale=opts.get("scale", RENDER_SCALE)).to_pil().convert("RGB")
                if opts.get("crop") is not False:
                    # BAND shaves the slide chrome off a portfolio deck. A page
                    # published whole is the artwork itself and keeps its
                    # margins; shaving it clipped captions off the bottom.
                    w, h = im.size
                    im = im.crop((0, int(h * BAND), w, h - int(h * BAND)))
                key = f"{src.lower()}{page:03d}"
                video = None

            if opts.get("slices"):
                # Explicit bands, given as (top, bottom) fractions of the page.
                # Some slides hold two photographs with no gutter a detector can
                # find — on one the join is a thin black rule — and the page
                # carries a black footer that belongs to neither.
                boxes = [(0, round(im.height * a), im.width, round(im.height * b))
                         for a, b in opts["slices"]]
            elif video or opts.get("crop") is False:
                # Whole frame, no detection. A video poster must match its clip
                # exactly, and a full-bleed design has no margin to trim — its
                # background colour *is* the artwork, and detection would read
                # it as empty and crop away everything but the shapes.
                boxes = [(0, 0, im.width, im.height)]
            else:
                # split=False for a page whose parts read as one composition —
                # a stacked wordmark, an icon sheet — that gutters would cut up.
                boxes = regions(im, split=opts.get("split", True),
                                crop=opts.get("crop", True),
                                rows=opts.get("rows", False))
            # A piece that occupies a corner of a slide comes out small at the
            # page's scale, and no rendition can add detail that was never
            # rendered. Work out what the widest piece needs and, if the page
            # was rendered too small for it, render it again larger and scale
            # the boxes to match.
            if src not in ("IMG", "VID") and boxes and not video:
                widest = max(b[2] - b[0] for b in boxes)
                base = opts.get("scale", RENDER_SCALE)
                if widest and widest < TARGET_PX:
                    want = TARGET_PX / widest
                    ceiling = MAX_PAGE_PX / max(im.width, 1)
                    # Never ask for more than the artwork on the slide holds.
                    art = embedded_ceiling(docs[src][page - 1])
                    if art:
                        ceiling = min(ceiling, max(1.0, art / max(im.width, 1)))
                    factor = min(want, ceiling)
                    if factor > 1.05:
                        big = docs[src][page - 1].render(
                            scale=base * factor).to_pil().convert("RGB")
                        bw, bh = big.size
                        im = big.crop((0, int(bh * BAND), bw, bh - int(bh * BAND)))
                        boxes = [tuple(int(round(v * factor)) for v in b)
                                 for b in boxes]

            keep = opts.get("keep")
            for i, box in enumerate(boxes, 1):
                if keep and i not in keep:
                    continue
                piece = im.crop(box)
                if opts.get("slices"):
                    piece = trim_white_margin(piece)
                stem = key + (f"-{i}" if len(boxes) > 1 else "")
                if opts.get("debg"):
                    piece = drop_backdrop(piece)
                if opts.get("dechrome"):
                    cut = opts["dechrome"]
                    piece = (piece.crop((0, cut, piece.width, piece.height))
                             if isinstance(cut, int) and cut is not True
                             else drop_chrome_bar(piece))
                if opts.get("cutout"):
                    cut = opts["cutout"]
                    piece = cut_out(piece, dark=cut if isinstance(cut, int)
                                    and cut is not True else None)
                if opts.get("debezel"):
                    # Cropping inside the frame already excludes the rounded
                    # corners; keying out afterwards would eat any dark
                    # artwork that reaches the screen edge.
                    piece = crop_screen(piece, inset=opts.get("inset"))
                    piece = trim_corners(piece)

                # Before the renditions are written: cropping a piece that has
                # already been saved changes nothing on disk.
                cropbox = (proj.get("piece_crop") or {}).get(stem)
                if cropbox:
                    # (top, right, bottom, left) as fractions of the piece, for
                    # chrome that no detector can safely tell from artwork:
                    # a browser window, an iOS status bar, a story overlay.
                    t, r, b, l = cropbox
                    pw, ph = piece.size
                    piece = piece.crop((round(pw * l), round(ph * t),
                                        pw - round(pw * r), ph - round(ph * b)))
                # Explicit slices are already measured, so the automatic trim
                # has nothing to add and can do harm: a slide header carries a
                # small wordmark over one tenth of the width, which still reads
                # as a flat band and gets shaved away row by row. A page
                # published whole (crop: False) is the same case at the
                # extreme — a solid-colour slide ground around a small logo
                # reads as border on every side, and the trim ate down to the
                # logo itself.
                if not opts.get("slices") and opts.get("crop") is not False:
                    piece = trim_edge_lines(piece)

                if opts.get("pad"):
                    piece = pad_out(piece, opts["pad"])

                # Do not publish beyond the resolution the slide actually
                # holds. A vector page renders at any scale, but the bitmap
                # placed on it does not, and a rendition wider than that
                # bitmap is an enlargement wearing a bigger number. That
                # reasoning assumes the bitmap IS the artwork — a photo or a
                # screenshot filling the piece. A page published whole
                # (crop: False) is usually a vector composition — a wordmark
                # on a solid ground — where a small embedded bitmap (a mark
                # rasterised into the file, a texture fill) is incidental,
                # not the subject, and would cap a 3840px slide to a 600px
                # logo's native size.
                if src not in ("IMG", "VID") and not video and opts.get("crop") is not False:
                    art = embedded_ceiling(docs[src][page - 1])
                    if art and piece.width > art >= 600:
                        share = piece.width / max(im.width, 1)
                        cap = int(art * min(1.0, share))
                        if 600 <= cap < piece.width:
                            piece = piece.resize(
                                (cap, round(piece.height * cap / piece.width)),
                                Image.LANCZOS)
                            # Downsampling blends the pixels either side of an
                            # edge, so a black ground trimmed a moment ago
                            # returns as a dark fringe. Trim what the resize
                            # put back.
                            piece = trim_edge_lines(piece)

                piece = whiten_corners(piece)
                piece = flatten_white(piece)
                targets = [t for t in WIDTHS if t < piece.width]
                targets.append(min(piece.width, WIDTHS[-1]))
                widths = []
                for target in sorted(set(targets)):
                    disp = piece if target == piece.width else piece.resize(
                        (target, round(piece.height * target / piece.width)),
                        Image.LANCZOS)
                    disp.save(os.path.join(d, f"{stem}-{target}.webp"),
                              quality=QUALITY, method=5)
                    widths.append(target)

                # The published height matches the largest rendition, so the
                # width/height attributes describe what actually loads.
                top = widths[-1]
                cap = (caption[i - 1] if isinstance(caption, (list, tuple))
                       and i - 1 < len(caption) else
                       caption[-1] if isinstance(caption, (list, tuple)) else caption)
                item = {"stem": stem, "caption": cap, "tags": tags,
                        "w": top, "h": round(piece.height * top / piece.width),
                        "widths": widths, "source": src, "page": page}
                item["hash"] = ahash(piece).hex()
                if opts.get("frac"):
                    item["frac"] = opts["frac"]

                if opts.get("bleed"):
                    # Runs the full width of the window, outside the page
                    # margin: a cinema title card wants the whole screen.
                    item["bleed"] = True
                if opts.get("span"):
                    # Pin the column count when the proportion alone gets it
                    # wrong: a wide screenshot is not always a full-measure one.
                    item["span"] = opts["span"]
                if video:
                    item["video"] = video
                    # Long clips are not worth pushing at every visitor; they
                    # get a poster and load only when someone presses play.
                    item["autoplay"] = opts.get(
                        "autoplay", opts.get("duration", 30) <= 25)
                items.append(item)
            print(f"{slug:18} {src} {str(page):>18}  -> {len(boxes)} image(s)")

        # Anything Polina dropped into drop/<slug>/ joins the project after the
        # deck pages, in filename order, at the same size as a deck piece.
        # The tags a dropped image inherits. Taking them from the project's
        # first entry was wrong: Verizon's first entry is a homepage, so every
        # Retail SEM page came out tagged "web" and was laid out as a website.
        # The commonest tag across the project describes it far better.
        counts = Counter(t for e in proj["pages"] for t in e[3])
        base_tags = proj.get("drop_tags") or (
            [counts.most_common(1)[0][0]] if counts else ["brand"])
        for n, (piece, cap, tags) in enumerate(
                dropped(slug, proj["title"], base_tags), 1):
            stem = f"drop{n:02d}"
            # Before the renditions are written, not after: cropping a piece
            # that has already been saved changes nothing on disk.
            cropbox = (proj.get("piece_crop") or {}).get(stem)
            if cropbox:
                t, r, b, l = cropbox
                pw, ph = piece.size
                piece = piece.crop((round(pw * l), round(ph * t),
                                    pw - round(pw * r), ph - round(ph * b)))
                piece = trim_edge_lines(piece)
            piece = whiten_corners(piece)
            piece = flatten_white(piece)
            targets = [t for t in WIDTHS if t < piece.width]
            targets.append(min(piece.width, WIDTHS[-1]))
            widths = []
            for target in sorted(set(targets)):
                disp = piece if target == piece.width else piece.resize(
                    (target, round(piece.height * target / piece.width)),
                    Image.LANCZOS)
                disp.save(os.path.join(d, f"{stem}-{target}.webp"),
                          quality=QUALITY, method=5)
                widths.append(target)
            top = widths[-1]
            items.append({"stem": stem, "caption": cap, "tags": tags,
                          "w": top, "h": round(piece.height * top / piece.width),
                          "widths": widths, "source": "DROP", "page": stem,
                          "hash": ahash(piece).hex()})
            print(f"{slug:18} DROP {stem:>18}  -> {cap}")

        # The decks show the same artwork on more than one slide, and a page
        # can also split into near-identical halves. Keep the first of each.
        seen, keep = set(), []
        for it in items:
            hsh = it.pop("hash", None)
            if hsh and hsh in seen:
                print(f"{slug:18} {'':4} {'':18}  -- dropped {it['stem']}, repeat of an earlier image")
                continue
            if hsh:
                seen.add(hsh)
            keep.append(it)
        manifest[slug] = keep

    path = os.path.join(ROOT, "manifest.json")
    if only and os.path.exists(path):
        existing = json.load(open(path))
        existing.update(manifest)
        manifest = existing
    json.dump(manifest, open(path, "w"), indent=1, ensure_ascii=False)
    print("\ntotal images:", sum(len(v) for v in manifest.values()))


if __name__ == "__main__":
    main()
