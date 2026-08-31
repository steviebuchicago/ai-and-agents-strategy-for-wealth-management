"""Box-and-arrow / matrix diagrams for the AI & Agents for Asset & Wealth
Management executive guide.

Hand-written SVG strings -> cairosvg at scale 2 (the house style shared with
getting-started-with-openclaw). Authoring space is 1900 x H; the SVG is emitted
at half size so each PNG lands on exactly 1900 x H device pixels.

Every label is taken verbatim from ../../RESEARCH.md (the authoritative facts
sheet), measured against its box before it is drawn (svgkit.fit / svgkit.wrap
raise on overflow), and checked glyph-by-glyph against the real font cmap
(house.assert_renderable) so nothing renders as a .notdef box. No figure or
regulation name is invented here.
"""

import os

from house import (BODY, CRIMSON, CYAN, HEAD, MUTED, OUT, PANEL, STROKE,
                   svg_to_png, text_w, verify)
from svgkit import (H, W, arrow, block, canvas, fit, heading, line, rrect, txt,
                    wrap)

SCRATCH = os.path.join(OUT, "_generate", "_svg")
os.makedirs(SCRATCH, exist_ok=True)

# extra house tones (identical to the openclaw diagrams module)
BAND_FILL = "#0D1A2B"
BAND_STROKE = "#1B3350"
CHIP_FILL = "#193049"
CHIP_STROKE = "#2B4C6D"
WARM = "#1C1A22"        # warm-dark ground for crimson callouts
GAP_FILL = "#171A24"    # the "gap you fill" panel ground

DOTS = " · "        # middle dot separator used in the source labels


def emit(name, body, h=H, w=W):
    svg = os.path.join(SCRATCH, name + ".svg")
    with open(svg, "w", encoding="utf-8") as fh:
        fh.write(canvas(body, w, h, solid=True))
    png = os.path.join(OUT, name + ".png")
    svg_to_png(svg, png, scale=2)
    return verify(png)


# --------------------------------------------------------------- shared bits --
def chip_row(rx, ry, rw, ch, items, size=21, pad=22, gap=16,
             fill=CHIP_FILL, stroke=CHIP_STROKE, tfill=BODY, sw=1.5, where=""):
    """Equal-width chips filling `rw` in a single row. Guards every label."""
    n = len(items)
    cw = (rw - 2 * pad - gap * (n - 1)) / n
    out, x = [], rx + pad
    for it in items:
        fit(it, size, cw - 20, False, (where or "chip") + ": " + it)
        out.append(rrect(x, ry, cw, ch, 12, fill, stroke, sw))
        out.append(txt(x + cw / 2, ry + ch / 2 + size * 0.35, it, size,
                       tfill, False, "middle"))
        x += cw + gap
    return "".join(out)


def chip_stack(x, y, w, items, chip_h, gap, size=20, tpad=18, dotc=CYAN,
               fill=CHIP_FILL, stroke=CHIP_STROKE, tfill=BODY, where=""):
    """A vertical column of bullet chips. Each label wraps to at most two
    lines inside its chip (wrap raises on a word too wide); a dot sits at the
    left. Returns (svg, y-after-the-stack)."""
    out, cy = [], y
    wrap_w = w - 2 * tpad - 24
    for it in items:
        lines = wrap(it, size, wrap_w)
        if len(lines) > 2:
            raise ValueError("%s: chip needs %d lines: %r"
                             % (where or "chip", len(lines), it))
        out.append(rrect(x, cy, w, chip_h, 12, fill, stroke, 1.5))
        out.append('<circle cx="%.1f" cy="%.1f" r="4.6" fill="%s"/>'
                   % (x + tpad + 3, cy + chip_h / 2, dotc))
        lh = size * 1.26
        ty = cy + chip_h / 2 - (len(lines) - 1) * lh / 2 + size * 0.34
        tx = x + tpad + 22
        for ln in lines:
            out.append(txt(tx, ty, ln, size, tfill))
            ty += lh
        cy += chip_h + gap
    return "".join(out), cy


def check(x, y, s, color=CYAN, sw=3.5):
    """A tick mark drawn as an SVG path (the font has no U+2713)."""
    return ('<path d="M %.1f %.1f l %.1f %.1f l %.1f %.1f" fill="none" '
            'stroke="%s" stroke-width="%.1f" stroke-linecap="round" '
            'stroke-linejoin="round"/>'
            % (x, y + s * 0.55, s * 0.4, s * 0.45, s * 0.9, -s * 1.0,
               color, sw))


def vlabel(x, y, s, size, fill, bold=True):
    """Vertically-set (rotated -90) centred label."""
    from house import esc, assert_renderable
    assert_renderable(s, s)
    return ('<text transform="rotate(-90 %.1f %.1f)" x="%.1f" y="%.1f" '
            'font-family="Helvetica, Arial, sans-serif" font-size="%.1f" '
            'font-weight="%s" fill="%s" text-anchor="middle">%s</text>'
            % (x, y, x, y, size, "bold" if bold else "normal", fill, esc(s)))


