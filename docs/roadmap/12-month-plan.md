# Carlyle Global Wealth AI Platform: 12-Month Build Plan

> Supplied planning material, preserved for reference. Proposed architecture and targets are not confirmed company policies or systems. Source labels and illustrative snippets reflect the original pasted text; they have not been independently verified.

## 1. Executive recommendation
Based on the role description, the goal is not simply to build a chatbot or a collection of AI demos. The goal is to build a governed, reusable AI and data automation platform that replaces manual Global Wealth operational processes with reliable, auditable, production-grade workflows.

The strongest approach is to use GitHub as the engineering control plane for the initiative: source code, architecture decisions, business requirements, automated testing, deployment pipelines, security controls, and delivery tracking.

I would organize the work around five core capabilities:

## 1. Governed data and calculation foundation

Standardize source data, metric definitions, business rules, calculation logic, data contracts, and lineage across GPE, Credit, and AlpInvest.

## 2. Operational automation engine

Replace high-volume manual calculations, reconciliations, data preparation, and reasonability checks with repeatable, tested workflows.

## 3. Retrieval and semantic access layer

Give AI applications governed access to approved metric definitions, fund information, operational procedures, and investor-contextualized data.

## 4. Governance, controls, and observability

Implement permissions, approvals, data quality rules, exception management, audit trails, lineage, monitoring, and production release controls.

## 5. Reusable GitHub engineering platform

Establish standard repositories, CI/CD, infrastructure as code, testing templates, code reviews, release strategies, and reusable service patterns.

The key strategic decision is to build the data, calculation, and control foundation first, then deliver business-facing AI products on top of it. This creates immediate operational value while ensuring each subsequent product becomes cheaper and faster to build.

## 2. What should actually be built?
I would define six concrete deliverables. These are proposed solutions derived from the role description, not claims about Carlyle's existing systems or confirmed internal priorities.

Data Lineage | Collibra
Product 1 — Metric Registry and Calculation Engine
Foundation
A version-controlled catalog of business metrics, authoritative sources, calculation rules, dependencies, owners, approval status, and effective dates.

First use case: Automate one high-volume investor or fund reporting metric, with reconciliation against the existing manual result.

Operational Dashboard — Recon360
Product 2 — Reconciliation and Exception Workbench
First business product
A workflow that compares source data, calculated outputs, and expected results; flags discrepancies; assigns review tasks; and records resolution evidence.

First use case: Replace spreadsheet-based reasonability checks for the selected metric.

Can ChatGPT work with your enterprise data? | by Mechanics Team | Medium
Product 3 — Global Wealth Knowledge Assistant
AI application
A permission-aware assistant that answers questions about approved procedures, metric definitions, fund documentation, and operational policies with source citations.

First use case: Help an operations analyst understand how a metric is defined, where its inputs originate, and which procedure applies.

DirectionalData LLC | The AI-Ready Semantic Layer Practice
Product 4 — Semantic Data Access API
Shared platform
A governed interface exposing approved metrics and business concepts to internal applications and AI agents without requiring each application to reinvent business logic.

First use case: Let the knowledge assistant retrieve approved metric values and definitions through the same API used by operational applications.

Account Reconciliation Software - Vena
Product 5 — Reporting Preparation and Review Automation
Expansion
A controlled workflow for assembling approved data, running calculations, generating draft outputs, validating results, and routing exceptions for human approval.

First use case: Automate preparation of one recurring report or reporting package, with existing approval requirements preserved.

Four Zero Soft — Engineering Intelligent Systems for Scalable Businesses
Product 6 — AI Operations and Governance Console
Platform operations
A consolidated view of workflow status, failed runs, data freshness, quality exceptions, AI evaluation results, releases, audit evidence, and operational ownership.

First use case: Monitor every production workflow and provide operations teams with actionable failure and exception information.

Prioritization: Products 1 and 2 should lead. Products 3 and 4 should reuse their definitions and governed data access. Product 5 should expand only after the underlying calculations and controls are validated. Product 6 should be implemented incrementally as part of the platform rather than postponed until the end.

