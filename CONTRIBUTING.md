# Contributing

1. Open an issue using the appropriate template; state the business outcome and acceptance evidence.
2. Create a short-lived feature branch (for example `codex/metric-contract`).
3. Make a small change and update the relevant contracts, decisions, and documentation.
4. Run `python3 scripts/check_docs.py`; include results in the pull request.
5. For executable components, add meaningful unit, contract, integration, and failure-path checks before release.
6. Request review from the relevant owner. Calculation definitions require business approval as well as technical review.

Use synthetic fixtures. Do not use public issues for confidential incidents or vulnerabilities. Never claim a proposed control is enforced until its configuration and evidence have been verified.