# ============================================================ 1. four audiences ==
AUDIENCES = [
    ("THE BOARD",  "oversight" + DOTS + "risk appetite" + DOTS
                   + "fiduciary duty" + DOTS + "the bet"),
    ("THE C-SUITE", "operating model" + DOTS + "economics" + DOTS
                    + "executive accountability"),
    ("LEADERSHIP", "execution" + DOTS + "org design" + DOTS + "the RACI"
                   + DOTS + "sequencing"),
    ("THE FIRM",   "capability" + DOTS + "training" + DOTS + "culture"
                   + DOTS + "adoption"),
]


def four_audiences():
    L = []
    title = "One strategy, four audiences"
    L.append(title)
    s = [heading(title, y=104)]

    # right-edge chip
    chip = "each reads its own layer"
    L.append(chip)
    cw = text_w(chip, 22, True) + 56
    s.append(rrect(1840 - cw, 74, cw, 46, 23, CHIP_FILL, CYAN, 2))
    s.append(txt(1840 - cw / 2, 104, chip, 22, CYAN, True, "middle"))

    # the why -> who -> how rail on the left
    rail_x = 150
    top, bot = 214, 946
    s.append(arrow(rail_x, top - 6, rail_x, bot + 6, CYAN, 4, size=13))
    rlabel = "why → who → how"
    L.append(rlabel)
    s.append(vlabel(96, (top + bot) / 2, rlabel, 26, CYAN))

    # four bands
    bx, bw = 250, 1590
    n = len(AUDIENCES)
    gap = 22
    bh = (bot - top - gap * (n - 1)) / n
    for i, (name, desc) in enumerate(AUDIENCES):
        y = top + i * (bh + gap)
        s.append(rrect(bx, y, bw, bh, 16, BAND_FILL, BAND_STROKE))
        s.append(rrect(bx, y, 10, bh, 5, CYAN, CYAN, 0))
        # audience name (left zone)
        fit(name, 34, 360, True, "audience name")
        s.append(txt(bx + 46, y + bh / 2 + 12, name, 34, HEAD, True))
        # descriptor (right zone), vertically centred, wrap-guarded
        dz_x = bx + 470
        dz_w = bx + bw - 40 - dz_x
        L.append(desc)
        lines = wrap(desc, 27, dz_w)
        assert len(lines) <= 2, (name, lines)
        cy = y + bh / 2 - (len(lines) - 1) * 19 + 10
        for ln in lines:
            s.append(txt(dz_x, cy, ln, 27, BODY))
            cy += 38
        # thin divider between the two zones
        s.append(line(bx + 450, y + 26, bx + 450, y + bh - 26, BAND_STROKE, 1.5))

    return emit("four-audiences", "".join(s), h=1000), L


# ============================================================ 2. value & shifts ==
VALUE_POOLS = [
    ("Investment & Research", "research cycles accelerate"),
    ("Distribution",          "capacity freed for advice"),
    ("Operations",            "cost and toil down"),
    ("Trading & Execution",   "manual workflows automated"),
]
SHIFTS = [
    "Judgment over analysis",
    "Distribution & trust is the battleground",
    "Mass customization becomes economical",
]


def value_and_shifts():
    L = []
    title = "Where AI creates value in AWM"
    L.append(title)
    s = [heading(title, y=104)]

    # ---- left: four value-pool cards (2x2) --------------------------------
    lx, lw = 60, 1120
    top = 190
    gx, gy = 30, 30
    cw = (lw - gx) / 2
    ch = (940 - top - gy) / 2
    for i, (name, effect) in enumerate(VALUE_POOLS):
        r, c = divmod(i, 2)
        x = lx + c * (cw + gx)
        y = top + r * (ch + gy)
        s.append(rrect(x, y, cw, ch, 18, PANEL, STROKE))
        s.append(rrect(x + 30, y + 34, 54, 8, 4, CYAN, CYAN, 0))
        fit(name, 31, cw - 60, True, "value pool name")
        s.append(txt(x + 30, y + 116, name, 31, HEAD, True))
        L.append(name)
        L.append(effect)
        fit(effect, 26, cw - 60, False, "value pool effect")
        s.append(txt(x + 30, y + 166, effect, 26, CYAN))
        s.append(txt(x + 30, y + ch - 34, "value pool", 20, MUTED))

    # ---- right: the "three shifts" panel ----------------------------------
    rx, rw = 1220, 620
    s.append(rrect(rx, top, rw, 940 - top, 20, GAP_FILL, STROKE))
    s.append(txt(rx + 40, top + 58, "THREE SHIFTS", 26, CYAN, True))
    s.append(txt(rx + 40, top + 92, "how the game changes", 22, MUTED))
    iy = top + 150
    row_h = (940 - top - 150 - 40) / 3
    for i, sh in enumerate(SHIFTS):
        y = iy + i * row_h
        s.append(rrect(rx + 30, y, rw - 60, row_h - 24, 14, PANEL, STROKE))
        s.append(txt(rx + 62, y + 50, str(i + 1), 30, CYAN, True))
        L.append(sh)
        lines = wrap(sh, 26, rw - 60 - 120, True)
        assert len(lines) <= 2, (sh, lines)
        cy = y + (row_h - 24) / 2 - (len(lines) - 1) * 17 + 9
        for ln in lines:
            s.append(txt(rx + 110, cy, ln, 26, HEAD, True))
            cy += 34

    return emit("value-and-shifts", "".join(s), h=1000), L