The first year should target multiple production releases, but not necessarily six independent applications. A small number of shared services and workflow components should power several visible business outcomes.

## 3. What to build in GitHub
My recommendation is to establish a dedicated GitHub organization or approved enterprise repository group for the platform, subject to Carlyle's existing technology standards. Start with a small number of well-defined repositories rather than one repository per product.

Recommended repository structure
global-wealth-ai-platform
Proposed platform organization / project root

global-wealth-ai-foundation

Metric definitions, calculation engine, data contracts, lineage, schemas, business rules and semantic models.

global-wealth-workflows

Reconciliation, exception management, reporting preparation, workflow orchestration and approval services.

global-wealth-ai-services

Retrieval, document ingestion, knowledge assistant, model integrations, AI evaluation and semantic access APIs.

global-wealth-platform-infra

AWS infrastructure as code, IAM, networking, environment configuration, observability, deployment and security policies.

global-wealth-architecture

Business requirements, process maps, architecture diagrams, ADRs, data dictionaries, control matrices, runbooks and operating procedures.

These are proposed repository names. Before creating them, check whether the enterprise already mandates a monorepo, shared infrastructure repository, service catalog, or approved internal developer platform.

What belongs in each repository?
The most important thing is to make business logic, data contracts, and deployment controls explicit and version-controlled.

Component

What to build

Business metric registry

Metric ID, definition, formula, unit, source, owner, effective date, approval status

Calculation engine

Deterministic, versioned functions with explicit inputs, outputs, precision, and rounding rules

Data contracts

Schemas, required fields, validation rules, ownership, freshness and compatibility rules

Reconciliation service

Expected-versus-actual comparisons, tolerances, discrepancy classification and evidence

Semantic API

Approved metric lookup, business entities, filters, contextual metadata and access enforcement

Retrieval service

Document ingestion, chunking, metadata, indexing, retrieval, citations and access filtering

Workflow orchestration

State transitions, retries, timeouts, approvals, idempotency and failure recovery

Audit and lineage

Source identifiers, transformation versions, calculation runs, reviewers and report outputs

Infrastructure

AWS resources, policies, secrets references, environment configuration and monitoring

Quality framework

Unit tests, integration tests, end-to-end tests, data quality tests and AI evaluation datasets

One crucial design rule: LLMs should explain, retrieve, classify, and assist; deterministic code should own authoritative financial calculations. An AI model should not silently substitute its own arithmetic or interpretation for an approved calculation rule.

Suggested application layout
For example, the foundation repository could look like this:


text

global-wealth-ai-foundation/
├── src/
│   ├── metrics/
│   │   ├── registry.py
│   │   ├── definitions.py
│   │   └── versioning.py
│   ├── calculations/
│   │   ├── engine.py
│   │   └── precision.py
│   ├── contracts/
│   │   ├── schemas.py
│   │   └── validation.py
│   ├── lineage/
│   │   └── events.py
│   └── api/
│       └── routes.py
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── contract/
│   └── fixtures/
├── docs/
│   ├── metric-definitions.md
│   ├── data-contracts.md
│   └── architecture.md
├── .github/
│   ├── CODEOWNERS
│   ├── pull_request_template.md
│   └── workflows/
│       ├── ci.yml
│       ├── security.yml
│       └── deploy.yml
├── pyproject.toml
├── Dockerfile
└── README.md
Python is a reasonable starting choice for data processing and AI services, with TypeScript or another approved language for interfaces where appropriate. The final language, frameworks, and repository boundaries should be confirmed against the firm's existing stack.

## 4. Target-state architecture
The architecture should separate source ingestion, trusted business logic, AI retrieval, application APIs, and human approval. That separation lets multiple products share the same foundation without duplicating calculations or bypassing controls.

## 1. Enterprise data and knowledge sources
Fund systems · Investor data · Finance data · Approved documents · Procedures

## 2. Ingestion and validation
AWS S3 · Lambda · Step Functions · Schema checks · Data quality · Quarantine

3A. Trusted data plane
Versioned calculations, metric registry, relational data, reconciliation and lineage.

3B. Knowledge plane
Document parsing, contextual metadata, retrieval indexes, embeddings and citations.

