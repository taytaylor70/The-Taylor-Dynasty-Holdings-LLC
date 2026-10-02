---
id: 0006
title: Document MCP onboarding for Claude Desktop, Claude Code, and Cursor
status: accepted
date: 2026-10-02
supersedes: none
superseded_by: none
---

# Decision: Document MCP onboarding for Claude Desktop, Claude Code, and Cursor

## Context

The MCP server shipped with registration snippets for Claude Desktop and
Claude Code only, and both assumed a local checkout path without saying so.
Cursor — the client most likely to be pointed at this repo — had no docs at
all, and the quick test in `mcp/README.md` referenced a stale folder layout
(`cd taylor-dynasty/mcp`). Every one of these is a silent-failure mode: a
client that can't start the server just shows no tools, with no explanation.

## Decision

`mcp/README.md` is the single onboarding guide for the harness. It documents
Claude Desktop, Claude Code, and Cursor end to end — config file locations by
OS, copy-paste-ready JSON/CLI, the absolute-path requirement, how to restart
each client, a one-prompt connection check, and a troubleshooting table for
the common silent failures. Other stdio clients get the generic two-field
recipe.

Docs are part of the harness: a client that cannot be onboarded from the
README is not onboarded.

## Consequences

- **Good:** any AI tool can be connected without guessing; the "no facts of
  its own" rule and the privacy rules are stated where a client operator will
  actually read them; failures have named fixes instead of folklore.
- **Bad:** three clients means three surfaces that drift when a vendor moves a
  config path or CLI flag — the docs need periodic re-verification.
- **To watch:** a client's setup instructions changing in a way that makes the
  README wrong; a fourth MCP client (ChatGPT connectors, Gemini, etc.) gaining
  real stdio support and needing a section of its own.

## Alternatives considered

| Option | Why we rejected it |
|---|---|
| Per-client READMEs (`mcp/clients/*.md`) | Splits one 10-minute task across files; the shared prerequisites drift. |
| Link to each vendor's docs instead of copying snippets | Vendors restructure docs; the repo should carry the working recipe. |
| Document one client only (Claude Desktop) | Claude Code and Cursor are the tools that actually touch this repo. |
