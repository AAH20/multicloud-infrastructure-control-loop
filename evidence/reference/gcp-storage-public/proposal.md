# Enforce approved Cloud Storage access

**Proposal:** `clp-c03315e8d4fc31e7b62d`

**Scope:** `//storage.googleapis.com/synthetic-public-bucket`

**Control:** `gcp.storage.public_access_prevention`

**Blast radius:** medium (5/10)

**Approval:** 1 reviewer(s) required

## Proposed change

Enable Public Access Prevention and remove broad IAM members after validating intended public delivery and service identities.

## Monthly cost-delta scenario

| Low | Expected | High |
|---:|---:|---:|
| $0.00 | $0.00 | $5.00 |

These values are fixture assumptions, not provider quotes. Validate region, tier, traffic, commitments and live pricing.

## Verification plan

- [ ] Inventory allUsers and allAuthenticatedUsers bindings
- [ ] Validate application identities
- [ ] Confirm intended public delivery replacement
- [ ] Recollect SCC state

## Safety boundary

This artifact is unapproved and performs no mutation. An accountable engineer must validate architecture dependencies and use an external deployment pipeline.
