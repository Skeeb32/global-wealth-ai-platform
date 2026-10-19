# Pilot operations readiness

Before shadow runs, identify a service owner and escalation route, define failure alerts and response targets, and record the approved reference process.

On a failed run: preserve sanitized run ID and lineage, prevent publication, classify invalid input versus transient infrastructure failure, and route to the responsible owner. Retry only with defined bounds and idempotency. Reconcile any replay against the same source snapshot and rule version.

Rollback must identify the prior artifact/configuration, restore the approved workflow, verify output agreement, and preserve review evidence. Never resolve a discrepancy by changing expected results without business approval.

Production gate: tested recovery, assigned support, monitoring, retention, authorization, and business sign-off. None is implemented by this runbook alone.