# ========================================================== 3. governance stack ==
def governance_stack():
    L = []
    title = "The governance stack — and the gap"
    L.append(title)
    s = [heading(title, y=100)]
    cap = ("Classic model risk management does not cover your agents. "
           "That layer is yours to build.")
    L.append(cap)
    fit(cap, 25, 1780, False, "governance caption")
    s.append(txt(60, 150, cap, 25, MUTED))

    px, pw = 60, 1780
    # ---- TOP: models -------------------------------------------------------
    ty, th = 214, 250
    s.append(rrect(px, ty, pw, th, 18, PANEL, STROKE))
    h1 = "MODELS — MODEL-RISK REGULATION"
    L.append(h1)
    fit(h1, 32, pw - 80, True, "models header")
    s.append(txt(px + 40, ty + 66, h1, 32, HEAD, True))
    s.append(txt(px + 40, ty + 102, "supervised model risk management",
                 22, MUTED))
    top_chips = ["independent validation", "monitoring", "documentation",
                 "three lines of defense"]
    L += top_chips
    s.append(chip_row(px, ty + 140, pw, 74, top_chips, size=23,
                      where="models chip"))

    # ---- MIDDLE: the gap (crimson) ----------------------------------------
    my, mh = 494, 320
    s.append(rrect(px, my, pw, mh, 18, GAP_FILL, CRIMSON, 3))
    # the "gap you fill" tab straddling the top edge
    tab = "THE GAP YOU FILL"
    L.append(tab)
    tw = text_w(tab, 21, True) + 52
    s.append(rrect(px + 40, my - 24, tw, 48, 24, WARM, CRIMSON, 2.5))
    s.append(txt(px + 40 + tw / 2, my - 24 + 32, tab, 21, CRIMSON, True,
                 "middle"))
    h2 = "AGENTIC AI — outside its scope"
    L.append(h2)
    fit(h2, 34, pw - 80, True, "agentic header")
    s.append(txt(px + 40, my + 92, h2, 34, HEAD, True))
    s.append(txt(px + 40, my + 128,
                 "no supervisory framework yet — the firm builds this",
                 22, CRIMSON))
    mid_chips = ["permissions", "budget caps", "audit log", "shadow mode",
                 "human gate", "approvals"]
    L += mid_chips
    s.append(chip_row(px, my + 170, pw, 78, mid_chips, size=22,
                      fill=WARM, stroke="#5A2A22", tfill=HEAD,
                      where="agentic chip"))

    # ---- BOTTOM: anchor ----------------------------------------------------
    by, bh = 844, 250
    anchor_w = 1140
    s.append(rrect(px, by, anchor_w, bh, 18, PANEL, STROKE))
    h3 = "ANCHOR — NIST AI RMF"
    L.append(h3)
    fit(h3, 32, anchor_w - 80, True, "anchor header")
    s.append(txt(px + 40, by + 66, h3, 32, HEAD, True))
    s.append(txt(px + 40, by + 102, "the recognized framework to anchor to",
                 22, MUTED))
    bot_chips = ["Govern", "Map", "Measure", "Manage"]
    L += bot_chips
    s.append(chip_row(px, by + 140, anchor_w, 74, bot_chips, size=24,
                      where="nist chip"))

    # EU AI Act side note
    ex = px + anchor_w + 30
    ew = px + pw - ex
    s.append(rrect(ex, by, ew, bh, 18, WARM, CYAN, 2))
    eu_h = "EU AI Act"
    L.append(eu_h)
    s.append(txt(ex + 34, by + 58, eu_h, 28, CYAN, True))
    eu_body = "still phasing in where an EU nexus exists"
    L.append(eu_body)
    elines = wrap(eu_body, 24, ew - 68)
    cy = by + 108
    for ln in elines:
        s.append(txt(ex + 34, cy, ln, 24, BODY))
        cy += 34

    return emit("governance-stack", "".join(s), h=1150), L


# ==================================================== 4. target operating model ==
HUB_CHIPS_R1 = ["standards", "platform", "governance"]
HUB_CHIPS_R2 = ["reusable patterns", "model & vendor evaluation"]
SPOKES = [
    ("Investments", (330, 250)),
    ("Distribution & Advice", (1570, 250)),
    ("Operations", (300, 560)),
    ("Risk & Compliance", (1600, 560)),
    ("Corporate/Enterprise", (950, 900)),
]


