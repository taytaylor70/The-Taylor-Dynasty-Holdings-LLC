---
id: 0004
title: The website is generated from canonical.json
status: accepted
date: 2026-09-08
supersedes: none
superseded_by: none
---

# Decision: The website is generated from canonical.json

## Context

Decisions 0001 and 0003 made the Vault the source of truth and canonical.json
its machine-readable form. But the five website pages still carried the facts
as hand-pasted literals — the same phone, email, tagline, and venture names
repeated dozens of times, able to drift from the JSON.

## Decision

Generate the five pages from canonical.json. The design and bespoke copy live
in `site/templates/*.html` as templates with `{{TOKENS}}` for the facts; a
build script (`tools/build_site.py`) injects the facts and writes the live
pages at the repo root.

## Consequences

- **Good:** one edit to canonical.json updates every occurrence of a fact
  across the site, the markdown specs, and the MCP server.
- **Good:** the build is idempotent and verified byte-for-byte against the
  pre-existing pages (only the "GENERATED FILE" banner was added).
- **Bad:** the site now has a build step; anyone hand-editing a root `*.html`
  will have their changes overwritten by the next build.
- **To watch:** venture names that appear in *derived* forms on the page
  (e.g. `<br>` line-breaks, `&#39;` HTML entities) are not yet tokenized —
  track those down if the names ever change.

## Alternatives considered

| Option | Why we rejected it |
|---|---|
| A JS SPA that fetches canonical.json at runtime | Breaks the "fully static, no build step" deploy; adds a network/JSON fetch |
| Server-side templating (Jinja at request time) | Requires a backend; the site must stay static |
| Leave the pages hand-authored and "review" them against the spec | No enforcement — exactly the drift this Vault exists to kill |
