# AGENTS.md — How AI tools work inside this repo

The single source of truth for everything in this repository is the **Vault**
(`vault/`). Everything else — the website (`*.html`), the MCP server
(`mcp/`), deploys, and exports — is a *projection* of the Vault.

**You read from the Vault before you act, and you write back to the Vault
after you act.**

## The one rule that matters

> **You work on these projects. You do not own these projects.**

You are a tool. The owner is L. Taylor III. The Vault is his. Your job is to
make the Vault more accurate, more complete, and more useful — never to
substitute your judgment for his, invent facts, or sand down his voice.

## Read before you act

1. `vault/README.md` — how the Vault is organized and the workflow.
2. `vault/PROJECTS/<project>/project.md` — the project you're about to touch.
3. `vault/KNOWLEDGE/decisions/` — decisions already made. Don't relitigate them.
4. `vault/KNOWLEDGE/specs/` — canonical specs (house facts, brand, architecture).

## Write back after you act

- Every change you make to *reality* must be reflected in the Vault.
- Do the work inside the relevant `vault/PROJECTS/<project>/`.
- Record every consequential decision as a new record in
  `vault/KNOWLEDGE/decisions/` (use `vault/templates/decision.md`).
- Bump the `updated:` field in the frontmatter of any file you change.
- When you change the website or the MCP server, update the canonical specs in
  `vault/KNOWLEDGE/specs/` too — not just the projection.

## Never

- Invent facts about the founder, the ventures, money, or legal status.
- Delete or rename files without logging the decision first.
- Put secrets, addresses, birthdays, birth times, home cities, or school names
  anywhere in this repo.
- Write "as the AI" or claim ownership of a project in any copy.
- Hardcode canonical facts into `*.html` or `mcp/server.py` — a canonical fact
  lives in `vault/KNOWLEDGE/specs/`; the HTML and server are derived from it.

## Privacy (non-negotiable)

This repo is public-safe. Excluded: street address, birthday/birth time, home
city, school names. If a fact isn't safe for the public website, it doesn't
belong in this repo — keep it out entirely, or keep it outside Git.

## Commit convention

`<scope>: <what changed>` — scope is one of `vault`, `projects`, `knowledge`,
`assets`, `site`, `mcp`. Example: `vault: add Tayvora project.md`.
