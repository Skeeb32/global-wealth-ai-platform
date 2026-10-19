# Global Wealth AI Platform

Independent reference project for a governed data and AI platform, based on the supplied **Carlyle Global Wealth AI Platform: 12-Month Build Plan**. This is not an official Carlyle repository, endorsement, or representation of its internal systems.

## Status and scope

Planning and engineering starter. No production services, approved financial formulas, cloud resources, investor data, or live AI integrations are included. Proposed outcomes and targets require discovery and business approval.

Start with a metric registry and deterministic calculation foundation, then reconciliation and exception handling. Add permission-aware retrieval and semantic APIs after the underlying definitions and controls are proven.

## Start here

- [Full supplied build plan](docs/roadmap/12-month-plan.md)
- [Target architecture](docs/architecture/target-state.md)
- [First 90 days and acceptance gates](docs/product/first-90-days.md)
- [Discovery inventory](docs/discovery/process-inventory.md)
- [Pilot prioritization](docs/product/use-case-prioritization.md)
- [Metric contracts](docs/data/metric-registry-schema.md)
- [Control matrix](docs/governance/control-matrix.md)
- [Repository decision](docs/decisions/ADR-0001-repository-strategy.md)
- [GitHub setup checklist](docs/governance/github-setup.md)
- [Contribution guide](CONTRIBUTING.md)

## Project layout

`src/` defines the intended component boundaries; each component currently contains a design brief. `tests/` defines the planned validation layers. `infra/` records deployment prerequisites. `.github/` contains ownership and contribution templates. No deployment workflow is enabled.

## Validate the starter

Requires Python 3.10 or later; no third-party dependencies.

```sh
python3 scripts/check_docs.py
```

This checks local Markdown links and required starter artifacts. It is not a financial calculation test or a production readiness assessment.

## Public repository boundary

Use synthetic examples only. Do not upload investor details, internal documents, production extracts, credentials, or sensitive incident evidence. Public issue templates ask for sanitized summaries. See [SECURITY.md](SECURITY.md).
