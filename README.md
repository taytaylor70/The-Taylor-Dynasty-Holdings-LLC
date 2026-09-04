# THE TAYLOR DYNASTY HOLDINGS

> Building Legacy. Creating Value. Engineering the Future.

The official website + MCP knowledge server for The Taylor Dynasty Holdings —
a first-generation family enterprise: one parent ecosystem, five ventures,
100% founder-owned.

## Structure

```
├── index.html        Home — earn the click (3D hero, 4D tesseract, live effects)
├── holdings.html     The Ventures — Dynasty map, five ventures, legal spine
├── tech.html         The Craft — capabilities, receipts, bite-sized AI bots
├── about.html        The Founder — problem, receipts, payoff
├── contact.html      Private Access — one number, zero gatekeepers
├── assets/           Favicons, OG image, source photography
└── mcp/              Zero-dependency MCP server (the house knowledge base)
```

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
street address, birthday/birth time, home city, and school names.
Keep it that way in future edits.

---
© The Taylor Dynasty Holdings LLC · First generation. Century vision.
