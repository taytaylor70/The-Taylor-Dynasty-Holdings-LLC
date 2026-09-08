#!/usr/bin/env python3
"""
build_specs.py — regenerate the markdown specs from canonical.json
===================================================================
The single source of truth is:

    vault/KNOWLEDGE/specs/canonical.json

This script renders it into the human-readable markdown specs that live
alongside it. Do NOT hand-edit the generated markdown — change the JSON, then
run this:

    python3 tools/build_specs.py

Zero dependencies (Python 3.9+). Idempotent — safe to run any time.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPEC_DIR = ROOT / "vault" / "KNOWLEDGE" / "specs"
CANONICAL_JSON = SPEC_DIR / "canonical.json"

GENERATED_NOTE = (
    "<!-- GENERATED FILE — do not edit by hand.\n"
    "     Source of truth: vault/KNOWLEDGE/specs/canonical.json\n"
    "     Regenerate with:  python3 tools/build_specs.py -->\n"
)


def _table(rows):
    """Render a list of rows (first is the header) as a markdown table."""
    header = rows[0]
    out = ["| " + " | ".join(header) + " |"]
    out.append("|" + "|".join(["---"] * len(header)) + "|")
    for row in rows[1:]:
        cells = [str(c).replace("|", "\\|") for c in row]
        out.append("| " + " | ".join(cells) + " |")
    return "\n".join(out)


def build_house_facts(data):
    f = data["founder"]
    m = data["meta"]
    lines = [
        "---",
        "name: canonical-house-facts",
        "slug: canonical-house-facts",
        "status: canonical",
        "owner: L. Taylor III",
        "updated: {}".format(m["updated"]),
        "---",
        "",
        GENERATED_NOTE,
        "# Canonical House Facts",
        "",
        "> **Canonical.** The website (`index.html`, `holdings.html`, `tech.html`,",
        "> `about.html`, `contact.html`) and the MCP server (`mcp/server.py`) are",
        "> generated from `canonical.json`. If they disagree, the JSON wins.",
        "> Change it here first, then update the projections.",
        "",
        "## Founder",
        "",
        _table([
            ["Field", "Value"],
            ["Preferred name", f["preferred_name"]],
            ["Role", f["role"]],
            ["Based in", f["based_in"]],
            ["Roots", f["roots"]],
            ["Generation", f["generation"]],
            ["Education (public record)",
             " · ".join(f["education_public"])],
            ["Standard quote", f["standard_quote"]],
            ["Story (short)", f["story_short"]],
        ]),
        "",
        "## Ventures",
        "",
        _table(
            [["Name", "Type", "Status", "Summary"]]
            + [[v["name"], v["type"], v["status"], v["summary"]]
               for v in data["ventures"]]
        ),
        "",
        "## Capabilities",
        "",
        _table(
            [["Capability", "Description"]]
            + [[c["name"], c["description"]] for c in data["capabilities"]]
        ),
        "",
        "### Built for (audience)",
        "",
    ]
    for a in data["audience"]:
        lines.append("- " + a)
    lines += [
        "",
        "## Career timeline",
        "",
        _table(
            [["Span", "Organization", "Note"]]
            + [[c["span"], c["org"], c["note"]] for c in data["career"]]
        ),
        "",
        "## Contact",
        "",
        _table([
            ["Field", "Value"],
            ["Cell", data["contact"]["cell"]],
            ["Email", data["contact"]["email"]],
            ["Hours", data["contact"]["hours"]],
            ["Philosophy", data["contact"]["philosophy"]],
        ]),
        "",
        "## Site map",
        "",
        _table(
            [["Page", "Goal", "Single action"]]
            + [[s["page"], s["goal"], s["action"]] for s in data["site_map"]]
        ),
        "",
        "## Privacy rules (baked into these facts)",
        "",
    ]
    for p in data["privacy"]:
        lines.append("- " + p)
    lines += [
        "",
        "## Change log",
        "",
        "- `{}` — version {} (generated from canonical.json).".format(
            m["updated"], m["version"]
        ),
        "",
    ]
    return "\n".join(lines)


def build_brand(data):
    b = data["brand"]
    m = data["meta"]
    lines = [
        "---",
        "name: brand-guidelines",
        "slug: brand-guidelines",
        "status: canonical",
        "owner: L. Taylor III",
        "updated: {}".format(m["updated"]),
        "---",
        "",
        GENERATED_NOTE,
        "# Brand Guidelines",
        "",
        "> **Canonical.** Any AI tool producing copy or design for the house runs",
        "> under these rules. Generated from `canonical.json`; the JSON wins.",
        "",
        "## Palette",
        "",
        _table(
            [["Name", "Hex"]] + [[k, v] for k, v in b["palette"].items()]
        ),
        "",
        "## Voice",
        "",
        b["voice"],
        "",
        "## Tagline",
        "",
        b["tagline"],
        "",
        "## House rules",
        "",
    ]
    for r in b["rules"]:
        lines.append("- " + r)
    lines += [
        "",
        "## Change log",
        "",
        "- `{}` — generated from canonical.json.".format(m["updated"]),
        "",
    ]
    return "\n".join(lines)


def main():
    with open(CANONICAL_JSON, "r", encoding="utf-8") as fh:
        data = json.load(fh)

    outputs = {
        SPEC_DIR / "canonical-house-facts.md": build_house_facts(data),
        SPEC_DIR / "brand-guidelines.md": build_brand(data),
    }

    for path, text in outputs.items():
        path.write_text(text, encoding="utf-8")
        print("wrote {}".format(path.relative_to(ROOT)))

    print("\nDone. Markdown specs are in sync with canonical.json.")


if __name__ == "__main__":
    sys.exit(main())
