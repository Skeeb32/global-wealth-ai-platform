# Metric registry contract

Status: proposed schema requirements; no metric is approved by this document.

| Group | Required fields and meaning |
|---|---|
| Identity | metric_id, version, entity_scope, period, currency, dimensions |
| Definition | business_definition, formula_reference, units, sign_convention, decimal_precision, rounding_mode |
| Sources | source_system, source_fields, snapshot_id, extracted_at, data_owner |
| Validation | required_fields, freshness_threshold, tolerances, reconciliation_rule, exception_severity |
| Lineage | transformation_version, calculation_version, run_id, downstream_outputs |
| Governance | technical_owner, business_approver, approval_status, effective_from, effective_to, permitted_use, change_history |

Use decimal representations for monetary values and explicit rounding at defined boundaries. Reject missing required data, incompatible currency/period/entity scope, stale inputs, ambiguous versions, and non-finite values. Do not silently coerce invalid values or select an unapproved formula.

Version changes must define compatibility and historical recomputation behavior. Preserve the source snapshot and exact rule used for each output. Approval lifecycle: draft → reviewed → approved → retired; production accepts only the approved version effective for the requested period.

The first executable schema and formula must be derived from a business-approved pilot specification. Synthetic fixtures should exercise missing data, duplicates, boundary rounding, stale records, and corrections.
