# KNOWLEDGE

What the house knows, and why. Organized by kind, not by project.

| Folder | Holds | Format |
|---|---|---|
| `decisions/` | One record per consequential decision (append-only) | `templates/decision.md` |
| `research/` | Findings, sources, competitive intel | free-form, dated |
| `specs/` | Canonical specs the site + server are generated from | `templates/spec.md` |
| `prompts/` | Reusable, versioned prompts for the AI tools | `templates/prompt.md` |
| `roadmaps/` | One roadmap per project, now/next/later/shipped | `templates/roadmap.md` |

**Rule of thumb:** a fact goes in `specs/` when it must be true everywhere; a
*choice* goes in `decisions/`; a *discovery* goes in `research/`; a *plan* goes
in `roadmaps/`; a *repeatable instruction to an AI* goes in `prompts/`.