def target_operating_model():
    L = []
    title = "The AI operating model — hub and spoke"
    L.append(title)
    s = [heading(title, y=100)]

    hub_cx, hub_cy = 950, 555
    hub_w, hub_h = 600, 300
    hx, hy = hub_cx - hub_w / 2, hub_cy - hub_h / 2

    # spokes first (so connectors sit under the boxes)
    sw_, sh_ = 320, 128
    for name, (scx, scy) in SPOKES:
        s.append(arrow(hub_cx, hub_cy, scx, scy, MUTED, 2.5,
                       double=True, size=10))
    for name, (scx, scy) in SPOKES:
        x, y = scx - sw_ / 2, scy - sh_ / 2
        s.append(rrect(x, y, sw_, sh_, 16, PANEL, STROKE))
        fit(name, 26, sw_ - 40, True, "spoke name")
        s.append(txt(scx, scy - 6, name, 26, HEAD, True, "middle"))
        s.append(txt(scx, scy + 30, "builds on the platform", 21, MUTED,
                     False, "middle"))
        L.append(name)
    L.append("builds on the platform")

    # hub on top
    s.append(rrect(hx, hy, hub_w, hub_h, 20, GAP_FILL, CYAN, 3))
    hub_t = "CENTER OF ENABLEMENT"
    L.append(hub_t)
    fit(hub_t, 32, hub_w - 60, True, "hub title")
    s.append(txt(hub_cx, hy + 62, hub_t, 32, HEAD, True, "middle"))
    s.append(txt(hub_cx, hy + 96, "the hub", 22, CYAN, False, "middle"))
    L += HUB_CHIPS_R1
    L += HUB_CHIPS_R2
    s.append(chip_row(hx, hy + 128, hub_w, 60, HUB_CHIPS_R1, size=20, pad=24,
                      gap=14, where="hub chip"))
    s.append(chip_row(hx, hy + 200, hub_w, 60, HUB_CHIPS_R2, size=20, pad=24,
                      gap=14, where="hub chip"))

    # bridge-leaders side note (bottom-left corner, kept clear of spokes)
    bx, by, bwd, bhd = 60, 916, 470, 118
    s.append(rrect(bx, by, bwd, bhd, 16, WARM, CRIMSON, 2))
    s.append(txt(bx + 30, by + 48, "Bridge leaders", 26, CRIMSON, True))
    bl = "AI fluency + market expertise"
    L.append("Bridge leaders")
    L.append(bl)
    fit(bl, 24, bwd - 60, False, "bridge leaders detail")
    s.append(txt(bx + 30, by + 86, bl, 24, BODY))

    return emit("target-operating-model", "".join(s), h=1050), L


# ========================================================== 5. data foundation ==
FLOW = [
    "Sources (structured + unstructured)",
    "Unified data platform",
    "Data products (domain-owned)",
    "Governance: quality · lineage · access control",
    "Agents & models",
]


def data_foundation():
    L = []
    title = "The data foundation agents read from"
    L.append(title)
    s = [heading(title, y=104)]

    n = len(FLOW)
    x0, gap = 60, 62
    bw = (1780 - gap * (n - 1)) / n
    bh = 210
    top = 250
    centers = []
    for i, label in enumerate(FLOW):
        x = x0 + i * (bw + gap)
        cx = x + bw / 2
        centers.append(cx)
        emph = (i == n - 1)
        s.append(rrect(x, top, bw, bh, 18,
                       GAP_FILL if emph else PANEL,
                       CYAN if emph else STROKE, 3 if emph else 2))
        s.append(txt(x + 24, top + 44, "0" + str(i + 1), 22,
                     CYAN if emph else MUTED, True))
        L.append(label)
        lines = wrap(label, 25, bw - 44, emph)
        assert len(lines) <= 4, (label, lines)
        cy = top + bh / 2 - (len(lines) - 1) * 17 + 24
        for ln in lines:
            s.append(txt(cx, cy, ln, 25,
                         HEAD if emph else BODY, emph, "middle"))
            cy += 34
        if i < n - 1:
            ax = x + bw
            s.append(arrow(ax + 10, top + bh / 2, ax + gap - 10,
                           top + bh / 2, CYAN, 3, size=12))

    # crimson security-boundary chip under stage 4 (access control)
    note = ("access is a security boundary — the code chooses where, "
            "the model chooses what")
    L.append(note)
    ncx = centers[3]
    ny, nw, nh = 560, 1120, 150
    nx = min(max(ncx - nw / 2, 60), 1840 - nw)
    s.append(line(ncx, top + bh, ncx, ny, CRIMSON, 2, dash="6 7"))
    s.append(rrect(nx, ny, nw, nh, 18, WARM, CRIMSON, 2.5))
    s.append(txt(nx + 34, ny + 44, "ACCESS = SECURITY BOUNDARY", 20,
                 CRIMSON, True))
    nlines = wrap(note, 26, nw - 68, True)
    assert len(nlines) <= 2, nlines
    cy = ny + 90
    for ln in nlines:
        s.append(txt(nx + 34, cy, ln, 26, HEAD, True))
        cy += 36

    return emit("data-foundation", "".join(s), h=820), L


# ============================================================ 6. maturity model ==
STAGES = [
    ("Ad hoc",   "shadow AI, no owner"),
    ("Piloting", "isolated wins, no governance"),
    ("Governed", "policy · MRM + agent layer · CoE"),
    ("Scaled",   "platform · federated delivery · measured value"),
    ("AI-first", "agentic workflows end to end · governance embedded "
                 "· judgment is the moat"),
]


