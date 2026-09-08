#!/usr/bin/env python3
"""
THE TAYLOR DYNASTY — MCP Server
================================
A zero-dependency Model Context Protocol (MCP) server that exposes the
public knowledge base of The Taylor Dynasty Holdings: the ventures, the
founder's story, tech capabilities, career timeline, brand guidelines,
and contact protocol.

Speaks newline-delimited JSON-RPC 2.0 over stdio (the MCP stdio
transport). No packages required — Python 3.9+ only.

Run:            python3 server.py
Register:       see README.md (Claude Desktop / Claude Code configs)

SOURCE OF TRUTH
---------------
This file contains NO knowledge. All facts are loaded at runtime from the
canonical spec:

    vault/KNOWLEDGE/specs/canonical.json

If a fact is wrong, fix it there — never here. The markdown specs under
vault/KNOWLEDGE/specs/ are generated from that JSON by tools/build_specs.py.

Privacy rules baked into the data (mirrors the website):
  · No street address  · no birthday / birth time  · no home city
  · No school names    · public-safe bio only
"""
import json
import os
import sys
from pathlib import Path

SERVER_NAME = "taylor-dynasty-mcp"
SERVER_VERSION = "2.0.0"
PROTOCOL_VERSION = "2024-11-05"

# ======================================================================
# CANONICAL DATA (loaded at runtime — the single source of truth)
# ======================================================================
CANONICAL_ENV = "TAYLOR_DYNASTY_CANONICAL"
_DEFAULT_CANONICAL = (
    Path(__file__).resolve().parent.parent
    / "vault" / "KNOWLEDGE" / "specs" / "canonical.json"
)


def _canonical_path() -> Path:
    override = os.environ.get(CANONICAL_ENV)
    if override:
        return Path(override)
    return _DEFAULT_CANONICAL


def _load_canonical() -> dict:
    path = _canonical_path()
    if not path.is_file():
        raise SystemExit(
            "Canonical spec not found: {}\n"
            "This server holds no facts of its own. Point {} at "
            "vault/KNOWLEDGE/specs/canonical.json (or keep this file inside "
            "the repo).".format(path, CANONICAL_ENV)
        )
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


_DATA = _load_canonical()

FOUNDER = _DATA["founder"]
VENTURES = _DATA["ventures"]
CAPABILITIES = [(c["name"], c["description"]) for c in _DATA["capabilities"]]
AUDIENCE = _DATA["audience"]
CAREER = [(c["span"], c["org"], c["note"]) for c in _DATA["career"]]
CONTACT = _DATA["contact"]
BRAND = _DATA["brand"]
SITE_MAP = [(s["page"], s["goal"], s["action"]) for s in _DATA["site_map"]]

# ======================================================================
# TOOL IMPLEMENTATIONS
# ======================================================================
def t_overview(_):
    lines = [
        "THE TAYLOR DYNASTY HOLDINGS — " + BRAND["tagline"],
        "",
        "A first-generation family enterprise: one parent ecosystem, five ventures,",
        "100% founder-owned, zero outside investors. Built in-house, on real paper",
        "(operating agreement + trademark/IP portfolio), to be inherited — not flipped.",
        "",
        "Ventures: " + ", ".join(v["name"] for v in VENTURES[1:]),
        "",
        "Founder: " + FOUNDER["preferred_name"] + " — " + FOUNDER["role"],
        "The standard, verbatim: \"" + FOUNDER["standard_quote"] + "\"",
    ]
    return "\n".join(lines)

def t_founder(_):
    ed = "\n".join("  · " + e for e in FOUNDER["education_public"])
    return "\n".join([
        "FOUNDER PROFILE — " + FOUNDER["preferred_name"],
        "Role: " + FOUNDER["role"],
        "Based: " + FOUNDER["based_in"],
        "Roots: " + FOUNDER["roots"],
        "Generation: " + FOUNDER["generation"],
        "Education (public record):", ed,
        "", "Story: " + FOUNDER["story_short"],
    ])

def t_ventures(_):
    out = ["THE VENTURES (6 entries: parent + 5)"]
    for v in VENTURES:
        out.append("")
        out.append("▸ " + v["name"] + " — " + v["type"])
        out.append("  Status: " + v["status"])
        out.append("  " + v["summary"])
    return "\n".join(out)

def t_venture_detail(args):
    q = str(args.get("name", "")).strip().lower()
    example = VENTURES[1]["name"] if len(VENTURES) > 1 else "a venture"
    if not q:
        return "Provide a venture name, e.g. {\"name\": \"" + example + "\"}. Known: " + ", ".join(v["name"] for v in VENTURES)
    for v in VENTURES:
        if q in v["name"].lower():
            return v["name"] + " — " + v["type"] + "\nStatus: " + v["status"] + "\n" + v["summary"]
    return "No venture matched '" + q + "'. Known: " + ", ".join(v["name"] for v in VENTURES)

def t_capabilities(_):
    out = ["TECH CAPABILITIES — All Technology · Software Engineering · Digital Product Creation", ""]
    for name, desc in CAPABILITIES:
        out.append("▸ " + name + " — " + desc)
    out.append("")
    out.append("Built for:")
    for a in AUDIENCE:
        out.append("  · " + a)
    return "\n".join(out)

def t_career(_):
    out = ["CAREER TIMELINE — twenty-five years of honest work", ""]
    for span, org, note in CAREER:
        out.append(span.ljust(11) + org + " — " + note)
    out.append("")
    out.append("Every check bankrolled the next skill; every skill built the house.")
    return "\n".join(out)

