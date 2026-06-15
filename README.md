# Unsloth Studio Trainer

中文说明见 [README.zh-CN.md](README.zh-CN.md).

Unsloth Studio Trainer is an open workflow package for operating local
Unsloth Studio and Unsloth CLI fine-tuning runs.

It is not a training framework and does not wrap or replace Unsloth. The goal is
to provide a reusable agent contract and sanitized templates for planning,
launching, monitoring, and cleaning up local fine-tuning jobs.

## Status

This workflow has been tested on Windows. The general Unsloth Studio training
flow should be portable to Linux, WSL, and macOS, but platform-specific commands,
environment paths, GPU discovery, and multi-GPU behavior still need validation
on the target machine.

## What It Covers

- conservative single-GPU CLI fine-tuning with a dry-run first
- Qwen3.5 dual-GPU runs through the Unsloth Studio API
- Windows-tested Qwen3.5 dual-GPU defaults:
  - `gpu_ids = [0, 1]`
  - `load_in_4bit = false`
- smoke-test templates before long training runs
- UTF-8 JSONL dataset checks
- clear separation between reusable skill files and local runtime outputs
- failure mapping for common version, quantization, encoding, and GPU-routing
  problems

## Repository Layout

```text
unsloth-studio-trainer/
  skills/
    unsloth-studio-trainer/
      SKILL.md
      templates/
        qwen35_dual_gpu_windows_api.template.json
        qwen35_dual_gpu_windows_api.smoke.template.json
```

The `skills/unsloth-studio-trainer` directory is the installable skill. The
repository root contains public documentation and license files.

## Requirements

- Unsloth Studio and/or Unsloth CLI installed on the target machine
- Python environment required by Unsloth
- NVIDIA GPU for CUDA training workflows
- two visible GPUs for the dual-GPU Studio API workflow
- UTF-8 JSONL local datasets
- for Qwen3.5, `transformers >= 5.2.0` in the Unsloth Studio environment

## Agent Setup Prompt

Give this prompt to an AI coding agent so it can install or internalize the
workflow instead of making you wire everything by hand:

```text
Please adopt this repository as an Unsloth Studio training workflow.

Repository: https://github.com/wicm84266964/unsloth-studio-trainer

Read README.md and skills/unsloth-studio-trainer/SKILL.md. If your environment
supports reusable skills or agent instructions, install or register
skills/unsloth-studio-trainer as a skill named unsloth-studio-trainer. If it
does not, internalize SKILL.md as durable operating instructions for this
project or session.

When helping me run Unsloth Studio or Unsloth CLI fine-tuning:
- Treat this workflow as Windows-tested.
- Treat Linux, WSL, and macOS as unverified until checked on the target machine.
- Discover local Unsloth paths, Python environments, GPU visibility, and
  dependency versions before training.
- Use a dry-run or one-step smoke test before any long run.
- For Windows-tested Qwen3.5 dual-GPU Studio API runs, default to
  gpu_ids=[0,1] and load_in_4bit=false unless target-machine validation proves
  another setup is safe.
- Keep datasets, model outputs, checkpoints, logs, caches, runtime state, API
  keys, and machine-specific run records out of the repository.
- Report the selected mode, GPU IDs, quantization setting, final status, final
  step/loss when available, output directory, generated LoRA artifacts, and any
  exact failure class.
```

## Usage

Install or copy `skills/unsloth-studio-trainer` into the skill directory used by
your automation environment.

For a new machine, use the skill to:

1. discover the local Unsloth Studio and CLI installation;
2. verify GPU visibility and dependency versions;
3. confirm the dataset is valid UTF-8 JSONL;
4. run a short smoke test;
5. launch the full run only after the smoke test succeeds;
6. report final status, loss, output directory, and expected LoRA artifacts.

## Templates

- `qwen35_dual_gpu_windows_api.template.json`
  - long-run Qwen3.5 dual-GPU Studio API template
  - defaults to the Windows-tested non-4bit dual-GPU path
- `qwen35_dual_gpu_windows_api.smoke.template.json`
  - one-step Qwen3.5 dual-GPU smoke test template
  - useful for validating a new local environment before a long run

All local paths are placeholders. Replace dataset and output paths before use.

## Data and Runtime Boundaries

This repository does not include datasets, trained models, checkpoints,
compiled caches, Unsloth runtime state, API keys, logs, or machine-specific run
records.

Training outputs should be written to explicit user-selected output
directories, not into the skill directory. Logs, temporary files, runtime state,
and caches should stay in clearly named run-local directories.

## License

MIT.
