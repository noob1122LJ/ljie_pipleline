#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r python/requirements.txt

echo "[bootstrap] Python environment is ready."
echo "[bootstrap] Run: source .venv/bin/activate && make smoke-python"
