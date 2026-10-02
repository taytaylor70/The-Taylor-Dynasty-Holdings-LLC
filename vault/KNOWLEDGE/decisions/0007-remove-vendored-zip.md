---
id: 0007
title: Remove the vendored repo zip from the repository
status: accepted
date: 2026-10-02
supersedes: none
superseded_by: none
---

# Decision: Remove the vendored repo zip from the repository

## Context

The initial commit vendored `The-Taylor-Dynasty-Holdings-LLC.zip` (~2.6 MB) —
a snapshot of the whole project, including a nested `.git/` directory and
frozen copies of the built pages. One frozen copy (`about.html`) still carries
the expanded school name that decision `0005` excludes, so a tracked artifact
was contradicting the public-safe rule and no regeneration would ever fix it.

The Vault is the single source of truth; a zip of the repo duplicates it and
goes stale silently. Nothing in the repo references the zip.

## Decision

Delete the zip from the repository and ignore `*.zip` from now on. Git history
still contains the blob — purging it requires a history rewrite (force-push on
`main`), which is an owner decision and is **not** done here.

## Consequences

- **Good:** one less stale, privacy-drifting duplicate; smaller repository;
  nothing to keep in sync.
- **Bad:** anyone who wants a zip must build one on demand (`git archive`)
  instead of pulling it from the repo.
- **To watch:** the expanded school name remains reachable in old commits
  until (unless) the owner orders a history rewrite.

## Alternatives considered

| Option | Why we rejected it |
|---|---|
| Keep the zip and refresh it each release | Duplicates the Vault; drifts again on the next change |
| Keep the zip but scrub the school name inside it | Still duplicates 2.6 MB and a nested `.git/`, still drifts |
| Rewrite history to purge the blob now | Force-push on shared `main` — needs explicit owner sign-off first |