def maturity_model():
    L = []
    title = "AI & agent capability maturity"
    L.append(title)
    s = [heading(title, y=104)]

    n = len(STAGES)
    x0, gap = 64, 20
    bw = (1780 - gap * (n - 1)) / n
    bh = 300
    base_bottom = 858
    rise = 62
    prev = None
    for i, (name, desc) in enumerate(STAGES):
        x = x0 + i * (bw + gap)
        cx = x + bw / 2
        bottom = base_bottom - i * rise
        y = bottom - bh
        emph = (i == n - 1)
        # ascending connector from previous box
        if prev is not None:
            s.append(arrow(prev[0], prev[1], x - 8, y + 40, CYAN, 3, size=11))
        prev = (x + bw + 8, y + 40)
        s.append(rrect(x, y, bw, bh, 18,
                       GAP_FILL if emph else PANEL,
                       CYAN if emph else STROKE, 3 if emph else 2))
        # number badge
        s.append('<circle cx="%.1f" cy="%.1f" r="26" fill="none" stroke="%s" '
                 'stroke-width="2.5"/>' % (x + 44, y + 48, CYAN))
        s.append(txt(x + 44, y + 57, str(i + 1), 26, CYAN, True, "middle"))
        fit(name, 28, bw - 100, True, "stage name")
        s.append(txt(x + 84, y + 57, name, 28, HEAD, True))
        L.append(str(i + 1) + " " + name)
        L.append(desc)
        lines = wrap(desc, 21, bw - 48)
        assert len(lines) <= 5, (name, lines)
        cy = y + 118
        for ln in lines:
            s.append(txt(x + 24, cy, ln, 21, BODY))
            cy += 30

    # reality-check caption
    cap = "Most firms are at 1–2 and think they're at 3."
    L.append(cap)
    cw = text_w(cap, 27, True) + 80
    cx = (x0 + 1780 + x0) / 2 - cw / 2 + 60
    s.append(rrect(cx, 912, cw, 74, 37, WARM, CRIMSON, 2.5))
    s.append(txt(cx + cw / 2, 958, cap, 27, HEAD, True, "middle"))

    return emit("maturity-model", "".join(s), h=1030), L


# ================================================================= 7. roadmap ==
PHASES = [
    ("DAYS 0–90", "Foundations",
     ["name an accountable owner", "stand up governance + CoE",
      "pick 2 no-regrets use cases", "baseline data"]),
    ("QUARTERS 2–4", "Governed scale",
     ["platform", "shadow-mode rollout", "tiered training", "scorecards"]),
    ("YEAR 2+", "AI-first",
     ["agentic workflows", "federated delivery", "incentives hardwired"]),
]


def roadmap():
    L = []
    title = "From bet to AI-first — the roadmap"
    L.append(title)
    s = [heading(title, y=104)]

    n = len(PHASES)
    x0, gap = 60, 44
    pw = (1780 - gap * (n - 1)) / n
    top, ph = 210, 470
    for i, (kick, name, items) in enumerate(PHASES):
        x = x0 + i * (pw + gap)
        emph = (i == n - 1)
        s.append(rrect(x, top, pw, ph, 20,
                       GAP_FILL if emph else PANEL,
                       CYAN if emph else STROKE, 3 if emph else 2))
        fit(kick, 24, pw - 72, True, "phase kicker")
        s.append(txt(x + 36, top + 60, kick, 24, CYAN, True))
        L.append(kick)
        fit(name, 34, pw - 72, True, "phase name")
        s.append(txt(x + 36, top + 108, name, 34, HEAD, True))
        L.append(name)
        s.append(line(x + 36, top + 132, x + pw - 36, top + 132,
                      BAND_STROKE, 1.5))
        iy = top + 186
        for it in items:
            s.append(check(x + 40, iy - 18, 22, CYAN))
            fit(it, 24, pw - 110, False, "roadmap item")
            s.append(txt(x + 82, iy, it, 24, BODY))
            L.append(it)
            iy += 62
        # progression arrow between panels
        if i < n - 1:
            s.append(arrow(x + pw + 8, top + ph / 2, x + pw + gap - 8,
                           top + ph / 2, CYAN, 3, size=12))

    # the spanning "sponsored from the top" arrow
    ay = top + ph + 96
    s.append(arrow(x0, ay, x0 + 1780, ay, CYAN, 3.5, size=13))
    span = "sponsored from the top, embedded in the operating model"
    L.append(span)
    sw_ = text_w(span, 25, True) + 72
    scx = x0 + 890
    s.append(rrect(scx - sw_ / 2, ay - 34, sw_, 68, 34, GAP_FILL, CYAN, 2.5))
    s.append(txt(scx, ay + 9, span, 25, HEAD, True, "middle"))

    return emit("roadmap", "".join(s), h=820), L


# ================================================ 8. board oversight roadmap ==
# A GOVERNANCE CADENCE (not an execution plan): four quarters of what the board
# APPROVES and the artifacts it INSPECTS. Distinct from the firm-level roadmap.
BOARD_QUARTERS = [
    ("Q1", "Set the appetite", [
        "approve the AI risk appetite",
        "charter a named oversight committee",
        "require the use-case inventory + risk register",
    ]),
    ("Q2", "Inspect the evidence", [
        "review shadow-mode results + model inventory",
        "approve the agentic-AI policy",
        "confirm the agentic-AI gap is covered",
    ]),
    ("Q3", "Govern the first go-live", [
        "approve the first narrow go-live",
        "review the incident log",
        "review the adoption + spend report",
    ]),
    ("Q4", "Reset the appetite", [
        "benchmark to NIST AI RMF",
        "reset the AI risk appetite",
        "approve the next-year plan",
    ]),
]


