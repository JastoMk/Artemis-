"""Contract tests for truthful ARTEMIS hosted-runner reporting."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "project-runner.yml"
DOC = ROOT / "PROJECT_RUNNER.md"


class ProjectRunnerScopeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workflow = WORKFLOW.read_text(encoding="utf-8")
        cls.documentation = DOC.read_text(encoding="utf-8")

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
        self.assertIn("does not execute the script in Termux", self.documentation)
        self.assertIn("llama.cpp compiles", self.documentation)
        self.assertIn("target handset", self.documentation)


if __name__ == "__main__":
    unittest.main()
