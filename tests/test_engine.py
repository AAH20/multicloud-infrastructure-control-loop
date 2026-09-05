import json
import unittest
from pathlib import Path

from control_loop.engine import CompilationError, compile_proposal, verify

ROOT = Path(__file__).resolve().parents[1]


class EngineTests(unittest.TestCase):
    def load(self, name): return json.loads((ROOT / name).read_text(encoding="utf-8"))
    def compile(self, fixture): return compile_proposal(self.load(f"examples/{fixture}"), self.load("config/rules.json"))

    def test_all_five_workflows_compile(self):
        fixtures = ["azure-storage-public.json", "aws-s3-public.json", "gcp-storage-public.json", "kubernetes-privileged.json", "cloud-logging-disabled.json"]
        self.assertEqual(5, len({self.compile(name)["proposal_id"] for name in fixtures}))

    def test_compilation_is_deterministic(self):
        self.assertEqual(self.compile("azure-storage-public.json"), self.compile("azure-storage-public.json"))

    def test_high_risk_change_requires_two_reviewers(self):
        proposal = self.compile("kubernetes-privileged.json")
        self.assertGreaterEqual(proposal["blast_radius"]["score"], 7)
        self.assertEqual(2, proposal["approval"]["minimum_reviewers"])

    def test_logging_cost_scales_with_event_assumption(self):
        proposal = self.compile("cloud-logging-disabled.json")
        self.assertEqual(1125.0, proposal["cost"]["monthly_delta"]["expected"])
        self.assertEqual("low", proposal["cost"]["confidence"])

    def test_compiler_refuses_satisfied_finding(self):
        finding = self.load("examples/aws-s3-public.json"); finding["status"] = "satisfied"
        with self.assertRaises(CompilationError):
            compile_proposal(finding, self.load("config/rules.json"))

    def test_post_change_verification(self):
        proposal = self.compile("azure-storage-public.json")
        receipt = verify(proposal, self.load("examples/azure-storage-remediated.json"))
        self.assertTrue(receipt["verified"])

    def test_wrong_scope_fails_verification(self):
        proposal = self.compile("azure-storage-public.json")
        after = self.load("examples/azure-storage-remediated.json"); after["scope"] = "wrong"
        self.assertFalse(verify(proposal, after)["verified"])


if __name__ == "__main__": unittest.main()