def board_oversight_roadmap():
    L = []
    title = "The board's first-year oversight"
    sub = "governing the bet is a fiduciary duty, not a technology update"
    L.append(title)
    L.append(sub)
    s = [heading(title, sub, y=100)]

    # crimson callout chip, top-right
    chip = "the board inspects artifacts, not adjectives"
    L.append(chip)
    cw = text_w(chip, 22, True) + 56
    s.append(rrect(1840 - cw, 70, cw, 48, 24, WARM, CRIMSON, 2.5))
    s.append(txt(1840 - cw / 2, 70 + 32, chip, 22, HEAD, True, "middle"))

    n = len(BOARD_QUARTERS)
    x0, gap = 60, 36
    bw = (1780 - gap * (n - 1)) / n
    top, ph = 210, 592
    for i, (q, name, items) in enumerate(BOARD_QUARTERS):
        x = x0 + i * (bw + gap)
        s.append(rrect(x, top, bw, ph, 20, PANEL, STROKE, 2))
        fit(q, 24, 120, True, "board quarter kicker")
        s.append(txt(x + 34, top + 58, q, 24, CYAN, True))
        L.append(q)
        fit(name, 25, bw - 68, True, "board quarter name")
        s.append(txt(x + 34, top + 104, name, 25, HEAD, True))
        L.append(name)
        s.append(line(x + 34, top + 126, x + bw - 34, top + 126,
                      BAND_STROKE, 1.5))
        stack, _ = chip_stack(x + 22, top + 150, bw - 44, items,
                              chip_h=118, gap=24, size=20, tpad=16,
                              where="board Q%d chip" % (i + 1))
        s.append(stack)
        L += items
        if i < n - 1:
            s.append(arrow(x + bw + 6, top + ph / 2, x + bw + gap - 6,
                           top + ph / 2, MUTED, 2.5, size=9))

    # spanning cadence arrow beneath all four quarters
    ay = top + ph + 86
    s.append(arrow(x0, ay, x0 + 1780, ay, CYAN, 3, size=13))
    span = "governance cadence — set risk appetite, then inspect the evidence"
    L.append(span)
    sw_ = text_w(span, 24, True) + 72
    scx = x0 + 890
    s.append(rrect(scx - sw_ / 2, ay - 33, sw_, 66, 33, GAP_FILL, CYAN, 2.5))
    s.append(txt(scx, ay + 9, span, 24, HEAD, True, "middle"))

    return emit("board-oversight-roadmap", "".join(s), h=1000), L


# ================================================ 9. CEO first-year roadmap ==
# An EXECUTION SEQUENCE (not an oversight cadence): five phases the accountable
# executive drives, ascending left-to-right like the maturity climb.
CEO_PHASES = [
    ("1", "Days 0–30", [
        "name one accountable owner",
        "charter the Center of Enablement",
        "publish the two policies",
    ]),
    ("2", "Days 30–90", [
        "pick 2 no-regrets use cases",
        "baseline the data",
        "start shadow mode",
    ]),
    ("3", "Q2", [
        "first governed go-live, one slice",
        "stand up the program dashboard",
        "publish the scorecards",
    ]),
    ("4", "Q3", [
        "expand to 2-3 domains (federated)",
        "tie comp to adoption",
    ]),
    ("5", "Q4", [
        "scale what works, kill what doesn't",
        "report outcomes to the board",
    ]),
]


def ceo_first_year_roadmap():
    L = []
    title = "The CEO's first year"
    sub = "the first-year execution sequence, owned by one executive"
    L.append(title)
    L.append(sub)
    s = [heading(title, sub, y=100)]

    # cyan callout chip, top-right
    chip = "one owner chairs the steering committee"
    L.append(chip)
    cw = text_w(chip, 22, True) + 56
    s.append(rrect(1840 - cw, 70, cw, 48, 24, CHIP_FILL, CYAN, 2))
    s.append(txt(1840 - cw / 2, 70 + 32, chip, 22, CYAN, True, "middle"))

    n = len(CEO_PHASES)
    x0, gap = 64, 20
    bw = (1780 - gap * (n - 1)) / n
    bh, rise, base_bottom = 420, 58, 908
    prev = None
    for i, (num, name, items) in enumerate(CEO_PHASES):
        x = x0 + i * (bw + gap)
        bottom = base_bottom - i * rise
        y = bottom - bh
        if prev is not None:
            s.append(arrow(prev[0], prev[1], x - 8, y + 44, CYAN, 3, size=11))
        prev = (x + bw + 8, y + 44)
        s.append(rrect(x, y, bw, bh, 20, PANEL, STROKE, 2))
        s.append('<circle cx="%.1f" cy="%.1f" r="21" fill="none" '
                 'stroke="%s" stroke-width="2.5"/>' % (x + 38, y + 44, CYAN))
        s.append(txt(x + 38, y + 52, num, 22, CYAN, True, "middle"))
        fit(name, 24, bw - 100, True, "ceo phase name")
        s.append(txt(x + 72, y + 53, name, 24, HEAD, True))
        L.append(name)
        s.append(line(x + 22, y + 78, x + bw - 22, y + 78, BAND_STROKE, 1.5))
        stack, _ = chip_stack(x + 16, y + 100, bw - 32, items,
                              chip_h=88, gap=12, size=19, tpad=15,
                              where="ceo phase %d chip" % (i + 1))
        s.append(stack)
        L += items

    # spanning sponsorship arrow beneath the climb
    ay = base_bottom + 58
    s.append(arrow(x0, ay, x0 + 1780, ay, CYAN, 3, size=13))
    span = "sponsored from the top, owned by one executive"
    L.append(span)
    sw_ = text_w(span, 24, True) + 72
    scx = x0 + 890
    s.append(rrect(scx - sw_ / 2, ay - 33, sw_, 66, 33, GAP_FILL, CYAN, 2.5))
    s.append(txt(scx, ay + 9, span, 24, HEAD, True, "middle"))

    return emit("ceo-first-year-roadmap", "".join(s), h=1040), L


