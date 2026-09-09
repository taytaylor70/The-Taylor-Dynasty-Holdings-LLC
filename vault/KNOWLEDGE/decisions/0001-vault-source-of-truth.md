---
id: 0001
title: The Vault is the single source of truth
status: accepted
date: 2026-09-08
supersedes: none
superseded_by: none
---

# Decision: The Vault is the single source of truth

## Context

The house's facts (ventures, founder bio, brand, contact) were duplicated
across the website HTML and the MCP server, with no authority. Any edit meant
hunting the same fact down in several files, and the tools could silently
drift apart. Meanwhile the owner wants ChatGPT, Claude, Gemini, Lovable,
Replit, and Cursor to *work on* the projects without *owning* them.

## Decision

Create a portable Vault (`vault/`) with three pillars — PROJECTS, KNOWLEDGE,
ASSETS — and declare it the single source of truth. The website and the MCP
server become projections of the Vault. Every AI tool reads the Vault before
acting and writes back after acting, per `AGENTS.md`.

## Consequences

- **Good:** one place to change a fact; tools inherit the same contract; no
  silent drift between site and server.
- **Bad:** discipline required — every change must be written back, or the
  Vault drifts and the whole point is lost.
- **To watch:** if projections keep getting hand-edited with canonical facts,
  tighten the rule or generate them from the spec.

## Alternatives considered

| Option | Why we rejected it |
|---|---|
| Keep facts in the MCP server only | Not human- or tool-friendly; HTML still duplicated them |
| Keep facts in the HTML only | Not machine-readable; weak for other AI tools |
| A database/headless CMS | Overkill for a portable, Git-backed Vault |
