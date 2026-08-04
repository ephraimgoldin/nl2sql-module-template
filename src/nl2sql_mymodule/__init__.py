# -*- coding: utf-8 -*-
"""Your module. It profiles a table; change it to do whatever you need.

Everything here is ordinary Python in an ordinary pip package. There is no
import from the app, no file edited in the engine, and no entry in any list.
`pip install .` makes this page appear in BOTH the Streamlit and the React app;
`pip uninstall nl2sql-eda` removes it.

Copy this directory, rename it, and change what run() does.
"""
from nl2sql_engine.modules import Action, Input, Module, Result


def profile(ctx, table: str, limit: int = 10) -> Result:
    """One row per column: its type, how many values are missing, how many differ.

    `ctx` is the whole surface a module gets — deliberately small, and versioned.
    ctx.query() goes through the same read-only guardrail as every other query
    in the app, because a module is student-written code and that is precisely
    why it does not get a private route to the database.
    """
    cols, _ = ctx.query(f'SELECT * FROM "{table}" LIMIT 0')
    total = ctx.query(f'SELECT count(*) FROM "{table}"')[1][0][0]
    rows = []
    for c in cols:
        _, r = ctx.query(
            f'SELECT count("{c}"), count(DISTINCT "{c}") FROM "{table}"')
        present, distinct = r[0]
        rows.append([c, total - present, distinct,
                     round(100.0 * distinct / total, 1) if total else 0.0])
    return Result.table(
        rows, ["column", "missing", "distinct", "distinct %"],
        title=f"{table} — {len(cols)} columns, {total:,} rows",
        note="A column with one distinct value carries no information; a column "
             "whose distinct count equals the row count is an identifier.")


MODULE = Module(
    name="eda",
    label="🔎 Exploratory analysis",
    description="Profile a table before trusting a query written against it.",
    # Against API_VERSION, not the package version. This module keeps working
    # across every 2.x core, because the CONTRACT is what it depends on.
    requires_core=">=1.0,<2.0",
    actions=[
        Action(name="profile", label="Profile a table", run=profile,
               help="Counts missing and distinct values per column.",
               inputs={
                   "table": Input(kind="table", label="Table"),
                   "limit": Input(kind="number", label="Sample rows", default=10),
               }),
    ],
)
