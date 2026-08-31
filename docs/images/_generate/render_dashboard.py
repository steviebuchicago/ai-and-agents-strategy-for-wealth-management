#!/usr/bin/env python3
"""Render the executive dashboard HTML to a crisp PNG using headless Chromium."""
import os, pathlib
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent.parent.parent  # docs/images/_generate -> repo root
SRC = REPO / "playbooks" / "ai-program-dashboard.html"
OUT = REPO / "docs" / "images" / "program-dashboard.png"

CHROMIUM = "/opt/pw-browsers/chromium"

with sync_playwright() as p:
    browser = p.chromium.launch(
        executable_path=CHROMIUM if os.path.exists(CHROMIUM) else None,
        args=["--force-color-profile=srgb", "--hide-scrollbars"],
    )
    page = browser.new_page(viewport={"width": 1360, "height": 1200}, device_scale_factor=2)
    page.goto(SRC.as_uri())
    page.wait_for_timeout(500)
    # Full-page shot captures the whole document height at 2x
    page.screenshot(path=str(OUT), full_page=True)
    browser.close()

print("wrote", OUT, OUT.stat().st_size, "bytes")
