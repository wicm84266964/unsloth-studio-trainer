---
name: unsloth-studio-trainer
description: Operate local Unsloth Studio and Unsloth CLI fine-tuning workflows. Use for single-GPU CLI smoke tests and training runs, or for Qwen3.5 dual-GPU Studio API runs. The workflow is tested on Windows; Linux, WSL, and macOS should be treated as unverified until checked on the target machine.
allowed-tools: powershell, read_file, list_files, glob
metadata:
  openclaw:
    os:
      - win32
    requires:
      bins:
        - python
---

# Unsloth Studio Trainer

Use this skill to operate local Unsloth Studio and Unsloth CLI fine-tuning
workflows. It provides procedural guardrails and templates; it does not replace
Unsloth or implement a training framework.

This workflow has been tested on Windows. The overall training flow may be
portable to Linux, WSL, and macOS, but platform-specific commands, environment
paths, GPU discovery, and multi-GPU behavior must be validated on the target
machine before being treated as supported.

## Reusable Boundary

- Do not assume a fixed `unsloth.exe`, Studio Python, virtual environment, or
  site-packages path.
- First discover the local Unsloth Studio and CLI installation on the target
  machine.
- All dataset paths, model paths, and output paths must be explicitly provided
  by the user or discovered from the target environment.
- Do not copy local logs, trained models, checkpoints, compiled caches, API
  keys, or machine-specific run records into the skill directory.

## Skill Root

Locate the skill root before using templates or writing skill-local metadata. In
a normal installation, the skill root is the directory that contains this
`SKILL.md`.

```text
<unsloth-studio-trainer skill root>
```

The agent may start from any project working directory. Treat the skill root as
the location for reusable templates and skill-local metadata. Do not write
Unsloth runtime files into the active coding project unless the user explicitly
chose that project as the training workspace.

## Directory Discipline

Keep reusable files and runtime artifacts separate.

The skill root should only contain:

- `SKILL.md`
- `templates/`
- optional reusable documentation under `references/`

Runtime files should be placed in run-local directories outside the skill root,
or in clearly named ignored directories if the user explicitly chooses the
skill directory as the workspace:

- `runs/<date-or-run-id>/` for reusable YAML or JSON run configuration
- `logs/<date-or-run-id>/` for raw logs
- `runtime/<date-or-run-id>/` for Studio server state
- `cache/<date-or-run-id>/` for compiled or rebuildable caches
- `tmp/<date-or-run-id>/` for disposable probes and intermediate files

Training output models, checkpoints, TensorBoard data, and dataset caches do
not belong in the skill directory. Write them to user-selected output paths.

## Tested Windows Facts

1. Single-GPU CLI training is the conservative default path.
2. The CLI path should use a config file, for example
   `unsloth.exe train -c <config>`.
3. Do not pretend CLI GPU flags are supported unless the installed CLI proves
   they are available on the target machine.
4. Qwen3.5 requires `transformers >= 5.2.0`.
5. The Windows-tested Qwen3.5 dual-GPU path is:
   - Unsloth Studio API `POST /api/train/start`
   - explicit `gpu_ids = [0, 1]`
   - `load_in_4bit = false`
6. Qwen3.5 dual-GPU with 4bit quantized loading failed in the tested Windows
   environment because quantized cross-device training was not supported.
7. Local datasets must be valid UTF-8 JSONL. Clean or convert the source data
   before training if decoding fails or if wrapped JSON must be transformed
   into JSONL.

## Mode Selection

### Mode A: `single-gpu-cli`

Use this by default when:

- the user did not explicitly request dual GPU;
- the goal is a conservative first validation;
- the model fits on one GPU;
- the Studio server is unavailable.

Rules:

- generate or update a YAML config;
- run a dry-run or one-step smoke test before long training;
- start the full run only after the smoke test succeeds.

### Mode B: `dual-gpu-studio-api`

Use this when:

- the user explicitly requests dual GPU;
- the target model is Qwen3.5 or the user chooses a Studio API workflow;
- the target machine has two visible NVIDIA GPUs;
- the Studio API health check is reachable.

Rules:

- submit through the Studio API rather than CLI GPU flags;
- pass explicit `gpu_ids = [0, 1]` unless the user selected different devices;
- default to `load_in_4bit = false` for Windows-tested Qwen3.5 dual-GPU runs;
- if the user requests 4bit dual-GPU, warn that the tested Windows workflow
  failed and revalidate on the target machine before using it for a long run.

## Preflight Checks

Before training, confirm at least:

1. Unsloth Studio or Unsloth CLI is installed.
2. The relevant Python environment is discoverable.
3. Qwen3.5 runs have `transformers >= 5.2.0`.
4. GPU visibility matches the requested mode.
5. Dataset files exist and are UTF-8 JSONL.
6. Output directory parents exist or can be created.
7. For Studio API mode, `GET /api/health` succeeds.
8. For authenticated Studio API mode, an API key or token is created only in
   the local runtime and is never written into repository files.

## Recommended Workflow

### Single-GPU CLI

1. Discover the local Unsloth CLI executable.
2. Create a run-local log directory.
3. Generate a YAML config using user-provided model, dataset, and output paths.
4. Run a dry-run or short smoke test.
5. Launch the full training run after validation.
6. Verify the output directory contains expected LoRA artifacts such as
   `adapter_config.json`, `adapter_model.safetensors`, and checkpoints.

### Qwen3.5 Dual-GPU Studio API

1. Start or discover the Studio server.
2. Check `GET /api/health`.
3. Create any required API key in local runtime only.
4. Fill `templates/qwen35_dual_gpu_windows_api.smoke.template.json`.
5. Submit the one-step smoke test.
6. If the smoke test succeeds, fill
   `templates/qwen35_dual_gpu_windows_api.template.json`.
7. Submit the full run through `POST /api/train/start`.
8. Poll `/api/train/status` and `/api/train/metrics`.
9. Read `/api/train/runs` or `/api/train/runs/{run_id}` for the final
   `output_dir` when the run completes.

## Dual-GPU Success Criteria

Treat a dual-GPU run as successful only when:

- `/api/train/start` returns a queued or running state;
- `/api/train/status` reaches a completed state;
- `final_step > 0`;
- `final_loss` or equivalent final metrics are available;
- the output directory exists;
- expected LoRA artifacts are present;
- both selected GPUs were observed allocating memory during the run;
- the run did not fail due to quantized cross-device training.

## Failure Mapping

### Version gate failure

Symptom: Qwen3.5 reports that `transformers >= 5.2.0` is required.

Action: upgrade the Studio environment dependency, restart the service if
needed, then rerun the smoke test.

### 4bit multi-device failure

Symptom: the run reports that an 8-bit or 4-bit model cannot be trained on a
different device.

Action: keep explicit GPU IDs but set `load_in_4bit = false`; rerun the smoke
test before the full run.

### Dataset encoding failure

Symptom: dataset loading fails with `gbk`, `utf-8`, JSON decoding, or malformed
line errors.

Action: clean the source into standard UTF-8 JSONL and validate line-by-line
before training.

### CLI sees multiple GPUs but trains on one GPU

Symptom: two GPUs are visible, but the CLI run only uses one GPU.

Action: do not count it as a dual-GPU success. Switch to the Studio API path if
dual-GPU execution is required.

## Templates

- `templates/qwen35_dual_gpu_windows_api.template.json`
  - reusable Qwen3.5 dual-GPU Studio API template
  - defaults to the Windows-tested non-4bit path
- `templates/qwen35_dual_gpu_windows_api.smoke.template.json`
  - one-step smoke test template
  - use before running a long job on a new machine

## Report Back

When finishing or handing off a run, report:

- selected mode: single-GPU CLI or Studio API;
- selected GPU IDs;
- whether `load_in_4bit` was enabled;
- phase, final step, and final loss if available;
- final output directory;
- whether expected LoRA artifacts were generated;
- exact failure class if the run failed.

## Cleanup

- Keep generated logs, caches, runtime state, and temporary files out of the
  repository unless the user explicitly asks to preserve a sanitized example.
- Never commit API keys, tokens, datasets, trained weights, checkpoints,
  compiled caches, local Studio state, or machine-specific run logs.
- If runtime files were accidentally written into the repository, move them to
  an ignored local directory or remove them before publishing.