# ============================================== 10. the governance spine ==
# Reconciles the single-owner rule with the firm-wide steering committee:
# three tiers (board -> steering committee -> delivery), the committee CHAIRED
# by the one accountable owner, with the down/up flows named on each seam.
COMM_ROW1 = ["Business-line heads", "Risk · CRO", "Compliance · CCO",
             "Data · CDO"]
COMM_ROW2 = ["Security · CISO", "Talent · CHRO", "Legal · GC",
             "Enablement lead"]
SPOKE_UNITS = ["Distribution", "Operations", "Investments"]


def governance_spine():
    L = []
    title = "The governance spine"
    sub = ("how a firm-wide AI program is steered — board, steering committee, "
           "and delivery")
    s = [heading(title, sub, y=100)]
    L += [title, sub]

    # reconciliation callout, top-right (crimson)
    chip = "a committee to steer — one person to answer"
    cw = text_w(chip, 22, True) + 56
    s.append(rrect(1840 - cw, 64, cw, 48, 24, WARM, CRIMSON, 2.5))
    s.append(txt(1840 - cw / 2, 64 + 32, chip, 22, HEAD, True, "middle"))
    L.append(chip)

    cx = 950

    def seam(y_top, y_bot, down, up):
        out = [arrow(cx, y_top, cx, y_bot, CYAN, 3, double=True, size=12)]
        my = (y_top + y_bot) / 2 + 6
        fit(down, 20, 380, False, "seam down"); fit(up, 20, 380, False, "seam up")
        out.append(txt(cx - 42, my, down, 20, MUTED, False, "end"))
        out.append(txt(cx + 42, my, up, 20, MUTED, False, "start"))
        L.append(down); L.append(up)
        return "".join(out)

    # ---- Tier 1: the board
    bw, bh = 760, 116
    bx, by = cx - bw / 2, 206
    s.append(rrect(bx, by, bw, bh, 18, PANEL, STROKE, 2))
    s.append(txt(cx, by + 50, "THE BOARD", 30, HEAD, True, "middle"))
    t1 = "designated oversight committee · quarterly"
    fit(t1, 22, bw - 60, False, "board sub")
    s.append(txt(cx, by + 86, t1, 22, CYAN, False, "middle"))
    L += ["THE BOARD", t1]

    # seam 1
    s.append(seam(by + bh + 6, 430 - 6,
                  "down · appetite & mandate", "up · assurance & evidence"))

    # ---- Tier 2: the steering committee (the hero)
    kw, kh = 1240, 336
    kx, ky = cx - kw / 2, 430
    s.append(rrect(kx, ky, kw, kh, 20, GAP_FILL, CYAN, 3))
    ct = "THE AI STEERING COMMITTEE"
    fit(ct, 32, kw - 80, True, "committee title")
    s.append(txt(cx, ky + 58, ct, 32, HEAD, True, "middle"))
    csub = "chaired by the single accountable AI owner · meets monthly"
    fit(csub, 22, kw - 80, False, "committee sub")
    s.append(txt(cx, ky + 94, csub, 22, CYAN, False, "middle"))
    L += [ct, csub]
    s.append(line(kx + 40, ky + 118, kx + kw - 40, ky + 118, BAND_STROKE, 1.5))
    s.append(chip_row(kx, ky + 140, kw, 60, COMM_ROW1, size=20, pad=28, gap=16,
                      where="committee member"))
    s.append(chip_row(kx, ky + 212, kw, 60, COMM_ROW2, size=20, pad=28, gap=16,
                      where="committee member"))
    L += COMM_ROW1 + COMM_ROW2
    note = "+ bridge leaders & practitioner voices, brought in as the work needs"
    fit(note, 20, kw - 80, False, "committee note")
    s.append(txt(cx, ky + kh - 24, note, 20, MUTED, False, "middle"))
    L.append(note)

    # seam 2
    s.append(seam(ky + kh + 6, 876 - 6,
                  "down · priorities & go/no-go", "up · findings & scorecards"))

    # ---- Tier 3: delivery (hub + business spokes)
    dw, dh = 1240, 176
    dx, dy = cx - dw / 2, 876
    s.append(rrect(dx, dy, dw, dh, 20, PANEL, STROKE, 2))
    s.append(txt(cx, dy + 44, "DELIVERY", 26, HEAD, True, "middle"))
    dsub = "the hub sets the standards & platform · the business spokes build on it"
    fit(dsub, 20, dw - 80, False, "delivery sub")
    s.append(txt(cx, dy + 74, dsub, 20, MUTED, False, "middle"))
    L += ["DELIVERY", dsub]
    # hub chip (cyan) on the left
    hcw = 300
    hx, hyy = dx + 28, dy + 96
    s.append(rrect(hx, hyy, hcw, 60, 12, CHIP_FILL, CYAN, 2))
    s.append(txt(hx + hcw / 2, hyy + 38, "Center of Enablement", 19, HEAD,
                 True, "middle"))
    L.append("Center of Enablement")
    # three business spokes on the right
    s.append(chip_row(hx + hcw + 12, hyy, dw - hcw - 68, 60, SPOKE_UNITS,
                      size=20, pad=8, gap=16, where="spoke unit"))
    L += SPOKE_UNITS

    return emit("governance-spine", "".join(s), h=1112), L


