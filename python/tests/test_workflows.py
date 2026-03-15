from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

from omics_pipeline.workflows import ensure_output_dirs, load_config


class TestWorkflows(unittest.TestCase):
    @unittest.skipUnless(importlib.util.find_spec("yaml") is not None, "pyyaml not installed")
    def test_load_config(self) -> None:
        cfg = load_config("configs/project.example.yaml")
        self.assertIn("project", cfg)
        self.assertIn("samples", cfg)

    def test_ensure_output_dirs(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            processed = Path(tmpdir) / "processed"
            results = Path(tmpdir) / "results"
            cfg = {
                "io": {
                    "processed_dir": str(processed),
                    "results_dir": str(results),
                }
            }
            ensure_output_dirs(cfg)
            self.assertTrue(processed.exists())
            self.assertTrue(results.exists())


if __name__ == "__main__":
    unittest.main()
