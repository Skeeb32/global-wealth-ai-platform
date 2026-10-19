# GitHub configuration checklist

Repository files alone do not enforce GitHub settings. These items must be configured and verified separately; this starter does not claim they are enabled.

- Protect `main` with pull requests, required reviewers, and required passing checks.
- Require code-owner review where supported; the sole maintainer cannot independently review their own changes.
- Enable approved dependency, code, and secret scanning capabilities.
- The Foundation CI workflow runs documentation checks and the executable suite on Ubuntu 24.04 with read-only contents permission and a verified pinned checkout action. Review runner policy before enterprise adoption.
- Make the Foundation CI check required in branch rules after verifying its first successful run. Extend tests as components are implemented.
- Configure protected staging and production environments, independent approvals, and short-lived deployment credentials before deployment workflows are introduced.
- Build immutable artifacts and promote the same version between environments.
- Configure private vulnerability reporting where supported.
- Create delivery views for discovery, ready, delivery, governance blockers, incidents, and quarterly milestones. Keep sensitive incident details private.

The Actions workflow is included. Deployment environments, branch protection, and GitHub Projects are not provisioned by these files.
