# Architecture

The project is an orchestration and decision layer, not a scanner or deployment engine. Provider bridges and policy tools observe state. This compiler consumes normalized findings and produces a bounded change proposal. Existing CI/CD systems remain responsible for plans, approvals, deployment and rollback.

## Invariants

- No cloud credentials are required or accepted by the compiler.
- A proposal cannot be generated from a satisfied or unknown finding.
- Exactly one version-controlled rule must match.
- Every proposal is unapproved and mutation-disabled.
- High-blast-radius proposals require at least two reviewers.
- Verification requires the same provider, control and scope, a newer observation, satisfied status and a post-change digest.
- Cost data always carries its model, confidence and live-validation requirements.

## Extension model

Provider collectors normalize evidence upstream. Rules supply architecture intent, IaC targets, bounded cost assumptions and tests. Export adapters can translate the proposal and verification receipt to CISO Assistant, OSCAL, SARIF, Jira, ServiceNow or Backstage without changing the core decision model.
