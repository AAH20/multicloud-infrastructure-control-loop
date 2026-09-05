from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class CompilationError(Exception):
    message: str

    def __str__(self) -> str:
        return self.message


def canonical_digest(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(payload.encode()).hexdigest()


def validate_finding(finding: dict[str, Any]) -> None:
    required = ("provider", "control_ref", "scope", "status", "observed_at", "context")
    missing = [key for key in required if key not in finding]
    if missing:
        raise CompilationError(f"missing required fields: {', '.join(missing)}")
    if finding["status"] not in {"satisfied", "not_satisfied", "unknown"}:
        raise CompilationError("status must be satisfied, not_satisfied, or unknown")
    if not isinstance(finding["context"], dict):
        raise CompilationError("context must be an object")


def select_rule(finding: dict[str, Any], rules: dict[str, Any]) -> dict[str, Any]:
    candidates = [rule for rule in rules.get("rules", []) if rule["control_ref"] == finding["control_ref"] and rule["provider"] in {finding["provider"], "multicloud"}]
    if len(candidates) != 1:
        raise CompilationError(f"expected exactly one rule for {finding['provider']}:{finding['control_ref']}; found {len(candidates)}")
    return candidates[0]


def blast_radius(rule: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
    dependency_count = max(0, int(context.get("dependency_count", 0)))
    factors = {
        "base": int(rule["base_risk"]),
        "shared_scope": 2 if context.get("shared_scope") else 0,
        "data_path": 2 if context.get("data_path") else 0,
        "dependencies": min(3, dependency_count // 3),
    }
    score = min(10, sum(factors.values()))
    level = "critical" if score >= 9 else "high" if score >= 7 else "medium" if score >= 4 else "low"
    return {"score": score, "level": level, "factors": factors, "dependency_count": dependency_count}


def cost_scenario(rule: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
    base = rule["monthly_cost_usd"]
    events = max(1.0, float(context.get("monthly_events_million", 1.0)))
    multiplier = events if rule["control_ref"] == "cloud.logging.enabled" else 1.0
    values = {key: round(float(value) * multiplier, 2) for key, value in base.items()}
    return {
        "currency": "USD",
        "monthly_delta": values,
        "model": "fixture assumption, not a provider quote",
        "confidence": "low",
        "validation_required": ["Live provider pricing", "Region and tier", "Measured traffic or ingestion", "Existing commitments and discounts"],
    }


def compile_proposal(finding: dict[str, Any], rules: dict[str, Any]) -> dict[str, Any]:
    validate_finding(finding)
    if finding["status"] != "not_satisfied":
        raise CompilationError("a remediation proposal requires status=not_satisfied")
    rule = select_rule(finding, rules)
    input_digest = canonical_digest(finding)
    core = {
        "schema_version": "1.0",
        "rule_id": rule["id"],
        "provider": finding["provider"],
        "control_ref": finding["control_ref"],
        "scope": finding["scope"],
        "input_digest": input_digest,
        "observed_at": finding["observed_at"],
        "title": rule["title"],
        "proposed_change": rule["change"],
        "iac_targets": rule["iac_targets"],
        "blast_radius": blast_radius(rule, finding["context"]),
        "cost": cost_scenario(rule, finding["context"]),
        "tests": rule["tests"],
        "approval": {"required": True, "state": "unapproved", "minimum_reviewers": 2 if context_is_high_risk(finding["context"], rule) else 1},
        "mutation": {"performed": False, "allowed_by_compiler": False},
    }
    core["proposal_id"] = f"clp-{canonical_digest(core)[:20]}"
    return core


def context_is_high_risk(context: dict[str, Any], rule: dict[str, Any]) -> bool:
    return blast_radius(rule, context)["score"] >= 7


def verification_contract(proposal: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "proposal_id": proposal["proposal_id"],
        "expected": {"provider": proposal["provider"], "control_ref": proposal["control_ref"], "scope": proposal["scope"], "status": "satisfied"},
        "requires_newer_observation": True,
        "requires_evidence_digest": True,
    }


def verify(proposal: dict[str, Any], post_change: dict[str, Any]) -> dict[str, Any]:
    contract = verification_contract(proposal)
    expected = contract["expected"]
    checks = {
        key: post_change.get(key) == expected[key] for key in ("provider", "control_ref", "scope", "status")
    }
    checks["newer_observation"] = str(post_change.get("observed_at", "")) > str(proposal["observed_at"])
    checks["evidence_digest_present"] = bool(post_change.get("evidence_digest"))
    passed = all(checks.values())
    return {
        "schema_version": "1.0",
        "proposal_id": proposal["proposal_id"],
        "verified": passed,
        "checks": checks,
        "post_change_digest": canonical_digest(post_change),
        "verified_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
    }