# ============================================ 11. personas: toil -> judgment ==
# The seven personas from doc 04 as a before/after matrix. Reinforces the
# through-line: the agent fetches, drafts, and watches; the human keeps the call.
PERSONAS = [
    ("Advisor", "relationship manager",
     "evenings lost to prep, notes, and CRM hygiene",
     "prep and follow-up drafted — hours go to the client"),
    ("Portfolio manager", "analyst",
     "days gathering and synthesizing before the thinking starts",
     "synthesis on tap; broader coverage, sharper calls"),
    ("Operations", "specialist",
     "high-volume, repetitive intake and reconciliation",
     "supervising exceptions, not processing the routine"),
    ("Compliance", "officer",
     "sampling a fraction of activity by hand",
     "anomalies surfaced across the whole population"),
    ("Client service", "associate",
     "the same routine questions, over and over",
     "routine handled; freed for the sensitive call"),
    ("Technologist", "builder",
     "pressure to ship the impressive demo",
     "governance-by-design, built in as the craft"),
    ("Executive", "leader",
     "managing by anecdote and dashboard",
     "reads the scorecard, asks the right question"),
]


def personas_before_after():
    L = []
    title = "The personas — from toil to judgment"
    sub = ("the agent fetches, drafts, and watches; the human keeps the "
           "decision and the accountability")
    s = [heading(title, sub, y=100)]
    L += [title, sub]

    px, pw = 60, 340                    # persona column
    ax = 60 + pw + 24                   # before column start
    aw = 700                            # before column width
    bx = ax + aw + 96                   # after column start (gap holds arrow)
    bw = 1840 - bx                      # after column width
    top = 232
    rh, gap = 116, 12

    # column headers
    s.append(txt(px + 20, top - 16, "PERSONA", 20, MUTED, True))
    s.append(txt(ax + 24, top - 16, "BEFORE · THE TOIL", 20, CRIMSON, True))
    s.append(txt(bx + 24, top - 16, "AFTER · THE JUDGMENT", 20, CYAN, True))
    L += ["BEFORE · THE TOIL", "AFTER · THE JUDGMENT"]

    for i, (name, qual, before, after) in enumerate(PERSONAS):
        y = top + i * (rh + gap)
        # persona chip
        s.append(rrect(px, y, pw, rh, 14, PANEL, STROKE, 2))
        fit(name, 26, pw - 44, True, "persona name")
        s.append(txt(px + 24, y + 50, name, 26, HEAD, True))
        fit(qual, 20, pw - 44, False, "persona qualifier")
        s.append(txt(px + 24, y + 82, qual, 20, MUTED))
        L += [name, qual]
        # before panel (warm/crimson)
        s.append(rrect(ax, y, aw, rh, 14, WARM, CRIMSON, 1.6))
        bl = wrap(before, 23, aw - 48)
        if len(bl) > 2:
            raise ValueError("before too long: %r -> %r" % (before, bl))
        by = y + rh / 2 - (len(bl) - 1) * 16 + 8
        for ln in bl:
            s.append(txt(ax + 24, by, ln, 23, BODY))
            by += 32
        L.append(before)
        # arrow across the gap
        s.append(arrow(ax + aw + 14, y + rh / 2, bx - 14, y + rh / 2,
                       CYAN, 3, size=11))
        # after panel (cyan chip)
        s.append(rrect(bx, y, bw, rh, 14, CHIP_FILL, CYAN, 1.6))
        al = wrap(after, 23, bw - 48, True)
        if len(al) > 2:
            raise ValueError("after too long: %r -> %r" % (after, al))
        ay = y + rh / 2 - (len(al) - 1) * 16 + 8
        for ln in al:
            s.append(txt(bx + 24, ay, ln, 23, HEAD, True))
            ay += 32
        L.append(after)

    # footer motif
    fy = top + len(PERSONAS) * (rh + gap) + 42
    s.append(arrow(px, fy, 1840, fy, CYAN, 3, size=13))
    span = "in every case: the agent augments the person and escalates the hard call"
    L.append(span)
    sw_ = text_w(span, 24, True) + 72
    scx = 950
    s.append(rrect(scx - sw_ / 2, fy - 33, sw_, 66, 33, GAP_FILL, CYAN, 2.5))
    s.append(txt(scx, fy + 9, span, 24, HEAD, True, "middle"))

    return emit("personas-before-after", "".join(s), h=1200), L


ALL = [four_audiences, value_and_shifts, governance_stack,
       target_operating_model, data_foundation, maturity_model, roadmap,
       board_oversight_roadmap, ceo_first_year_roadmap, governance_spine,
       personas_before_after]

if __name__ == "__main__":
    for fn in ALL:
        print(fn.__name__)
        fn()
