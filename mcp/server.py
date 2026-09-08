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

Privacy rules baked into the knowledge base (mirrors the website):
  · No street address  · no birthday / birth time  · no home city
  · No school names    · public-safe bio only
"""
import json
import sys

SERVER_NAME = "taylor-dynasty-mcp"
SERVER_VERSION = "1.0.0"
PROTOCOL_VERSION = "2024-11-05"

# ======================================================================
# KNOWLEDGE BASE (public-safe)
# ======================================================================
FOUNDER = {
    "preferred_name": "L. Taylor III (goes by \"TayTay\" in person)",
    "role": "Founder — All Technology, Software Engineering, Digital Product Creation",
    "based_in": "Columbus, Ohio · Eastern Time",
    "roots": "Orlando, Florida roots, Maryland finish",
    "generation": "First generation — the dynasty starts with him",
    "education_public": [
        "Office Administration Certification (2013)",
        "GED — McDonough High School, Maryland (2008)",
    ],
    "standard_quote": "I love anything Technology, Fast, seductive, grown and sexy, "
                      "as well as having determination for the making of greatness.",
    "story_short": "Saw technology promise a meritocracy and quietly become a gate. "
                   "Built the house to close that gap — certified in the fundamentals, "
                   "self-taught in the future, 100% founder-owned.",
}

VENTURES = [
    {
        "name": "The Taylor Dynasty Holdings LLC",
        "type": "Parent ecosystem",
        "status": "Active · 100% founder-owned · zero outside investors",
        "summary": "The parent company and legal spine: operating agreement (trust "
                   "ownership, management authority, capital, distributions, banking "
                   "authority, successor continuity, dissolution, Schedule A) plus a "
                   "trademark & IP portfolio system with USPTO filing tracker, domain "
                   "and copyright registries.",
    },
    {
        "name": "Oasis Marketplace",
        "type": "Commerce · digital storefront",
        "status": "Building (est. 2025)",
        "summary": "The commerce layer of the ecosystem — the house's digital products "
                   "and a shortlist of curated goods, sold under one standard.",
    },
    {
        "name": "DogSphere",
        "type": "Pet ecosystem",
        "status": "Building (est. 2025)",
        "summary": "Everything dogs, in one sphere — products, community, and care for "
                   "the people who take the 6 a.m. walk.",
    },
    {
        "name": "Taylor Made Real Estate",
        "type": "Property",
        "status": "Building (est. 2025)",
        "summary": "The family trade, formalized. Taylor Made General Contractor ran "
                   "job sites 1995–2015; the name inherits two decades of building "
                   "standard and points it at property.",
    },
    {
        "name": "The Nephew's First Business™",
        "type": "Legacy venture",
        "status": "Trademark filed · building",
        "summary": "Labeled exactly as promised: the nephew's first business. Built "
                   "hand-in-hand with the next generation — the dynasty's first "
                   "inheritance, live.",
    },
    {
        "name": "The Taylor Edition",
        "type": "AI platform · software",
        "status": "In development (flagship)",
        "summary": "The house's AI platform — built in-house, in public. The flagship "
                   "proof that the technology division ships, not just plans.",
    },
]

CAPABILITIES = [
    ("IT Specialist", "Solo IT operations end to end — setups, fixes, hardening; every fix comes with the explanation."),
    ("Cybersecurity", "Locks before launch — hardened accounts, devices, and habits sized for real budgets."),
    ("Cloud Architecture", "Right-sized infrastructure — from first domain to multi-region, zero enterprise bloat."),
    ("DevOps Automation", "If you do it twice, it gets scripted — pipelines, deployments, busywork automated."),
    ("Software Engineering", "Napkin to production — clean, documented, maintainable builds."),
    ("Digital Product Creation", "Bite-sized AI bots, built and sold digitally — bots that answer, automate, and sell."),
]

AUDIENCE = [
    "Entry-level IT specialists — real skills, real tools, zero gatekeeping; the explanation comes with the fix.",
    "Solo / one-person operations — security, cloud, and automation right-sized and fully owned.",
]

CAREER = [
    ("1995–2015", "Taylor Made General Contractor, LLC", "Office assistant & carpenter's apprentice — the family business; work ethic installed early."),
    ("2015–2016", "MLS", "A year of showing up, every day, on time."),
    ("2016–2017", "Dover Cleaners", "Precision on a schedule."),
    ("2017–2018", "Redner's Warehouse Markets", "The public, at scale."),
    ("2017–2018", "Perdue Farms, Inc.", "Industrial discipline."),
    ("2019", "TAB Retail Construction", "Back on job sites — the family trade, one more time."),
    ("2019–2020", "Amazon Prime Delivery (DSP)", "Routes, rates, and logistics at scale — from the inside."),
    ("2020–", "FedEx (delivery driver)", "The last W-2. After the route: certifications, code, cloud — the pivot went full-time."),
    ("Now", "The Taylor Dynasty", "Every shift cashed, every skill banked. The house stands on all of it."),
]

CONTACT = {
    "cell": "(202) 276-0500 (call or text — the founder answers)",
    "email": "Taytaylor70@gmail.com",
    "hours": "Eastern Time · response within 24 hours",
    "philosophy": "One number, zero gatekeepers. Say who you are, ask the real "
                  "question, leave with a next step — a price, a plan, or an honest no.",
}

BRAND = {
    "palette": {"Onyx": "#0b0c0c", "Dynasty Gold": "#c0a57a", "Heirloom Cream": "#f2ecdb", "Midnight": "#091118"},
    "voice": "Clarity, high efficiency, empathy — formal but human. Skeptical, innovative, humble.",
    "rules": [
        "Never brag — show receipts instead.",
        "No apologies in copy; no empty flattery.",
        "One primary action per page, and every action ends at the cell.",
        "Explanations ship with the work — plain English, always.",
    ],
    "tagline": "Building Legacy. Creating Value. Engineering the Future.",
}

SITE_MAP = [
    ("/ (index.html)", "Earn the click — make a stranger feel the brand in 5 seconds", "Request Private Access → dial (202) 276-0500"),
    ("/about (about.html)", "Build trust — the problem, the receipts, the payoff", "Call the founder directly"),
    ("/holdings (holdings.html)", "Show proof — the five ventures and the legal spine", "Request the private deck"),
    ("/tech (tech.html)", "Establish authority — capability plus taste", "Start a project conversation"),
    ("/contact (contact.html)", "Convert — zero friction between intent and a dial", "Dial (202) 276-0500"),
]

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
    if not q:
        return "Provide a venture name, e.g. {\"name\": \"DogSphere\"}. Known: " + ", ".join(v["name"] for v in VENTURES)
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
    {"name": "venture_detail", "description": "Full record for one venture by name (e.g. 'DogSphere', 'The Taylor Edition').",
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
