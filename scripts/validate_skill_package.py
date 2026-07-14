#!/usr/bin/env python3
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "skills" / "unsloth-studio-trainer"
SKILL_PATH = SKILL_ROOT / "SKILL.md"
FULL_TEMPLATE = SKILL_ROOT / "templates" / "qwen35_dual_gpu_windows_api.template.json"
SMOKE_TEMPLATE = SKILL_ROOT / "templates" / "qwen35_dual_gpu_windows_api.smoke.template.json"


def load_json(path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def require(condition, message):
    if not condition:
        raise SystemExit(message)


def main():
    for path in (SKILL_PATH, FULL_TEMPLATE, SMOKE_TEMPLATE):
        require(path.is_file(), f"missing required package file: {path.relative_to(ROOT)}")

    skill_text = SKILL_PATH.read_text(encoding="utf-8")
    require(skill_text.startswith("---\n"), "SKILL.md must start with YAML frontmatter")
    require("\nname: unsloth-studio-trainer\n" in skill_text, "SKILL.md has the wrong skill name")
    require("## Preflight Checks" in skill_text, "SKILL.md is missing preflight checks")
    require("## Data and Runtime Boundaries" in skill_text or "## Reusable Boundary" in skill_text,
            "SKILL.md is missing the data boundary")

    full = load_json(FULL_TEMPLATE)
    smoke = load_json(SMOKE_TEMPLATE)
    for name, payload in (("full", full), ("smoke", smoke)):
        require(payload.get("gpu_ids") == [0, 1], f"{name} template must keep the tested GPU IDs")
        require(payload.get("load_in_4bit") is False, f"{name} template must keep the tested non-4bit default")
        require(str(payload.get("output_dir", "")).startswith("<absolute path"),
                f"{name} template must not contain a machine-specific output path")
        require(str(payload.get("tensorboard_dir", "")).startswith("<absolute path"),
                f"{name} template must not contain a machine-specific TensorBoard path")

    require(full.get("max_steps") == 0, "full template must not be reduced to a smoke run")
    require(smoke.get("max_steps") == 1, "smoke template must remain a one-step run")
    print("Unsloth Studio Trainer skill package validation passed.")


if __name__ == "__main__":
    main()
