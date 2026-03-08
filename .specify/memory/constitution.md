<!--
SYNC IMPACT REPORT
==================
Version change: (unversioned template) → 1.0.0
Bump rationale: MAJOR — initial ratification; all placeholders replaced with concrete values.

Modified principles:
  - [PRINCIPLE_1_NAME] → I. Data Fidelity (NON-NEGOTIABLE)
  - [PRINCIPLE_2_NAME] → II. Spec-First Development
  - [PRINCIPLE_3_NAME] → III. Reproducible Environment
  - [PRINCIPLE_4_NAME] → IV. Simplicity
  - [PRINCIPLE_5_NAME] → V. Transparency for Technical Users

Added sections:
  - Technology Stack
  - Development Workflow

Removed sections: none

Templates reviewed:
  - .specify/templates/plan-template.md    ✅ Constitution Check section aligns with principles
  - .specify/templates/spec-template.md    ✅ Mandatory sections (user stories, requirements, success criteria) align
  - .specify/templates/tasks-template.md   ✅ Phase structure and story independence align with Spec-First principle

Deferred TODOs: none
-->

# E-Commerce Analytics Dashboard Constitution

## Core Principles

### I. Data Fidelity (NON-NEGOTIABLE)

Visualizations MUST faithfully represent the underlying source data at all times.
No sampling, silent rounding, or approximations are permitted without explicit,
visible disclosure in the UI. All aggregations (sums, averages, filtered totals)
MUST be labeled with their scope and logic so a technical user can independently
verify any displayed number. When data is unavailable or ambiguous, the dashboard
MUST surface an explicit error or "no data" state rather than displaying a zero or
a partial result silently.

**Rationale**: The primary audience is the data/analytics team. Any visualiza-
tion that cannot be trusted as an exact representation of the data destroys the
dashboard's core value and erodes user confidence.

### II. Spec-First Development

Every feature MUST have an approved written specification (spec.md) before any
implementation code is written. Prototyping, exploratory coding, or "let me
just try it" approaches are not permitted as a substitute for a spec. The spec
MUST define user stories with acceptance scenarios and measurable success criteria
before work begins.

**Rationale**: Spec-first discipline prevents scope creep, keeps the team aligned,
and produces a durable record of intent that supports future audits and amendments.

### III. Reproducible Environment

All Python dependencies MUST be managed via `uv` with a committed `uv.lock` file.
No dependency may be installed outside of `uv sync`. Implicit upgrades are
prohibited — the lockfile is the source of truth. Any environment MUST be fully
reproducible by running `uv sync` from a clean checkout with no additional steps.

**Rationale**: Reproducibility eliminates "works on my machine" failures and
ensures that Streamlit Cloud deployments match local development exactly.

### IV. Simplicity

Implementation MUST use the minimum viable complexity for each requirement.
Premature abstractions, helper utilities for one-time operations, and
over-engineered patterns are prohibited. Any complexity beyond the straightforward
path MUST be explicitly justified in the plan with a documented rationale.
YAGNI (You Aren't Gonna Need It) is the default stance.

**Rationale**: A dashboard codebase that stays simple is easier to audit, extend,
and hand off. Complexity introduced without justification compounds over time.

### V. Transparency for Technical Users

Every chart and summary metric MUST expose access to the underlying raw data
(e.g., a data table view, a download link, or a clearly documented filter state).
No metric may be presented without a visible definition of how it is calculated.
Technical users MUST be able to inspect, validate, and export any displayed value.

**Rationale**: The audience is data/analytics professionals who routinely validate
dashboards against source systems. Opaque visualizations undermine their workflow.

## Technology Stack

- **Language**: Python 3.11+
- **UI Framework**: Streamlit
- **Data Processing**: pandas
- **Package Manager**: `uv` (lockfile committed; `uv sync` is the only install method)
- **Data Source**: CSV files (e.g., `data/sales-data.csv`); no live database connections
  assumed unless specified in a feature spec
- **Deployment Target**: Streamlit Cloud

Any addition to the stack MUST be approved via a constitution amendment before
it is introduced into a feature spec.

## Development Workflow

1. **Spec** — Author `spec.md` with user stories, acceptance scenarios, and
   success criteria. Spec MUST be reviewed and approved before proceeding.
2. **Plan** — Run `/speckit.plan` to produce `plan.md`, `research.md`, and
   `data-model.md`. Constitution Check gate MUST pass.
3. **Tasks** — Run `/speckit.tasks` to generate `tasks.md`. Tasks are ordered
   by dependency and user story priority.
4. **Implement** — Execute tasks in order. Each user story MUST be independently
   testable at its checkpoint before the next story begins.
5. **Deploy** — Push to GitHub; Streamlit Cloud auto-deploys from `main`.

Skipping or reordering steps MUST be documented as a governance exception in
the relevant plan.md.

## Governance

This constitution supersedes all other practices, conventions, and tribal knowledge
for the E-Commerce Analytics Dashboard project. Any conflict between a feature
spec, plan, or task list and this constitution MUST be resolved in favor of the
constitution or escalated as an amendment.

**Amendment procedure**:
1. Propose the change with a written rationale.
2. Identify all affected downstream artifacts (templates, specs, plans, tasks).
3. Update this constitution and increment the version per semantic versioning rules.
4. Propagate changes to all affected artifacts before the amendment is considered
   ratified.

**Versioning policy**:
- MAJOR: Principle removed, renamed, or fundamentally redefined.
- MINOR: New principle or section added; material expansion of existing guidance.
- PATCH: Clarifications, wording improvements, typo fixes.

**Compliance review**: Every feature plan MUST include a Constitution Check section
that explicitly verifies compliance with each principle before implementation begins.

**Version**: 1.0.0 | **Ratified**: 2026-03-07 | **Last Amended**: 2026-03-07
