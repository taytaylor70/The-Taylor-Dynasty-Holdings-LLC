---
name: AI Agent Harness
slug: ai-agent-harness
status: building
owner: L. Taylor III
created: 2026-09-08
updated: 2026-09-08
---

# AI Agent Harness

The tooling that turns generic AI models into assistants that *know the
house* — the MCP knowledge server plus the agent contract (`../../AGENTS.md`).

## Pitch

Make every AI tool (ChatGPT, Claude, Gemini, Cursor, Lovable, Replit) a
first-class citizen of the house: it reads the Vault, works on the projects,
and writes back. The harness is what keeps "works on" from becoming "owns".

## Status

Building. `../../mcp/server.py` exposes the public knowledge base over MCP
(10 tools) and **loads all facts from `../../KNOWLEDGE/specs/canonical.json`
at runtime** — it holds no facts of its own. The markdown specs are generated
from that JSON by `../../tools/build_specs.py`, and the five website pages are
generated from `../../site/templates/` by `../../tools/build_site.py`.

## What we know (links, not copies)

- Spec: `../../KNOWLEDGE/specs/canonical.json` (the single source of truth)
- Contract: `../../AGENTS.md` (the rules every tool inherits)
- Decisions: `../../KNOWLEDGE/decisions/`
- Roadmap: `../../KNOWLEDGE/roadmaps/ai-agent-harness.md`

## Assets

- Server: `../../mcp/server.py`, docs: `../../mcp/README.md`
- Generators: `../../tools/build_specs.py` (markdown), `../../tools/build_site.py` (HTML)
- Templates: `../../site/templates/`

## Open questions

- [ ] Which MCP clients to document onboarding for (Claude, Cursor, others).
- [ ] Tokenize the two remaining *derived* venture-name forms (the `<br>`
      line-break in the holdings map, and the `&#39;` entity in the index
      contact dropdown) so 100% of name occurrences are generated.

## Resolved

- Founder-record drift (2026-09-08, owner decision): full legal name is
  **Luther A. Taylor III** (now in canonical.json + site + MCP founder profile);
  the school is **McDonough High School** (abbreviated — "Maurice J." scrubbed
  from the site, matching the public-safe record). See log below.

## Log

- `2026-09-08` — created the Vault; wired the harness to the Vault contract.
- `2026-09-08` — server now loads `canonical.json` at runtime; markdown specs
      generated (single source of truth).
- `2026-09-08` — the five website pages now generate from canonical.json via
      `site/templates/` + `tools/build_site.py`.
- `2026-09-08` — reconciled the founder-record drift: full name → canonical
      (`full_name`), school name → abbreviated, and the education facts are now
      tokenized (`{{EDU0}}`, `{{EDU1}}`) so they can't drift again.
