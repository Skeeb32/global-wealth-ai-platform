# Proposed control matrix

All controls below are requirements to implement and verify, not claims of enforcement by this starter.

| Control | Proposed accountable role | Required evidence | Release gate |
|---|---|---|---|
| Approved metric definition | Business metric owner | Signed version and effective dates | Before calculation release |
| Deterministic calculation | Engineering lead | Reference and edge-case test results | Before pilot |
| Reconciliation | Operations owner | Tolerances, mismatch queue, resolution history | Before production |
| Access enforcement | Security owner | Negative authorization tests at retrieval and API boundaries | Before data access |
| Lineage | Data owner | Source snapshot to output trace | Every production run |
| Human approval | Process owner | Reviewer identity, decision and timestamp | Before authoritative publication |
| Retention | Governance owner | Approved schedule and deletion verification | Before live storage |
| Release controls | Platform owner | CI checks, review, immutable artifact and rollback evidence | Every release |
| Monitoring and recovery | Service owner | Alerts, runbook, recovery exercise | Before production |
| AI evaluation | AI service owner | Citation, retrieval, refusal and permission evaluation evidence | Before model/prompt/index changes |

Assign actual people during discovery. Confidential evidence remains in approved private systems.
