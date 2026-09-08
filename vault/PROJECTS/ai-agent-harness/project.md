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
(10 tools). Next: derive the server's data from
`../../KNOWLEDGE/specs/canonical-house-facts.md` instead of a hand-maintained
copy, so there is exactly one source of truth.

## What we know (links, not copies)

- Spec: `../../KNOWLEDGE/specs/canonical-house-facts.md`
- Contract: `../../AGENTS.md` (the rules every tool inherits)
- Decisions: `../../KNOWLEDGE/decisions/`
- Roadmap: `../../KNOWLEDGE/roadmaps/ai-agent-harness.md`

## Assets

- Server: `../../mcp/server.py`, docs: `../../mcp/README.md`

## Open questions

- [ ] Move server data to a shared `canonical.json` that both the site and the
      server read, or keep markdown as the canonical form and generate JSON?
- [ ] Which MCP clients to document onboarding for (Claude, Cursor, others).

## Log

- `2026-09-08` — created the Vault; wired the harness to the Vault contract.
