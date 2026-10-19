# GitHub configuration checklist

Repository files alone do not enforce GitHub settings. These items must be configured and verified separately; this starter does not claim they are enabled.

- Protect `main` with pull requests, required reviewers, and required passing checks.
- Require code-owner review where supported; the sole maintainer cannot independently review their own changes.
- Enable approved dependency, code, and secret scanning capabilities.
- Add a CI workflow after selecting the runner and dependency strategy; pin third-party actions to verified full commit SHAs and use minimal permissions.
- Run the existing documentation validator in CI; add executable tests as components are implemented.
- Configure protected staging and production environments, independent approvals, and short-lived deployment credentials before deployment workflows are introduced.
- Build immutable artifacts and promote the same version between environments.
- Configure private vulnerability reporting where supported.
- Create delivery views for discovery, ready, delivery, governance blockers, incidents, and quarterly milestones. Keep sensitive incident details private.

No Actions workflow, deployment environment, branch protection, or GitHub Project is provisioned by these files.
