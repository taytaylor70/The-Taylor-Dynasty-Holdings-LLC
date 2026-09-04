# The Taylor Dynasty — MCP Server

Turn any MCP-capable client (Claude Desktop, Claude Code, Cursor, etc.) into an
assistant that *knows the house*: the ventures, the founder's public story, the
tech stack, the career receipts, the brand rules, and the contact protocol.

**Zero dependencies** — Python 3.9+ only. Speaks newline-delimited JSON-RPC 2.0
over stdio (the standard MCP transport).

---

## Tools (10)

| Tool | What it returns |
|---|---|
| `dynasty_overview` | The parent ecosystem, the five ventures, the standard |
| `founder_profile` | Public-safe bio of L. Taylor III |
| `ventures_list` | Parent + 5 ventures with type, status, summary |
| `venture_detail` | One venture's full record (`{"name": "DogSphere"}`) |
| `tech_capabilities` | The toolkit + who it's built for |
| `career_timeline` | The full public work history, 1995 → now |
| `contact_info` | Cell, email, hours, the calling philosophy |
| `brand_guidelines` | Palette, voice, and the house copy rules |
| `site_map` | The 5 pages, each page's goal + single call to action |
| `search_dynasty` | Keyword search across everything (`{"query": "AI"}`) |

## Quick test (no client needed)

```bash
cd taylor-dynasty/mcp
printf '%s\n' \
  '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}' \
  '{"jsonrpc":"2.0","id":2,"method":"tools/list"}' \
  '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"dynasty_overview","arguments":{}}}' \
  | python3 server.py
```

## Register with Claude Desktop

Add to `claude_desktop_config.json` (Settings → Developer → Edit Config):

```json
{
  "mcpServers": {
    "taylor-dynasty": {
      "command": "python3",
      "args": ["/absolute/path/to/taylor-dynasty/mcp/server.py"]
    }
  }
}
```

## Register with Claude Code

```bash
claude mcp add taylor-dynasty python3 /absolute/path/to/taylor-dynasty/mcp/server.py
```

## Privacy rules (enforced in the data, not just the docs)

The knowledge base mirrors the public site exactly — it contains **no** street
address, birthday or birth time, home city, or school names. If a fact isn't
safe for the website, it isn't in the server.

## Extending it

Ideas queued: `resources/` exposing each page's copy as an MCP resource,
`prompts/` for generating on-brand proposals, and a `site_stats` tool wired to
real analytics once the domain is live.
