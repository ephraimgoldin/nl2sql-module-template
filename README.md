# nl2sql-module-template

A starting point for a module for the **NL2SQL app**. Copy it, rename it, change
one function.

## The one rule

**You never edit the app.** Everything you write lives in your own package.
That is what lets a new core be shipped to you without touching your work — and
it is the instinct worth resisting, because the natural move is to open
`app.py`.

## Start

```powershell
git clone https://github.com/ephraimgoldin/nl2sql-module-template.git mymodule
cd mymodule
pip install -e . --extra-index-url https://ephraimgoldin.github.io/nl2sql-engine/simple/
```

`-e` is editable: change the code, refresh the browser, see it. No reinstall.

Open the app → **🧩 Modules** → your page is there, in the React app *and* the
Streamlit one. You wrote Python; you did not write any UI.

## What you write

```python
from nl2sql_engine.modules import Action, Input, Module, Result

def profile(ctx, table: str) -> Result:
    cols, _ = ctx.query(f'SELECT * FROM "{table}" LIMIT 0')
    return Result.table([[c] for c in cols], ["column"], title=table)

MODULE = Module(
    name="mymodule", label="🔎 My module",
    requires_core=">=1.0,<2.0",
    actions=[Action(name="profile", label="Profile a table", run=profile,
                    inputs={"table": Input(kind="table", label="Table")})],
)
```

An action takes `ctx` plus its declared inputs and returns a `Result`.

## `ctx` — everything you get

| | |
|---|---|
| `ctx.query(sql)` | read-only SQL → `(columns, rows)`. Same guardrail as the rest of the app. |
| `ctx.tables()` | table names |
| `ctx.columns(table)` | column names |
| `ctx.schema_text()` | the schema as the model is shown it, semantic layer included |
| `ctx.data_dir()` | where you may write. Survives a core upgrade. |

Deliberately small, and versioned. If something you need is missing, that is a
gap in the contract worth reporting — not a reason to reach into the engine.

## Result kinds

`Result.table(rows, columns)` · `Result.markdown(text)` · `Result.sql(text)` ·
`Result.chart({"rows": ...})` · `Result.error(message)`

Rows are **positional** — a list of lists matching `columns`.

## Input kinds

`table` · `column` (set `of_table="table"`) · `text` · `number` · `bool` ·
`choice` (with `choices=[...]`)

Each frontend draws the right control. You never write a widget.

## Versions

`requires_core` is checked against the core's **`API_VERSION`**, not its package
version. The core can go 2.0 → 2.9 — new features, fixes, better prompts — and
your module keeps working, because the contract did not move.

If it ever does move, your module is **listed with the reason** and the app
still starts. You will always have a working app in which to fix it.

## Upgrading the core

```powershell
pip install -U nl2sql-engine --extra-index-url https://ephraimgoldin.github.io/nl2sql-engine/simple/
```

Your connections, semantic layers, learned examples and saved runs live in a
per-user folder (`%LOCALAPPDATA%\nl2sql` on Windows), not in the app. Upgrading
does not touch them.