def t_contact(_):
    return "\n".join([
        "CONTACT — PRIVATE ACCESS",
        "Phone (cell): " + CONTACT["cell"],
        "Email: " + CONTACT["email"],
        "Hours: " + CONTACT["hours"],
        "", CONTACT["philosophy"],
    ])

def t_brand(_):
    pal = "\n".join("  · " + k + " " + v for k, v in BRAND["palette"].items())
    rules = "\n".join("  · " + r for r in BRAND["rules"])
    return "\n".join([
        "BRAND GUIDELINES", "Tagline: " + BRAND["tagline"], "",
        "Palette:", pal, "", "Voice: " + BRAND["voice"], "", "Rules:", rules,
    ])

def t_site_map(_):
    out = ["SITE MAP — 5 pages, one action each", ""]
    for page, goal, action in SITE_MAP:
        out.append(page + "\n  Goal: " + goal + "\n  Action: " + action + "")
    return "\n".join(out)

def t_search(args):
    q = str(args.get("query", "")).strip().lower()
    if not q:
        return "Provide {\"query\": \"...\"} — e.g. 'phone', 'AI', 'real estate', 'education'."
    corpus = []
    corpus.append(("overview", t_overview({})))
    corpus.append(("founder", t_founder({})))
    corpus.append(("ventures", t_ventures({})))
    corpus.append(("capabilities", t_capabilities({})))
    corpus.append(("career", t_career({})))
    corpus.append(("contact", t_contact({})))
    corpus.append(("brand", t_brand({})))
    corpus.append(("site map", t_site_map({})))
    hits = []
    for source, text in corpus:
        for line in text.split("\n"):
            if q in line.lower() and line.strip():
                hits.append("[" + source + "] " + line.strip())
    if not hits:
        return "No public records matched '" + q + "'. Try: ventures, AI, bots, real estate, phone, timeline, brand."
    seen, out = set(), ["SEARCH: '" + q + "' — " + str(len(hits)) + " match(es)"]
    for h in hits[:20]:
        if h not in seen:
            seen.add(h)
            out.append("  " + h)
    return "\n".join(out)

TOOLS = [
    {"name": "dynasty_overview", "description": "What The Taylor Dynasty Holdings is — the parent ecosystem, the five ventures, and the standard.",
     "inputSchema": {"type": "object", "properties": {}}},
    {"name": "founder_profile", "description": "Public-safe bio of L. Taylor III: role, base, roots, education, story.",
     "inputSchema": {"type": "object", "properties": {}}},
    {"name": "ventures_list", "description": "All six entries (parent + five ventures) with type, status, and summary.",
     "inputSchema": {"type": "object", "properties": {}}},
    {"name": "venture_detail", "description": "Full record for one venture by name, e.g. '" + VENTURES[1]["name"] + "' (partial match OK).",
     "inputSchema": {"type": "object", "properties": {"name": {"type": "string", "description": "Venture name (partial match OK)"}}, "required": ["name"]}},
    {"name": "tech_capabilities", "description": "The technology toolkit and who it's built for.",
     "inputSchema": {"type": "object", "properties": {}}},
    {"name": "career_timeline", "description": "The founder's full public work history, 1995 to now.",
     "inputSchema": {"type": "object", "properties": {}}},
    {"name": "contact_info", "description": "How to reach the house — cell, email, hours, philosophy.",
     "inputSchema": {"type": "object", "properties": {}}},
    {"name": "brand_guidelines", "description": "Palette, voice, and the house rules for copy and design.",
     "inputSchema": {"type": "object", "properties": {}}},
    {"name": "site_map", "description": "The five public pages, each page's goal, and its one call to action.",
     "inputSchema": {"type": "object", "properties": {}}},
    {"name": "search_dynasty", "description": "Keyword search across the entire public knowledge base.",
     "inputSchema": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}},
]
HANDLERS = {
    "dynasty_overview": t_overview, "founder_profile": t_founder, "ventures_list": t_ventures,
    "venture_detail": t_venture_detail, "tech_capabilities": t_capabilities,
    "career_timeline": t_career, "contact_info": t_contact, "brand_guidelines": t_brand,
    "site_map": t_site_map, "search_dynasty": t_search,
}

# ======================================================================
# JSON-RPC / MCP stdio loop
# ======================================================================
def send(payload):
    sys.stdout.write(json.dumps(payload) + "\n")
    sys.stdout.flush()

def rpc_error(rid, code, message):
    return {"jsonrpc": "2.0", "id": rid, "error": {"code": code, "message": message}}

def handle(req):
    method = req.get("method", "")
    rid = req.get("id")
    if rid is None:                     # notification — acknowledge silently
        return None
    if method == "initialize":
        return {"jsonrpc": "2.0", "id": rid, "result": {
            "protocolVersion": PROTOCOL_VERSION,
            "capabilities": {"tools": {}},
            "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION}}}
    if method == "ping":
        return {"jsonrpc": "2.0", "id": rid, "result": {}}
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": rid, "result": {"tools": TOOLS}}
    if method == "tools/call":
        params = req.get("params") or {}
        name = params.get("name", "")
        fn = HANDLERS.get(name)
        if fn is None:
            return rpc_error(rid, -32602, "Unknown tool: " + name)
        try:
            text = fn(params.get("arguments") or {})
            return {"jsonrpc": "2.0", "id": rid, "result":
                    {"content": [{"type": "text", "text": text}]}}
        except Exception as e:                       # noqa: BLE001
            return rpc_error(rid, -32000, "Tool error: " + str(e))
    return rpc_error(rid, -32601, "Method not found: " + method)

def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except json.JSONDecodeError:
            send(rpc_error(None, -32700, "Parse error"))
            continue
        resp = handle(req)
        if resp is not None:
            send(resp)

if __name__ == "__main__":
    main()