## 4. Governed service and access layer
API Gateway · ECS or Lambda · Identity and authorization · Semantic APIs · AI orchestration

Business applications

Operations workbench, reporting workflows, internal assistant.

Human control

Review queues, approvals, exception resolution and escalation.

Cross-cutting controls

Identity and access · Encryption · Secrets management · Audit logs · Lineage · Monitoring · Cost tracking · CI/CD · AI evaluation

Conceptual architecture, not a verified representation of Carlyle's current infrastructure. Exact AWS services, data stores, identity integrations, and network boundaries require internal discovery.

How the AWS services fit
Service

Recommended responsibility

S3

Raw, curated, and document storage with appropriate access boundaries

Lambda

Lightweight ingestion, validation, event handlers and API operations

Step Functions

Multi-step workflows, retries, approvals and recovery paths

ECS

Long-running services, heavier processing, and workloads unsuitable for Lambda

API Gateway

Authenticated API entry point, throttling and request controls

RDS

Relational metadata, metric definitions, workflow state and audit-related records where appropriate

GitHub Actions

Automated testing, security checks, artifact building and controlled deployment

Do not introduce every service simply because it appears in the job description. Choose each based on workload characteristics and the firm's existing platform. AWS recommends evaluating architecture across operational excellence, security, reliability, performance, cost, and sustainability. 

AWS Well-Architected Framework
+1

For long-running workflows, implement explicit retry, timeout, failure-catching, and recovery behavior rather than treating a successful deployment as proof of reliability. 

AWS Step Functions

The critical data design
Every production metric should have a defined contract, including:

Identity: Unique metric ID, fund/entity scope, period, currency, and relevant dimensions.

Definition: Business meaning, formula, units, sign convention, rounding and precision.

Sources: Authoritative systems, source fields, extraction timestamps, and data owners.

Validation: Required fields, freshness thresholds, tolerances, reconciliation rules, and exception severity.

Lineage: Source snapshot, transformation version, calculation version, run ID, and downstream output.

Governance: Business approver, technical owner, effective dates, change history, and permitted use.

For AI retrieval, attach metadata such as document type, fund, date, version, owner, confidentiality classification, and permissions. Apply authorization before returning retrieved content, not just after generating the answer.

The retrieval layer should distinguish between an approved definition, an operational procedure, an authoritative calculated value, and an unverified narrative. These are different kinds of evidence and must not be treated interchangeably.

## 5. GitHub engineering standards to implement from day one
GitHub should be more than a place to store source code. It should enforce how the team changes, tests, reviews, releases, and operates software.

Pull request and release workflow
1
Create issue
Business requirement, acceptance criteria, owner and risk classification

2
Open feature branch and pull request
Small change, linked issue, peer review and business-rule evidence

3
Automated quality gates
Unit, integration, contract, data-quality, security and AI evaluation tests

4
Deploy to development / staging
Infrastructure validation, integration checks and synthetic test data

5
Obtain production approval
Authorized reviewer, change evidence and rollback plan

6
Canary or controlled production release
Health checks, metrics, error monitoring and rollback triggers

Minimum controls for every repository
Protect the default branch; require pull requests and designated reviewers.

Require passing CI checks before merging.

Assign CODEOWNERS for calculation logic, security-sensitive code, infrastructure, and shared contracts.

Use GitHub Actions with minimal permissions, trusted and pinned dependencies, and short-lived cloud credentials where supported.

Keep secrets and investor data out of source code, logs, pull request artifacts, and test fixtures.

Use protected deployment environments and explicit production approval.

Build immutable, versioned artifacts and promote the same artifact through environments.

Add dependency scanning, secret scanning, code scanning, and software composition checks as supported by the approved enterprise tooling.

Define rollback, feature-flag, and incident-response procedures for each production service.

GitHub's documentation specifically recommends hardening workflow dependencies and permissions, while deployment environments can enforce required reviews and restrict production deployment access. 

GitHub Docs
+2

Initial CI pipeline
The following is a starter design for the foundation repository, not a production-ready deployment workflow.


yaml

name: Foundation CI

on:
  pull_request:
  push:
    branches: [main]

permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -e ".[dev]"
      - run: ruff check .
      - run: mypy src
      - run: pytest tests/unit --cov=src --cov-report=term-missing
      - run: pytest tests/contract
Before adopting this example, pin third-party actions to verified full commit SHAs, use the approved runner and dependency-management strategy, and replace the illustrative test commands with the actual project configuration. Add integration tests using isolated test infrastructure, rather than relying on unit tests alone.

## 6. The first 90 days: exactly what to do
The first three months should establish credibility through one real business outcome, not a long architecture exercise.

Days 1–30
Discover and design

Outcome: an approved problem, architecture, and delivery backlog.

Meet Client Solutions Group, Finance, Fund Management, GPE, Credit, AlpInvest, security, and platform stakeholders.

Map three to five candidate manual workflows and their source systems, calculations, spreadsheets, review steps, and failure modes.

Inventory the most frequently used metrics and identify discrepancies in definitions.

Score opportunities by volume, hours saved, error exposure, data readiness, and implementation complexity.

Establish the GitHub repositories, ADR template, issue taxonomy, CI baseline, and initial architecture diagram.

Obtain agreement on one pilot, its business owner, its expected outcomes, and its approval controls.

Deliverables: Current-state process maps, prioritized use-case backlog, target-state architecture, metric specification, and pilot acceptance criteria.

Days 31–60
Build the foundation

Outcome: the first calculation pipeline and reconciliation prototype.

Implement the first metric definition and calculation as deterministic, tested code.

Create input schemas, validation rules, versioned outputs, and data lineage records.

Build a sample ingestion-to-calculation workflow using synthetic or approved non-production data.

Implement reconciliation against an approved reference result and surface mismatches as structured exceptions.

Provision the required development infrastructure using the approved infrastructure-as-code tooling.

Establish CI, test fixtures, logs, dashboards, and an auditable execution record.

Deliverables: Working calculation engine, metric registry MVP, automated tests, reconciliation prototype, and repeatable deployment pipeline.

Days 61–90
Pilot and prove

Outcome: a controlled pilot ready for a production decision.

Run the new workflow against representative historical cases and compare outputs with the existing process.

Test edge cases, missing data, duplicate events, stale inputs, rounding, exceptions, and recovery.

Implement reviewer sign-off and preserve evidence for discrepancies and resolutions.

Pilot with a small group of business users in shadow mode, without replacing the authoritative process prematurely.

Measure processing time, exception rates, calculation agreement, and user feedback.

Complete security, operational-readiness, and production-approval reviews.

Deliverables: Pilot results, quantified baseline-versus-target comparison, operational runbook, remediation backlog, and production go/no-go recommendation.

The exact first use case must be selected through discovery. Do not assume that a particular fund, metric, or reporting process is the highest-value opportunity without validating it with process owners.

## 7. Twelve-month delivery roadmap
The first 90 days establish the initial product. The remaining nine months should scale the proven patterns across additional workflows and business areas.

Q1
Discover
Foundation and first pilot

Approved architecture and operating model.

Metric registry and calculation framework MVP.

First reconciliation workflow in shadow mode.

GitHub CI/CD, security baseline, and documented requirements.

Success evidence: a validated pilot, documented baseline, and a clear production decision.

Q2
Launch
First production product and reusable retrieval

Release the first controlled operational automation to production.

Launch the exception workbench and reviewer workflow.

Build the document ingestion and retrieval foundation.

Deliver an internal knowledge assistant for an approved, limited use case.

Success evidence: real users, measured time savings, approved controls, monitoring, and support ownership.

Q3
Scale
Reusable semantic access and multiple workflows

Add governed metric APIs and reusable data contracts.

Onboard additional metrics or workflows based on measured value.

Extend retrieval to additional approved document sets.

Introduce automated reporting preparation where dependencies and controls are ready.

Success evidence: multiple production use cases sharing the same foundation rather than separate bespoke implementations.

Q4
Institutionalize
Enterprise adoption and target-state architecture

Expand successful patterns across eligible GPE, Credit, and AlpInvest processes.

Establish standard onboarding templates for new metrics and funds.

