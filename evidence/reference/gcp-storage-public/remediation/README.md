# Remediation scaffold

Target implementations: terraform, opentofu, config-connector

Enable Public Access Prevention and remove broad IAM members after validating intended public delivery and service identities.

No deployable resource values are generated because account topology, identity ownership, DNS, networking, data classification and workload dependencies are not present in the fixture. Implement the change in the customer's reviewed module, attach the resulting plan, obtain approval, deploy through the existing pipeline, and run the verification contract.
