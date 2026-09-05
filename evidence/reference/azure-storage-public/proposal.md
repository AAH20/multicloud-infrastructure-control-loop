# Move Azure Storage to an approved private-access path

**Proposal:** `clp-cb0b5aa1e24ef49575b7`

**Scope:** `/subscriptions/000/resourceGroups/rg-example/providers/Microsoft.Storage/storageAccounts/synthetic`

**Control:** `azure.storage.public_access`

**Blast radius:** critical (9/10)

**Approval:** 2 reviewer(s) required

## Proposed change

Add a Private Endpoint and private DNS association, then disable public network access after consumer-path validation.

## Monthly cost-delta scenario

| Low | Expected | High |
|---:|---:|---:|
| $7.30 | $18.00 | $73.00 |

These values are fixture assumptions, not provider quotes. Validate region, tier, traffic, commitments and live pricing.

## Verification plan

- [ ] Resolve the storage FQDN from every approved network
- [ ] Test application read/write paths
- [ ] Confirm public path denial
- [ ] Recollect Azure Policy state

## Safety boundary

This artifact is unapproved and performs no mutation. An accountable engineer must validate architecture dependencies and use an external deployment pipeline.
