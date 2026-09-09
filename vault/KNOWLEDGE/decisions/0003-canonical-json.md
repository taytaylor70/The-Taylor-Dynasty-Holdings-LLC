---
id: 0003
title: Canonical facts live in one JSON file
status: accepted
date: 2026-09-08
supersedes: none
superseded_by: none
---

# Decision: Canonical facts live in one JSON file

## Context

Decision 0001 declared the Vault the source of truth, but the house facts were
still duplicated: once in `mcp/server.py` (hardcoded dicts) and once in the
markdown spec. Editing a fact meant changing two files, and the server could
silently drift from the spec.

## Decision

Make `vault/KNOWLEDGE/specs/canonical.json` the single machine-readable source
of truth. `mcp/server.py` loads it at runtime and holds **no facts**; the
markdown specs (`canonical-house-facts.md`, `brand-guidelines.md`) are
**generated** from it by `tools/build_specs.py`.

## Consequences

- **Good:** one place to change any fact; zero drift between server and specs;
  the JSON is easy for any AI tool to read programmatically.
- **Bad:** markdown specs are now read-only (generated); a contributor must
  remember to regenerate after editing the JSON.
- **To watch:** if the website HTML ever gets hardcoded facts again, extend the
  generator (or a build step) to produce it from the same JSON.

## Alternatives considered

| Option | Why we rejected it |
|---|---|
| Parse the markdown spec in the server | Brittle; markdown tables are not a machine format |
| Keep facts in `server.py` and generate markdown from it | Couples knowledge to one tool's runtime; Python isn't a neutral data store |
| YAML instead of JSON | Marginal readability gain; JSON needs no extra parser |
