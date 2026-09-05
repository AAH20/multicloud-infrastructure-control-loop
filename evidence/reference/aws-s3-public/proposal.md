# Restrict unintended S3 public access

**Proposal:** `clp-5a6e9b6fbbe45db4d1b4`

**Scope:** `arn:aws:s3:::synthetic-public-bucket`

**Control:** `aws.s3.public_access`

**Blast radius:** medium (5/10)

**Approval:** 1 reviewer(s) required

## Proposed change

Enable account/bucket public-access controls only after identifying intended public distribution and replacing it with an approved delivery path where required.

## Monthly cost-delta scenario

| Low | Expected | High |
|---:|---:|---:|
| $0.00 | $0.00 | $5.00 |

These values are fixture assumptions, not provider quotes. Validate region, tier, traffic, commitments and live pricing.

## Verification plan

- [ ] Inventory bucket policies and ACLs
- [ ] Validate CDN/application consumers
- [ ] Confirm intended principals retain access
- [ ] Recollect Security Hub state

## Safety boundary

This artifact is unapproved and performs no mutation. An accountable engineer must validate architecture dependencies and use an external deployment pipeline.
