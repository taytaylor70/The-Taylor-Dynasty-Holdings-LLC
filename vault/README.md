# The AI Project Vault

> **AI works on your projects. AI does not own your projects.**

This folder is the single source of truth for The Taylor Dynasty Holdings.
The website, the MCP server, and every AI tool (ChatGPT, Claude, Gemini,
Lovable, Replit, Cursor) are *tools that read from and update this Vault*.
They are never the owner.

## The shape

```
                  YOUR AI PROJECT VAULT  (this folder)
                          │
         ┌────────────────┼────────────────┐
         │                │                │
      PROJECTS          KNOWLEDGE         ASSETS
         │                │                │
    Taylor's Tech     Decisions        Logos
    Taylor Dynasty    Research         PDFs
    Oasis Marketplace Specs            Contracts
    AI Agent Harness  Prompts          Images
    Tayvora           Roadmaps         Code
         │                │                │
         └────────────────┼────────────────┘
                          │
                   GIT / CLOUD STORAGE
                          │
         ┌────────────────┼────────────────┐
         │                │                │
      ChatGPT           Claude           Gemini
         │                │                │
      Lovable           Replit           Cursor
```

## The three pillars

| Pillar | Holds | Answer this |
|---|---|---|
| `PROJECTS/` | One folder per venture/bet. `project.md` is the living front door. | *What are we building, and where does it stand?* |
| `KNOWLEDGE/` | Decisions, research, specs, prompts, roadmaps. | *What do we know, and why did we decide it?* |
| `ASSETS/` | Logos, PDFs, contracts, images, code. | *What raw material do the projects run on?* |

## Where the source of truth lives

- **Canonical facts** (founder, ventures, brand, contact, capabilities) live in
  `KNOWLEDGE/specs/canonical.json` — a single machine-readable file.
- The MCP server (`../mcp/server.py`) **loads that JSON at runtime and holds no
  facts of its own**.
- The markdown specs (`canonical-house-facts.md`, `brand-guidelines.md`) are
  **generated** from the JSON — run `python3 tools/build_specs.py`.
- The website (`../index.html` etc.) is a **projection** of the same facts:
  the pages are generated from `../site/templates/` + the JSON by
  `../tools/build_site.py`.
  If any of them disagree, `canonical.json` wins.
- **Every consequential decision** gets its own record in
  `KNOWLEDGE/decisions/`. Decisions are append-only; supersede, never delete.

## The workflow (any AI tool, every time)

```
1. READ      open the project.md + relevant decisions + specs
2. WORK      do the task inside the project's folder
3. WRITE     update project.md, add a decision record, bump `updated:`
4. COMMIT    one focused commit: <scope>: <what changed>
```

An AI that changes reality without writing it back into the Vault has broken
the contract — the Vault drifts, and the next tool starts from a lie.

## File conventions

- Folders: lowercase, hyphenated slugs (`oasis-marketplace`, `ai-agent-harness`).
- Every tracked markdown file starts with frontmatter (see `templates/`).
- Dates: `YYYY-MM-DD` UTC.
- Status vocabulary (projects): `idea · planning · building · live · paused · retired`.
- Status vocabulary (decisions): `proposed · accepted · superseded`.

## Adding a new AI tool

1. Point it at this repo.
2. Tell it: *"Read `AGENTS.md`, then `vault/README.md`, then the project."*
3. That's it — the contract is in the repo, so the tool inherits it.
