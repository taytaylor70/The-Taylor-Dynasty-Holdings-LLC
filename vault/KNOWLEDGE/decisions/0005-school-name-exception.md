---
id: 0005
title: Allow the public GED school name as the sole school-name exception
status: accepted
date: 2026-09-08
supersedes: none
superseded_by: none
---

# Decision: Allow the public GED school name as the sole school-name exception

## Context

Decision 0002 declared the repo "public-safe only" and named school names among
the excluded facts. But the founder's own public GED record — "GED — McDonough
High School, Maryland (2008)" — has been in the public site and the knowledge
base from the start, and the owner chose to keep it (see the founder-record
reconciliation of 2026-09-08). The blanket "no school names" rule therefore
contradicted the data the owner wants published.

## Decision

Refine the privacy rule to: **no school names beyond the public GED record
(McDonough High School).** The GED school name is the single permitted
exception; every other school name stays excluded.

## Consequences

- **Good:** the rule now matches the data and the owner's intent; no more
  contradiction between policy and published facts.
- **Good:** still maximally private — only the already-public GED school name
  is allowed; no new school names may be added.
- **Bad:** the exception is narrow and specific, so it must not become a
  precedent for adding other school names.
- **To watch:** if another education credential (or a child's school) is ever
  mentioned, it is **not** covered by this exception and must stay out.

## Alternatives considered

| Option | Why we rejected it |
|---|---|
| Keep "no school names" and remove the GED school name | Contradicts the owner's explicit choice to keep the public record |
| Allow all education school names | Opens the door to exactly the exposure the rule exists to prevent |
| Redact to "Maryland" only | Loses a documented public credential for no privacy gain |
