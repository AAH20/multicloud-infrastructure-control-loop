# Remediation scaffold

Target implementations: terraform, opentofu, cloudformation

Enable account/bucket public-access controls only after identifying intended public distribution and replacing it with an approved delivery path where required.

No deployable resource values are generated because account topology, identity ownership, DNS, networking, data classification and workload dependencies are not present in the fixture. Implement the change in the customer's reviewed module, attach the resulting plan, obtain approval, deploy through the existing pipeline, and run the verification contract.
