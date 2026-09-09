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
- The five website pages (`../index.html` …) are generated from the JSON too —
  via `site/templates/` + `tools/build_site.py`.

## Editing a fact

1. Edit `canonical.json`.
2. Regenerate everything:
   `python3 tools/build_specs.py && python3 tools/build_site.py`
3. Commit. The MCP server picks up the change automatically at next start.

If a projection disagrees with `canonical.json`, the **JSON wins** — fix the
projection (regenerate), not the JSON.
