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
from that JSON by `../../tools/build_specs.py`.

## What we know (links, not copies)

- Spec: `../../KNOWLEDGE/specs/canonical.json` (the single source of truth)
- Contract: `../../AGENTS.md` (the rules every tool inherits)
- Decisions: `../../KNOWLEDGE/decisions/`
- Roadmap: `../../KNOWLEDGE/roadmaps/ai-agent-harness.md`

## Assets

- Server: `../../mcp/server.py`, docs: `../../mcp/README.md`
- Generator: `../../tools/build_specs.py`

## Open questions

- [ ] Generate the website HTML from `canonical.json` too, or leave the HTML
      hand-authored and the spec as the review reference?
- [ ] Which MCP clients to document onboarding for (Claude, Cursor, others).

## Log

- `2026-09-08` — created the Vault; wired the harness to the Vault contract.
- `2026-09-08` — server now loads `canonical.json` at runtime; markdown specs
      generated (single source of truth).
