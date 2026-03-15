#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from omics_pipeline.workflows import run_template_pipeline


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Python omics template pipeline")
    parser.add_argument("--config", required=True, help="Path to YAML config file")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_template_pipeline(args.config)


if __name__ == "__main__":
    main()
