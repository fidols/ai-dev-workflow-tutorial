# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

This is a **documentation-only tutorial repository** — it contains Markdown instructional content and sample data, not application code. There are no build, lint, or test commands. All content is plain Markdown files.

Students fork this repo and build a Streamlit sales dashboard inside their fork, following the workflow taught in the tutorial materials.

## Repository structure

```
v2/                        # Current tutorial (use this)
  pre-work-setup.md        # Student pre-work: accounts, tools, fork/clone (~60-90 min)
  workshop-build-deploy.md # Live workshop: spec-kit → Jira → build → deploy (~3 hours)

v1/                        # Original multi-document version (legacy, kept for reference)
  00-overview.md through 08-glossary.md

prd/ecommerce-analytics.md # The PRD students build from (ShopSmart e-commerce dashboard)
data/sales-data.csv        # Sample dataset used in the dashboard
```

## Workflow taught in this tutorial

The tutorial teaches this end-to-end professional dev workflow:

1. **PRD** (written) → **spec-kit** (Claude generates constitution, spec, plan, tasks) → **Jira** (task tracking)
2. **Claude Code** (AI-assisted coding) → **Git commit/push** → **Streamlit Cloud** (deploy live)

Key tools introduced: GitHub, Jira/Atlassian, Cursor, Claude Code, [spec-kit](https://github.com/github/spec-kit), Python + Streamlit, `uv` (Python package manager).

## Editing guidelines

- **v2 is current** — all improvements go to `v2/pre-work-setup.md` and `v2/workshop-build-deploy.md`
- **v1 is legacy** — do not update v1 files unless specifically asked
- UI instructions go stale quickly; the tutorial includes a standing caveat about evolving UIs — preserve this
- The PRD (`prd/ecommerce-analytics.md`) is intentionally written as a student-facing artifact, not a real internal doc

## Active Technologies
- Python 3.11+ + streamlit, pandas, plotly, (managed via `uv`) (001-sales-dashboard)
- CSV file — `data/sales-data.csv` (read-only, no database) (001-sales-dashboard)

## Recent Changes
- 001-sales-dashboard: Added Python 3.11+ + streamlit, pandas, plotly, (managed via `uv`)
