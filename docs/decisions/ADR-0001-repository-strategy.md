# ADR-0001: Start with one public reference repository

Date: 2026-10-19

Status: accepted for this starter; enterprise topology remains undecided.

## Context

The supplied plan proposes foundation, workflow, AI services, infrastructure, and architecture repositories. The requested deliverable is one public repository under Skeeb32.

## Decision

Keep the plan, documentation, contribution templates, and component briefs together in `global-wealth-ai-platform`. Use folders to express boundaries until independently deployed components or ownership justify separation.

## Consequences

The starter is easy to inspect and evolve. Public content is limited to reference material and synthetic examples. Production code/data placement, private repositories, and enterprise policies require separate decisions. This public repository grants no access to enterprise systems.
