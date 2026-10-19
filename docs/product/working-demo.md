# Working demo: calculation to review

## Implemented

- Explicit registry lookup for `synthetic_nav` version `1.0.0`; the only allowlisted formula is assets minus liabilities.
- Immutable in-memory metric definition, decimal arithmetic, cents precision with half-even rounding, and an inclusive absolute tolerance of 0.01 USD.
- Strict snapshot field set, synthetic-only flag, USD currency, version and identifier checks, effective dates, timezone-aware extraction, 24-hour freshness, and nonnegative assets/liabilities.
- Decimal strings with at most 18 integer and six fractional digits. Floats, exponents, non-finite values, and extra fields are rejected. Reference results must already be rounded to cents.
- Atomic SQLite run insertion, source/metric hashes, source snapshot, metric definition, engine version, and timestamp.
- Idempotent replay by run ID and fingerprint; a changed source, metric, or actor is rejected under the same run ID. Replay returns the historical run without recalculating freshness. A new ID revalidates the input.
- Matched and exception results both require review. A different reviewer label and evidence are required. Reviews are final through this API; corrections use a new run. Review never erases the original discrepancy.
- CLI JSON output with exit code 0 on success, 2 on invalid input or storage errors. An exception is a successful workflow result needing review, not a CLI failure.

## Contract

See [matched input](../../examples/matched.json) and [exception input](../../examples/exception.json). The reference value shares the snapshot's entity, currency, and period. This prototype trusts that association; it does not retrieve or independently authenticate source/reference systems.

## Boundaries

This metric is marked `demo_only`, not business approved. The synthetic flag is a caller assertion, not a data-loss-prevention control. No real data belongs in this repository or demo.

CLI actors and reviewer names are not authenticated. SQLite files are editable by their local owner; hashes provide reproducible provenance, not tamper-proof audit storage. There is no network API, tenant isolation, encryption layer, external publication, cloud deployment, or LLM service. A reviewer may accept an exception with evidence; the recorded discrepancy remains visible. Production exception policy must be independently defined.

The supplied architecture remains the target. Next steps are a business-approved metric and reference corpus, authenticated authorization, controlled exception policies, database migrations and retention, operational recovery, then permission-aware retrieval. No project board or branch-protection rules have been provisioned.

## Verification

Run `PYTHONPATH=src python3 -m unittest discover -s tests -v` and `python3 scripts/check_docs.py`. The suite covers valid and invalid contracts, timezone/freshness boundaries, rounding, tolerances, idempotency conflicts, persistence, reviewer rules, and command-line execution. GitHub Actions runs the same commands on Ubuntu 24.04's Python.
