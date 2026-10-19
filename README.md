# Global Wealth AI Platform

Independent reference project for a governed data and AI platform, based on the supplied **Carlyle Global Wealth AI Platform: 12-Month Build Plan**. This is not an official Carlyle repository, endorsement, or representation of its internal systems.

## Status and scope

Working local Python demo plus planning and governance starter. Includes a versioned synthetic metric, strict input validation, decimal calculations, reconciliation, SQLite persistence, and a review workflow. No production services, business-approved financial formulas, cloud resources, investor data, or live AI integrations are included. Proposed outcomes and targets require discovery and business approval.

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

`src/wealth_platform/` contains the working library and command-line interface. The other `src/` folders describe future component boundaries. `tests/test_workflow.py` covers contracts, calculations, persistence, and the CLI. `examples/` contains synthetic match and exception cases. `.github/workflows/ci.yml` runs documentation and test checks with read-only repository permissions. No deployment workflow is enabled.

## Validate the starter

Requires Python 3.10 or later; no third-party dependencies.

```sh
python3 scripts/check_docs.py
```

This checks local Markdown links and required starter artifacts. Run the executable suite with `PYTHONPATH=src python3 -m unittest discover -s tests -v`. These checks do not establish production readiness.

## Public repository boundary

Use synthetic examples only. Do not upload investor details, internal documents, production extracts, credentials, or sensitive incident evidence. Public issue templates ask for sanitized summaries. See [SECURITY.md](SECURITY.md).

## Run the working demo

From the repository root, with Python 3.10 or later (no external runtime dependencies):

```sh
export PYTHONPATH=src
python3 -m wealth_platform metrics
python3 -m wealth_platform run examples/matched.json --run-id demo-match --actor analyst --as-of 2026-10-19T12:00:00Z
python3 -m wealth_platform run examples/exception.json --run-id demo-exception --actor analyst --as-of 2026-10-19T12:00:00Z
python3 -m wealth_platform review demo-exception --reviewer reviewer --decision rejected --evidence "Synthetic reference differs by 100 USD; investigate source."
python3 -m wealth_platform runs
python3 -m wealth_platform show demo-exception
```

The matched example produces `1000000.00` USD; the exception example preserves a `100.00` USD difference. Both start in `pending_review`. The demo clock keeps the dated fixtures repeatable; omit it to enforce freshness against the current clock.

Results are stored in ignored `demo.sqlite3`. Use `--db /path/to/demo.sqlite3` **before** the subcommand to select another database. Repeating the same run ID and inputs returns the existing result; changed inputs require a new run ID.

See [demo behavior and limitations](docs/product/working-demo.md). Reviewer names are self-declared CLI labels, not authenticated identities. This is a synthetic local prototype, not a production approval system.
