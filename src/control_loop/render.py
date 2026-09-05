from pathlib import Path
from typing import Any
import json

from .engine import verification_contract


def proposal_markdown(proposal: dict[str, Any]) -> str:
    cost = proposal["cost"]["monthly_delta"]
    risk = proposal["blast_radius"]
    tests = "\n".join(f"- [ ] {item}" for item in proposal["tests"])
    return f"""# {proposal['title']}

**Proposal:** `{proposal['proposal_id']}`

**Scope:** `{proposal['scope']}`

**Control:** `{proposal['control_ref']}`

**Blast radius:** {risk['level']} ({risk['score']}/10)

**Approval:** {proposal['approval']['minimum_reviewers']} reviewer(s) required

## Proposed change

{proposal['proposed_change']}

## Monthly cost-delta scenario

| Low | Expected | High |
|---:|---:|---:|
| ${cost['low']:.2f} | ${cost['expected']:.2f} | ${cost['high']:.2f} |

These values are fixture assumptions, not provider quotes. Validate region, tier, traffic, commitments and live pricing.

## Verification plan

{tests}

## Safety boundary

This artifact is unapproved and performs no mutation. An accountable engineer must validate architecture dependencies and use an external deployment pipeline.
"""


def remediation_readme(proposal: dict[str, Any]) -> str:
    targets = ", ".join(proposal["iac_targets"])
    return f"""# Remediation scaffold

Target implementations: {targets}

{proposal['proposed_change']}

No deployable resource values are generated because account topology, identity ownership, DNS, networking, data classification and workload dependencies are not present in the fixture. Implement the change in the customer's reviewed module, attach the resulting plan, obtain approval, deploy through the existing pipeline, and run the verification contract.
"""


def write_bundle(directory: Path, proposal: dict[str, Any]) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "remediation").mkdir(exist_ok=True)
    (directory / "proposal.json").write_text(json.dumps(proposal, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (directory / "proposal.md").write_text(proposal_markdown(proposal), encoding="utf-8")
    (directory / "verification-contract.json").write_text(json.dumps(verification_contract(proposal), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (directory / "remediation" / "README.md").write_text(remediation_readme(proposal), encoding="utf-8")
