"""Contract tests for truthful ARTEMIS hosted-runner reporting."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "project-runner.yml"
DOC = ROOT / "PROJECT_RUNNER.md"
PREFLIGHT = ROOT / "scripts" / "termux_llama_preflight.sh"
TRIAL_DOC = ROOT / "docs" / "LLAMA_CPP_TERMUX_TRIAL.md"


class ProjectRunnerScopeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workflow = WORKFLOW.read_text(encoding="utf-8")
        cls.documentation = DOC.read_text(encoding="utf-8")
        cls.preflight = PREFLIGHT.read_text(encoding="utf-8")
        cls.trial_documentation = TRIAL_DOC.read_text(encoding="utf-8")

    def test_job_name_describes_hosted_repository_validation(self):
        self.assertIn("  project-validation:", self.workflow)
        self.assertIn(
            "name: Hosted repository validation (not device health)",
            self.workflow,
        )
        self.assertNotIn("  health-check:", self.workflow)

    def test_report_discloses_hosted_scope_and_device_limit(self):
        self.assertIn("hosted Linux repository checks only.", self.workflow)
        self.assertIn(
            "Not a live service, exchange, or Android-device/Termux health check.",
            self.workflow,
        )
        self.assertIn(
            "script not executed on target device",
            self.workflow,
        )
        self.assertIn(
            "target-device compatibility not tested",
            self.workflow,
        )

    def test_summary_and_artifact_run_after_failure(self):
        self.assertIn("name: Publish validation summary", self.workflow)
        self.assertIn("if: always()", self.workflow)
        self.assertIn("GITHUB_STEP_SUMMARY", self.workflow)
        self.assertIn("name: Save runner report", self.workflow)
        self.assertIn(
            "project-runner-report-${{ github.run_id }}-${{ github.run_attempt }}",
            self.workflow,
        )

    def test_workflow_permissions_remain_read_only(self):
        self.assertIn("permissions:\n  contents: read", self.workflow)

    def test_documentation_separates_hosted_and_device_acceptance(self):
        self.assertIn("not a Huawei/Android device test", self.documentation)
        self.assertIn("execute the script in Termux", self.documentation)
        self.assertIn("llama.cpp compiles", self.documentation)
        self.assertIn("target handset", self.documentation)

    def test_actions_use_node24_compatible_majors(self):
        expected = (
            "uses: actions/checkout@v7",
            "uses: actions/setup-python@v7",
            "uses: actions/upload-artifact@v7",
        )
        for pin in expected:
            with self.subTest(pin=pin):
                self.assertIn(pin, self.workflow)
        self.assertNotIn("actions/checkout@v4", self.workflow)
        self.assertNotIn("actions/setup-python@v5", self.workflow)
        self.assertNotIn("actions/upload-artifact@v4", self.workflow)
        self.assertIn("Node 24-compatible", self.documentation)

    def test_termux_preflight_reports_android_abis_without_side_effects(self):
        self.assertIn("ro.product.cpu.abi", self.preflight)
        self.assertIn("ro.product.cpu.abilist", self.preflight)
        self.assertIn('getprop "$property"', self.preflight)
        self.assertIn("read-only inventory", self.preflight.lower())
        self.assertNotIn("pkg install", self.preflight)
        self.assertNotIn("git clone", self.preflight)
        self.assertIn("Android primary ABI and ABI list", self.trial_documentation)


if __name__ == "__main__":
    unittest.main()
