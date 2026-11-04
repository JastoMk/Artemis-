import importlib.util
import tempfile
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location("artemis", Path(__file__).resolve().parents[1] / "artemis.py")
artemis = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(artemis)


class ArtemisLocalTaskTests(unittest.TestCase):
    def test_add_and_complete_task_persist_locally(self):
        with tempfile.TemporaryDirectory() as directory:
            store = Path(directory) / "tasks.json"
            created = artemis.add_task("Test offline operation", store)
            self.assertEqual(created["id"], 1)
            self.assertFalse(created["done"])
            completed = artemis.complete_task(1, store)
            self.assertTrue(completed["done"])
            self.assertTrue(artemis.load_tasks(store)[0]["done"])

    def test_ids_increment_and_empty_title_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            store = Path(directory) / "tasks.json"
            artemis.add_task("First", store)
            second = artemis.add_task("Second", store)
            self.assertEqual(second["id"], 2)
            with self.assertRaises(ValueError):
                artemis.add_task("   ", store)

    def test_unknown_task_is_reported(self):
        with tempfile.TemporaryDirectory() as directory:
            store = Path(directory) / "tasks.json"
            with self.assertRaises(KeyError):
                artemis.complete_task(99, store)

    def test_corrupt_store_is_not_silently_overwritten(self):
        with tempfile.TemporaryDirectory() as directory:
            store = Path(directory) / "tasks.json"
            store.write_text("{broken", encoding="utf-8")
            with self.assertRaises(RuntimeError):
                artemis.load_tasks(store)

    def test_diagnostics_explicitly_disclose_ui_automation_limit(self):
        info = artemis.diagnostics()
        self.assertFalse(info["network_required"])
        self.assertIn("not implemented", info["android_ui_automation"])


if __name__ == "__main__":
    unittest.main()