Complete lineage, operational monitoring, ownership, and governance gaps.

Publish reference architectures, engineering standards, and a prioritized next-year roadmap.

Success evidence: multiple production products, demonstrable efficiency improvements, reusable architecture, and business-sponsored expansion.

These are proposed milestones, not guaranteed delivery dates. Production timelines will depend on data access, business approvals, security reviews, existing platform constraints, and the size of the delivery team.

## 8. What success should be measured against
The job description defines qualitative success but does not supply numeric targets. I would establish baselines during the first month, agree on targets with the business sponsors, and report progress monthly.

KPI

What to measure

Illustrative first-year objective

Production delivery

Distinct AI-enabled products and workflows in real use

3–5 meaningful production releases, subject to scope

Operational efficiency

Processing time and manual touchpoints per case

30–50% reduction for selected workflows

Calculation integrity

Agreement with approved reference results

100% agreement on defined deterministic test cases; all production discrepancies investigated

Data quality

Completeness, freshness, reconciliation exceptions

Agreed thresholds for each onboarded metric

AI reliability

Retrieval correctness, citation support, access-control failures

Approved evaluation thresholds; zero known unauthorized disclosure

Reusability

Time required to onboard a subsequent metric or workflow

Demonstrable reduction from the initial pilot baseline

Engineering quality

Automated test coverage, deployment failures, recovery time

Required critical-path tests, monitored releases, documented recovery procedures

Adoption

Active users, workflow usage, user feedback

Sustained usage by designated business teams

Governance

Approved definitions, traceable calculations, assigned owners

Complete required lineage and approvals for every production metric

The numerical objectives above are starting proposals, not established company targets. For example, the reduction in processing time should be calculated from a documented baseline and should not be achieved by removing required review controls.

How to calculate business value
Use a consistent formula for each workflow:

Annual hours saved
=
N
×
T
before
−
T
after
60
Annual hours saved=N× 
60
T 
before
​
 −T 
after
​
 
​
 
Where:

N
N is the annual number of cases processed.

T
before
T 
before
​
  is the average manual processing time in minutes.

T
after
T 
after
​
  is the average processing time after automation, including necessary human review.

Then calculate estimated annual labor value by multiplying hours saved by the agreed fully loaded hourly cost. Report risk reduction separately unless Finance approves a defensible methodology for valuing it.

This makes the business case credible and lets leadership compare automation opportunities objectively.

## 9. Business discovery: what needs to be researched internally
Public research can inform engineering standards, but it cannot establish Carlyle's current processes, data ownership, system integrations, or approved architecture. Those must be investigated with the people who operate the business.

Use a structured discovery backlog.

Discovery checklist
0 / 15 questions reviewed

Process inventory
Primary stakeholders: Fund Management and Operations


Which workflows are most frequent and labor-intensive?

Which processes have deadlines, escalations, or investor-facing outputs?

Where do spreadsheets, email handoffs, and manual approvals occur?
Calculation definitions
Primary stakeholders: Finance and metric owners


Which formulas and rounding conventions are authoritative?

Which definitions differ between funds, products, or teams?

How are historical corrections and restatements handled?
Data architecture
Primary stakeholders: Enterprise and data architects


Which source systems own each field?

How are data freshness, identifiers, and historical snapshots handled?

What AWS, database, API, and data platform capabilities already exist?
AI and information governance
Primary stakeholders: Security, Risk, Legal, and data owners


Which models and retrieval services are approved?

What restrictions govern investor data and confidential fund documents?

What audit, retention, human-review, and AI evaluation requirements apply?
Delivery and adoption
Primary stakeholders: Product managers and engineering leadership


Which teams own development, deployment, and production support?

What GitHub, CI/CD, incident management, and observability standards are mandatory?

Who approves process changes and retires the manual process?
The most important output from this work is a business-approved inventory linking each candidate workflow to its volume, current effort, authoritative data, calculation logic, risks, owner, and target-state requirements.

## 10. External research and technical standards
I reviewed primary documentation relevant to the architecture and delivery model. These sources help establish implementation principles; they do not confirm what Carlyle has already deployed.


AWS Well-Architected Framework

