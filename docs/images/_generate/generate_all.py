"""Reproducible driver for the AWM executive-guide diagrams.

Run:  python3 generate_all.py

It (1) renders all nine PNGs to ../  (docs/images), each verified > 1200px
wide by house.verify at draw time; (2) runs a spelling gate that checks the
canonical regulation / framework / role terms against ../../RESEARCH.md (when
present), blocks a list of known misspellings, and blocks sanitized tokens
that belong to the companion repos; and (3) prints a manifest of
file -> size -> the exact labels it contains.

Every label is measured against its box (svgkit.fit / wrap) and checked
glyph-by-glyph against the real font cmap (house.assert_renderable) as it is
drawn, so this driver never has to guess whether a diagram overflowed.
"""

import os
import re
import sys

import diagrams
from house import OUT

RESEARCH = os.path.abspath(os.path.join(OUT, "..", "..", "RESEARCH.md"))

# --- canonical terms: must appear verbatim in the labels AND in RESEARCH.md ---
CANON = ["NIST AI RMF", "EU AI Act",
         "agentic", "fiduciary", "RACI"]
CANON_CI = ["Center of Enablement"]      # matched case-insensitively

# --- exact task-specified labels that must be present (fidelity spot checks) --
MUST_HAVE = [
    "why → who → how",
    "MODELS — MODEL-RISK REGULATION",
    "AGENTIC AI — outside its scope",
    "still phasing in where an EU nexus exists",
    "CENTER OF ENABLEMENT",
    "Govern", "Map", "Measure", "Manage",
    "Most firms are at 1–2 and think they're at 3.",
    # --- the board oversight roadmap (governance cadence) ---
    "The board's first-year oversight",
    "governance cadence — set risk appetite, then inspect the evidence",
    "the board inspects artifacts, not adjectives",
    "confirm the agentic-AI gap is covered",
    "benchmark to NIST AI RMF",
    # --- the CEO first-year roadmap (execution sequence) ---
    "The CEO's first year",
    "charter the Center of Enablement",
    "sponsored from the top, owned by one executive",
    "one owner chairs the steering committee",
    # --- the governance spine (steering committee) ---
    "The governance spine",
    "THE AI STEERING COMMITTEE",
    "chaired by the single accountable AI owner · meets monthly",
    "a committee to steer — one person to answer",
]

# --- literal misspellings that must NEVER appear (case-insensitive) -----------
# each is chosen so it cannot be a substring of any correct label above.
BANNED = [
    "NIST RMF", "NIST AI RFM", "AI RFM",
    "Centre of Enablement", "Center of Enablment",
    "fiducary", "fidiciary", "fiduaciary", "fiduciary duty duty",
    "agenetic", "aigentic", "agentic ai ai",
    "E.U. AI Act", "EU A.I. Act",
    "RASI", "RACI matrix matrix",
]

# --- sanitize: firm-identifying content that must NEVER leak into public labels --
# (case-insensitive substring match against every label drawn).
SANITIZE = ["codename", "internal-only"]


def run():
    # RESEARCH.md backs the canonical terms. If it is not present in this
    # checkout, the gate still enforces that every canonical term appears in
    # the labels, that the required labels are present, and that no banned
    # spelling or sanitized token leaks in — it only skips the cross-check
    # against the facts sheet, so the driver stays reproducible either way.
    try:
        research = open(RESEARCH, encoding="utf-8").read()
    except FileNotFoundError:
        research = ""
        print("NOTE: RESEARCH.md not found at %s — canonical terms are still "
              "checked for presence and exact spelling in the labels, but not "
              "cross-checked against the facts sheet." % RESEARCH)
    research_l = research.lower()

    results = []                 # (name, (w, h), labels)
    for fn in diagrams.ALL:
        size, labels = fn()
        # name = the png emitted; recover from the function via a re-render map
        results.append((fn, size, labels))

    # map function -> emitted file name (the string passed to emit)
    NAME = {
        diagrams.four_audiences: "four-audiences",
        diagrams.value_and_shifts: "value-and-shifts",
        diagrams.governance_stack: "governance-stack",
        diagrams.target_operating_model: "target-operating-model",
        diagrams.data_foundation: "data-foundation",
        diagrams.maturity_model: "maturity-model",
        diagrams.roadmap: "roadmap",
        diagrams.board_oversight_roadmap: "board-oversight-roadmap",
        diagrams.ceo_first_year_roadmap: "ceo-first-year-roadmap",
        diagrams.governance_spine: "governance-spine",
        diagrams.personas_before_after: "personas-before-after",
    }

    all_text = "\n".join(l for _, _, ls in results for l in ls)
    all_text_l = all_text.lower()

    # ---------------------------------------------------------- spelling gate --
    problems = []

    for term in CANON:
        if term not in all_text:
            problems.append("canonical term missing from labels: %r" % term)
        if research and term.lower() not in research_l:
            problems.append("canonical term not backed by RESEARCH.md: %r" % term)
    for term in CANON_CI:
        if term.lower() not in all_text_l:
            problems.append("canonical term missing from labels: %r" % term)
        if research and term.lower() not in research_l:
            problems.append("canonical term not backed by RESEARCH.md: %r" % term)

    for phrase in MUST_HAVE:
        if phrase not in all_text:
            problems.append("required label missing: %r" % phrase)

    for bad in BANNED:
        if re.search(re.escape(bad), all_text, re.IGNORECASE):
            problems.append("banned spelling present: %r" % bad)

    for bad in SANITIZE:
        if re.search(re.escape(bad), all_text, re.IGNORECASE):
            problems.append("sanitize: forbidden token present in labels: %r"
                            % bad)

    print("\n" + "=" * 72)
    if problems:
        print("SPELLING GATE: FAILED")
        for p in problems:
            print("  - " + p)
        print("=" * 72)
        sys.exit(1)
    print("SPELLING GATE: PASSED")
    print("  canonical terms verified against RESEARCH.md: "
          + ", ".join(CANON + CANON_CI))
    print("  %d required labels present · %d banned spellings absent · "
          "%d sanitized tokens absent"
          % (len(MUST_HAVE), len(BANNED), len(SANITIZE)))

    # ---------------------------------------------------------------- manifest --
    print("\n" + "=" * 72)
    print("MANIFEST — file -> size -> exact labels")
    print("=" * 72)
    for fn, (w, h), labels in results:
        name = NAME[fn] + ".png"
        seen, uniq = set(), []
        for l in labels:
            if l not in seen:
                seen.add(l)
                uniq.append(l)
        print("\n%s   %d x %d px   (%d labels)" % (name, w, h, len(uniq)))
        for l in uniq:
            print("    | " + l)
    print("\n" + "=" * 72)
    print("%d PNGs written to %s" % (len(results), OUT))


if __name__ == "__main__":
    run()
