---
id: 0002
title: Public-safe knowledge only
status: accepted
date: 2026-09-08
supersedes: none
superseded_by: none
---

# Decision: Public-safe knowledge only

## Context

The Vault is meant to be shared with third-party AI tools and synced to cloud
storage. Some personal facts (street address, birthday/birth time, home city,
school names) have no business in a shared, Git-backed source of truth.

## Decision

The Vault — and the whole repo — holds **public-safe facts only**. Excluded:
street address, birthday/birth time, home city, school names. Anything else
sensitive stays out of Git entirely.

## Consequences

- **Good:** the Vault can be shared with any tool without a leak.
- **Bad:** the private/legal layer (operating agreement, contracts) must live
  outside Git or in a private store.
- **To watch:** if a private fact is needed by a tool, use a private store —
  never a public repo.

## Alternatives considered

| Option | Why we rejected it |
|---|---|
| Private repo | Simpler, but blocks the whole "portable, shareable Vault" premise |
| Redacted placeholders in the Vault | Risky — a placeholder invites a bad actor to fill it in |
