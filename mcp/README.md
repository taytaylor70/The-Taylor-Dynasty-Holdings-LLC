# The Taylor Dynasty — MCP Server

> **This server holds no facts of its own.** It loads its entire knowledge base
> at runtime from `../vault/KNOWLEDGE/specs/canonical.json` — the single source
> of truth. To change a fact, edit the JSON and restart the server; the markdown
> specs are regenerated with `python3 tools/build_specs.py`.

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

From the repo root:

```bash
cd mcp
printf '%s\n' \
  '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}' \
  '{"jsonrpc":"2.0","id":2,"method":"tools/list"}' \
  '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"dynasty_overview","arguments":{}}}' \
  | python3 server.py
```

You should see three JSON lines come back — `serverInfo`, a list of 10 tools,
and the house overview. Do this **before** configuring any client: it proves
Python and the Vault JSON are working, so any later failure is a client-config
problem, not a server problem.

---

## Before you start (30 seconds)

1. **Python 3.9+**
   ```bash
   python3 --version        # Windows: python --version
   ```
2. **The absolute path to `server.py`.** Clients do **not** expand `~`, `.`,
   or environment variables in `args` — give them the full path:
   ```bash
   pwd                      # from the repo root, e.g. /Users/taytay/taylor-dynasty
   # the path you need: /Users/taytay/taylor-dynasty/mcp/server.py
   ```
3. **Smoke-test the server** with the quick test above.

Throughout the rest of this file, replace `/absolute/path/to/taylor-dynasty`
with that real path.

---

## Onboarding

### 1. Claude Desktop

**Where the config lives** (create the file if it doesn't exist yet):

| OS | Path |
|---|---|
| macOS | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Windows | `%APPDATA%\Claude\claude_desktop_config.json` |
| Linux | `~/.config/Claude/claude_desktop_config.json` |

The easiest route: **Settings → Developer → Edit Config** opens the file
directly.

Add the server:

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

- If the file already has an `mcpServers` block, add the `"taylor-dynasty"`
  entry **inside** it — don't replace the file.
- **Restart Claude Desktop completely.** Closing the window is not enough:
  macOS → right-click the dock icon → Quit; Windows → right-click the tray
  icon → Exit. Reopen the app.
- **Verify:** the tools (hammer) icon appears in the composer — ask
  *"call dynasty_overview"*. MCP logs live under **Settings → Developer**.

### 2. Claude Code

One command, run from anywhere:

```bash
claude mcp add --scope user taylor-dynasty -- python3 /absolute/path/to/taylor-dynasty/mcp/server.py
```

- `--scope user` makes the server available in every project. Without it the
  default is **local** — it works only in the folder you ran the command from
  and looks "missing" everywhere else. `--scope project` writes a shareable
  `.mcp.json` into that project instead.
- Everything after `--` is the server command — keep the two dashes.
- **Verify:** `claude mcp list` (expect *Connected*), or `/mcp` inside a
  session.
- Remove with `claude mcp remove taylor-dynasty`.

### 3. Cursor

**Where the config lives** — a project file overrides the global one:

| Scope | Path |
|---|---|
| Global (all projects) | `~/.cursor/mcp.json` |
| Project (just this repo) | `.cursor/mcp.json` |

The easiest route: **Settings → Tools & MCP → New MCP Server**, which opens
the config file for you.

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

- The `mcpServers` root key is required — without it, Cursor silently ignores
  the file.
- Project config is machine-specific (it hardcodes one absolute path); prefer
  the **global** file so every workspace gets the server.
- **Reload:** **Settings → Tools & MCP** (or restart Cursor). Confirm the
  server shows as connected, then ask the Agent *"list the taylor-dynasty
  tools"*.

### 4. Any other MCP client (generic)

Every stdio client needs the same two pieces:

```
command:  python3                        (Windows: python)
args:     ["/absolute/path/to/taylor-dynasty/mcp/server.py"]
```

No API key, no port, no network — the server only reads the Vault JSON.

---

## Verify it's connected (once per client)

Ask the assistant to run:

> Call `dynasty_overview`, then `ventures_list`.

Expected: the parent ecosystem, the five ventures, and the standard quote —
then a `ventures_list` with **6 entries** (parent + five ventures). If you get
that, every tool above works. If not, see Troubleshooting.

---

## Troubleshooting

| Symptom | Likely cause / fix |
|---|---|
| Server listed, but no tools appear | `args` uses a relative path or `~`. Use the **absolute** path. |
| `command not found: python3` (Windows) | Use `"command": "python"`, or the full path from `where python`. |
| `Canonical spec not found: …` | The server resolves `canonical.json` relative to its own file. Keep `server.py` inside the repo, or set `TAYLOR_DYNASTY_CANONICAL` (below). |
| Client ignores the config entirely | Validate the JSON — configs fail silently on a stray comma: `python3 -m json.tool <config file>` |
| Tools appear, but answers are stale | The server reads `canonical.json` **at startup**. Restart the client after editing the Vault. |
| Claude Desktop doesn't see it | Quit completely (dock/tray → Quit) and reopen. Check **Settings → Developer** logs. |

---

## Where the data lives

`server.py` resolves `canonical.json` relative to its own location, so keep it
inside the repo. To point it elsewhere (e.g. a packaged deploy), set:

```bash
export TAYLOR_DYNASTY_CANONICAL=/absolute/path/to/canonical.json
```

## Privacy rules (enforced in the data, not just the docs)

The knowledge base mirrors the public site exactly — it contains **no** street
address, birthday or birth time, home city, or school names (beyond the public
GED record, McDonough High School). If a fact isn't safe for the website, it
isn't in `canonical.json`.

## Extending it

Ideas queued: `resources/` exposing each page's copy as an MCP resource,
`prompts/` for generating on-brand proposals (the prompts now live in
`../vault/KNOWLEDGE/prompts/`), and a `site_stats` tool wired to real
analytics once the domain is live.
