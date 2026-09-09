#!/usr/bin/env python3
"""
build_site.py — generate the five website pages from canonical.json
====================================================================
The single source of truth is:

    vault/KNOWLEDGE/specs/canonical.json

This script renders the templates under `site/templates/` into the live pages
at the repo root. The templates carry the design and bespoke copy; the facts
(phone, email, city, tagline, founder, ventures) are injected from the JSON.

    python3 tools/build_site.py              # regenerate all five pages
    python3 tools/build_site.py --extract    # re-tokenize the live HTML -> templates

Zero dependencies (Python 3.9+). Idempotent — safe to run any time.

Do NOT hand-edit the generated `*.html` facts. Edit `canonical.json` (facts)
or `site/templates/*.html` (copy/design), then run this script.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPEC = ROOT / "vault" / "KNOWLEDGE" / "specs" / "canonical.json"
TPL_DIR = ROOT / "site" / "templates"
PAGES = ["index.html", "holdings.html", "tech.html", "about.html", "contact.html"]

BANNER = (
    "<!-- GENERATED FILE — do not edit by hand.\n"
    "     Source of truth: vault/KNOWLEDGE/specs/canonical.json\n"
    "     Edit site/templates/ + run:  python3 tools/build_site.py -->"
)

TOKEN_RE = re.compile(r"\{\{([A-Z0-9_]+)\}\}")


# ----------------------------------------------------------------------
# Render: token -> value, derived from canonical.json
# ----------------------------------------------------------------------
def _values(data):
    f = data["founder"]
    c = data["contact"]
    v = data["ventures"]
    vals = {
        "TAGLINE": data["brand"]["tagline"],
        "PHONE": c["phone"],
        "PHONE_TEL": c["phone_tel"],
        "EMAIL": c["email"],
        "CITY": f["based_in"].split("\u00b7")[0].strip(),
        "CITY_TZ": f["based_in"],
        "FOUNDER_NAME": f["preferred_name"].split(" (")[0],
        "FOUNDER_QUOTE": f["standard_quote"],
    }
    for i, venture in enumerate(v):
        vals["V%d_NAME" % i] = venture["name"]
        vals["V%d_SECTOR" % i] = venture.get("sector", venture["type"])
    return vals


def render(template, vals):
    def sub(m):
        key = m.group(1)
        if key not in vals:
            raise KeyError("Unknown token in template: {{%s}}" % key)
        return vals[key]
    return TOKEN_RE.sub(sub, template)


# ----------------------------------------------------------------------
# Extract: the live HTML -> templates (find facts, write tokens)
# Ordered so longer/more-specific literals are matched first.
# ----------------------------------------------------------------------
EXTRACT_PAIRS = [
    ("Columbus, Ohio · Eastern Time", "{{CITY_TZ}}"),
    ("Columbus, Ohio", "{{CITY}}"),
    ("(202) 276-0500", "{{PHONE}}"),
    ("+12022760500", "{{PHONE_TEL}}"),
    ("Taytaylor70@gmail.com", "{{EMAIL}}"),
    ("Building Legacy. Creating Value. Engineering the Future.", "{{TAGLINE}}"),
    ("I love anything Technology, Fast, seductive, grown and sexy, as well as "
     "having determination for the making of greatness.", "{{FOUNDER_QUOTE}}"),
    ("L. Taylor III", "{{FOUNDER_NAME}}"),
    # venture names (plain, unambiguous)
    ("The Taylor Dynasty Holdings LLC", "{{V0_NAME}}"),
    ("Oasis Marketplace", "{{V1_NAME}}"),
    ("DogSphere", "{{V2_NAME}}"),
    ("Taylor Made Real Estate", "{{V3_NAME}}"),
    ("The Nephew's First Business™", "{{V4_NAME}}"),
    ("The Taylor Edition", "{{V5_NAME}}"),
    # sector labels (only when they sit between tag boundaries, to avoid prose)
    (">The Parent<", ">{{V0_SECTOR}}<"),
    (">Commerce<", ">{{V1_SECTOR}}<"),
    (">Pet Ecosystem<", ">{{V2_SECTOR}}<"),
    (">Property<", ">{{V3_SECTOR}}<"),
    (">Legacy<", ">{{V4_SECTOR}}<"),
    (">AI · Software<", ">{{V5_SECTOR}}<"),
]


def extract(template):
    for find, token in EXTRACT_PAIRS:
        template = template.replace(find, token)
    return template


def _add_banner(html):
    if BANNER.splitlines()[0] in html:
        return html
    return html.replace("<!DOCTYPE html>\n", "<!DOCTYPE html>\n" + BANNER + "\n", 1)


def main():
    with open(SPEC, "r", encoding="utf-8") as fh:
        data = json.load(fh)

    if "--extract" in sys.argv:
        for page in PAGES:
            src = ROOT / page
            out = TPL_DIR / page
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(extract(src.read_text(encoding="utf-8")), encoding="utf-8")
            print("template ->", out.relative_to(ROOT))
        print("\nTemplates extracted. Now run `python3 tools/build_site.py` to regenerate.")
        return

    vals = _values(data)
    for page in PAGES:
        tpl = TPL_DIR / page
        if not tpl.is_file():
            raise SystemExit("Missing template: %s" % tpl)
        rendered = render(tpl.read_text(encoding="utf-8"), vals)
        (ROOT / page).write_text(_add_banner(rendered), encoding="utf-8")
        print("wrote", page)
    print("\nDone. The five pages are in sync with canonical.json.")


if __name__ == "__main__":
    main()