Provides guidance for designing and operating secure, reliable, observable, and cost-effective cloud workloads. Use it to review the target architecture and deployment decisions.

Source: AWS documentation

Read the AWS Well-Architected Framework  

AWS Well-Architected Framework


AWS Step Functions error handling

Documents retries, timeouts, catchers, and recovery patterns. These are directly relevant to production financial workflows that must handle transient failures without silently losing work.

Read the Step Functions error-handling guide  

AWS Step Functions


GitHub Actions security

Covers permissions, dependency trust, secrets, and workflow hardening. Apply these practices before allowing CI/CD to access sensitive environments or deploy infrastructure.

Read GitHub Actions security guidance  

GitHub Docs


GitHub deployment environments

Explains deployment protection rules, required reviewers, and environment-specific access. These capabilities can support controlled promotion to production.

Read GitHub deployment environment documentation  

GitHub


NIST AI Risk Management Framework

Provides a framework for identifying, assessing, and managing AI risks throughout the lifecycle. Use it as a reference for AI evaluation, oversight, documentation, and governance, adapted to Carlyle's actual policies.

Read the NIST AI Risk Management Framework  

NIST

## 11. What I would create in GitHub during week one
Before building an AI model or deploying AWS infrastructure, create the initial delivery and governance artifacts:

README.md — Platform mission, scope, system boundaries, and getting started.

docs/architecture/target-state.md — Proposed architecture and open design decisions.

docs/discovery/process-inventory.md — Current-state workflows and owners.

docs/data/metric-registry-schema.md — Required fields and governance for metric definitions.

docs/governance/control-matrix.md — Access, approvals, reconciliation, lineage, and retention requirements.

docs/product/use-case-prioritization.md — Scoring model and candidate pilot selection.

docs/roadmap/12-month-plan.md — Quarterly outcomes, dependencies, and success metrics.

docs/decisions/ADR-0001-repository-strategy.md — Monorepo versus multiple repositories.

.github/ISSUE_TEMPLATE/ — Templates for features, data defects, architecture decisions, and production incidents.

.github/pull_request_template.md — Testing evidence, business impact, risk, and rollback requirements.

Create GitHub Projects views for discovery, ready-to-build work, delivery, governance blockers, production incidents, and quarterly milestones. Link each feature to a business outcome and each production release to its acceptance criteria.

Do not commit real investor information, production extracts, credentials, or confidential documents to the repository. Use synthetic fixtures and approved secure data environments for development and testing.

## 12. The leadership strategy
The role is approximately 30% discovery, 50% architecture and delivery, and 20% leadership and governance. Your operating rhythm should reflect that distribution.

Business discovery: Run structured process walkthroughs and maintain a prioritized, business-approved backlog.

Architecture and delivery: Personally lead the design of shared foundations, review critical code, and ensure at least one end-to-end production outcome is delivered early.

Leadership and governance: Establish engineering standards, delegate bounded components to senior developers, maintain architecture decisions, and report outcomes and risks to leadership.

A practical cadence would be weekly delivery reviews, regular business-owner demonstrations, architecture and code reviews, monthly sponsor updates, and quarterly target-state architecture reviews.

Given the four-day in-office requirement, use in-person time for process walkthroughs, design workshops, decisions involving multiple stakeholders, and product demonstrations. Reserve focused engineering work for uninterrupted implementation and review time.

Final recommendation
If I were starting this role, I would make the first major investment a reusable, version-controlled metric and calculation foundation, paired with a reconciliation and exception workflow.

I would then use that foundation to deliver a permission-aware knowledge assistant and semantic API, followed by additional automated reporting workflows. Every release would use the same testing, security, deployment, lineage, and operational controls.

That strategy addresses the three outcomes that matter most:

Visible business impact: Multiple real products replacing manual work, with measurable results.

Enterprise architecture: A reusable, governed data and retrieval foundation for future AI initiatives.

Technical leadership: A disciplined GitHub engineering platform that lets the team deliver faster without compromising reliability or control.

The guiding principle is simple: build one real workflow end to end, prove the business value, turn the implementation into a reusable pattern, and repeat.