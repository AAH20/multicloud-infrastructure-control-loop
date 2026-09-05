# Production Roadmap

## Implemented

- Five provider and platform workflows
- Deterministic rule selection
- Transparent blast-radius and cost scenarios
- Review-gated proposal bundles
- Post-change verification receipts
- Offline tests and synthetic reference artifacts

## Next

1. Publish a JSON Schema and compatibility test kit for bridge inputs.
2. Add adapters consuming the three published CISO Assistant cloud bridges.
3. Add Terraform/OpenTofu plan parsing and Infracost validation.
4. Add Kubernetes server-side dry-run and OPA policy simulation.
5. Add provider pricing adapters with timestamped source receipts.
6. Add GitHub App installation and draft-PR generation behind explicit authorization.
7. Export proposals and receipts to OSCAL, SARIF and CISO Assistant.
8. Add Backstage templates, OpenTelemetry and SLO dashboards.
9. Run controlled live-cloud labs and publish independently reproducible measurements.

Production readiness requires authenticated integration tests, threat modeling, tenant isolation, rollback exercises, versioned schemas and supported-provider matrices.
