# Remove unnecessary privileged execution

**Proposal:** `clp-30e471a8a5c4dbca6ccd`

**Scope:** `cluster/synthetic/namespaces/platform/deployments/device-plugin`

**Control:** `kubernetes.workload.privileged`

**Blast radius:** critical (9/10)

**Approval:** 2 reviewer(s) required

## Proposed change

Set a least-privilege security context and admission policy while preserving explicitly justified system workloads.

## Monthly cost-delta scenario

| Low | Expected | High |
|---:|---:|---:|
| $0.00 | $0.00 | $20.00 |

These values are fixture assumptions, not provider quotes. Validate region, tier, traffic, commitments and live pricing.

## Verification plan

- [ ] Run workload functional and startup tests
- [ ] Validate required device and filesystem access
- [ ] Exercise admission policy in audit mode
- [ ] Collect runtime and admission evidence

## Safety boundary

This artifact is unapproved and performs no mutation. An accountable engineer must validate architecture dependencies and use an external deployment pipeline.
