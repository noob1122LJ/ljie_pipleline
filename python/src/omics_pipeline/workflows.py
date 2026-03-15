from __future__ import annotations

from pathlib import Path


def load_config(config_path: str | Path) -> dict:
    try:
        import yaml
    except ModuleNotFoundError as exc:
        raise ModuleNotFoundError(
            "Missing dependency 'pyyaml'. Please run: pip install -r python/requirements.txt"
        ) from exc

    config_path = Path(config_path)
    with config_path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def ensure_output_dirs(config: dict) -> None:
    io_cfg = config.get("io", {})
    for key in ("processed_dir", "results_dir"):
        out_dir = Path(io_cfg.get(key, f"data/{key}"))
        out_dir.mkdir(parents=True, exist_ok=True)


def run_template_pipeline(config_path: str | Path) -> None:
    config = load_config(config_path)
    ensure_output_dirs(config)

    project_name = config.get("project", {}).get("name", "unknown_project")
    samples = config.get("samples", [])
    print(f"[Python] Project: {project_name}")
    print(f"[Python] Samples loaded: {len(samples)}")
    print("[Python] TODO: Replace template with Scanpy/scvi-tools/Squidpy workflow.")
