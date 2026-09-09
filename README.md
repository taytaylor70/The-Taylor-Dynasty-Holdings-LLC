# THE TAYLOR DYNASTY HOLDINGS

> Building Legacy. Creating Value. Engineering the Future.

The official website + MCP knowledge server for The Taylor Dynasty Holdings —
a first-generation family enterprise: one parent ecosystem, five ventures,
100% founder-owned.

> **This repo is the AI Project Vault.** The single source of truth is
> `vault/` — the website and MCP server are *projections* of it. AI tools
> (ChatGPT, Claude, Gemini, Lovable, Replit, Cursor) work **on** these
> projects; they do not **own** them. Start at `vault/README.md`.

## Structure

```
├── vault/            ← THE SOURCE OF TRUTH (projects, knowledge, assets)
│   ├── PROJECTS/         One folder per venture — project.md is the front door
│   ├── KNOWLEDGE/        decisions · research · specs · prompts · roadmaps
│   └── ASSETS/           logos · pdfs · contracts · images · code
├── AGENTS.md         The contract every AI tool inherits
├── CLAUDE.md         Pointer to AGENTS.md (Claude auto-reads this)
├── site/templates/   The five pages as templates (facts injected from the spec)
├── tools/            build_specs.py (markdown) · build_site.py (HTML)
├── index.html        Home — generated from site/templates/ (3D hero, live effects)
├── holdings.html     The Ventures — generated (Dynasty map, five ventures)
├── tech.html         The Craft — generated (capabilities, receipts, bots)
├── about.html        The Founder — generated (problem, receipts, payoff)
├── contact.html      Private Access — generated (one number, zero gatekeepers)
├── assets/           Favicons, OG image, source photography
└── mcp/              Zero-dependency MCP server (loads canonical.json)
```

> The HTML pages and the MCP server are **projections** of
> `vault/KNOWLEDGE/specs/canonical.json`. If they disagree with the JSON, the
> JSON wins — regenerate with `python3 tools/build_specs.py && python3 tools/build_site.py`.

## The site

Five pages, one action each — and every action ends at the cell.
Fully self-contained static HTML (no build step, no dependencies);
fonts are the only network request, with graceful offline fallbacks.

**Design system:** Onyx `#0b0c0c` · Dynasty Gold `#c0a57a` ·
Heirloom Cream `#f2ecdb` · Midnight `#091118`

## Deploy

Any static host takes this folder as-is:

```bash
# Netlify
npx netlify-cli deploy --prod --dir .

# Vercel
npx vercel --prod

# GitHub Pages
# Settings → Pages → Deploy from branch → main / root
```

After registering the domain, update the `taylordynasty.com` placeholder in
each page's `<head>` social meta block.

## The MCP server

Turns any MCP client into an assistant that knows the house — 10 tools
covering ventures, founder bio, tech capabilities, career timeline, brand
guidelines, and contact protocol. Python 3.9+, zero dependencies:

```bash
python3 mcp/server.py        # stdio JSON-RPC — see mcp/README.md to register
```

## Privacy

The public pages and the MCP knowledge base intentionally exclude the
street address, birthday/birth time, and home city. School names are also
excluded — **except** the one in the public GED record (McDonough High School).
Keep it that way in future edits.

---
© The Taylor Dynasty Holdings LLC · First generation. Century vision.
