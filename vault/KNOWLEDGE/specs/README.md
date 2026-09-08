# Specs

Canonical specs. The website and the MCP server are **projections** of these
facts — change them here first, then regenerate/update the projections.

## The single source of truth

| File | Role |
|---|---|
| `canonical.json` | **THE source of truth** — all house facts, machine-readable |
| `canonical-house-facts.md` | *generated* — human-readable rendering of the JSON |
| `brand-guidelines.md` | *generated* — brand rendering of the JSON |

- `mcp/server.py` loads `canonical.json` at runtime and holds **no facts**.
- The two markdown files are generated from the JSON. **Do not hand-edit them.**

## Editing a fact

1. Edit `canonical.json`.
2. Run `python3 tools/build_specs.py` to regenerate the markdown specs.
3. Commit both. The MCP server picks up the change automatically at next start.

If a projection disagrees with `canonical.json`, the **JSON wins** — fix the
projection, not the JSON.
