# Remediation scaffold

Target implementations: kubernetes, helm, kustomize, opa

Set a least-privilege security context and admission policy while preserving explicitly justified system workloads.

No deployable resource values are generated because account topology, identity ownership, DNS, networking, data classification and workload dependencies are not present in the fixture. Implement the change in the customer's reviewed module, attach the resulting plan, obtain approval, deploy through the existing pipeline, and run the verification contract.
