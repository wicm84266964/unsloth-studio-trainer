# Unsloth Studio Trainer

Unsloth Studio Trainer 是一个用于操作本机 Unsloth Studio 和 Unsloth CLI
微调任务的开源工作流包。

它不是新的训练框架，也不替代 Unsloth。本项目的目标是提供一份可复用的智能体
操作合约和脱敏模板，用于规划、启动、监控和收尾本地微调任务。

## 当前状态

这个工作流已经在 Windows 上跑通。整体 Unsloth Studio 训练流程理论上可以迁移
到 Linux、WSL 和 macOS，但平台命令、环境路径、GPU 探测、多卡行为和量化训练
细节需要在目标设备上重新复核。

## 覆盖内容

- 保守的单卡 CLI 微调流程，并且先做 dry-run
- 通过 Unsloth Studio API 提交 Qwen3.5 双卡训练
- Windows 上已经验证过的 Qwen3.5 双卡默认设置：
  - `gpu_ids = [0, 1]`
  - `load_in_4bit = false`
- 长任务前的 smoke test 模板
- UTF-8 JSONL 数据集检查
- 可复用 skill 文件和本机运行产物的边界划分
- 常见版本、量化、编码、GPU 路由问题的失败映射

## 目录结构

```text
unsloth-studio-trainer/
  skills/
    unsloth-studio-trainer/
      SKILL.md
      templates/
        qwen35_dual_gpu_windows_api.template.json
        qwen35_dual_gpu_windows_api.smoke.template.json
```

`skills/unsloth-studio-trainer` 是可安装的 skill。仓库根目录只放公开说明和许可证。

## 环境要求

- 目标机器已经安装 Unsloth Studio 或 Unsloth CLI
- 具备 Unsloth 所需的 Python 环境
- CUDA 训练工作流需要 NVIDIA GPU
- 双卡 Studio API 工作流需要能看到两张 GPU
- 本地数据集为 UTF-8 JSONL
- 如果训练 Qwen3.5，Unsloth Studio 环境中的 `transformers` 需要满足 `>= 5.2.0`

## 给智能体的安装提示词

把下面这段提示词交给 AI 编程智能体，让它自己安装或内化这个工作流，而不是让你
手动一点点配置：

```text
请把这个仓库内化为一个 Unsloth Studio 训练工作流。

仓库地址：https://github.com/wicm84266964/unsloth-studio-trainer

请阅读 README.md 和 skills/unsloth-studio-trainer/SKILL.md。如果你的运行环境
支持可复用 skill 或智能体指令，请把 skills/unsloth-studio-trainer 安装或注册为
名叫 unsloth-studio-trainer 的 skill。如果不支持，请把 SKILL.md 内化为当前项目
或当前会话里的长期操作规范。

当你协助我运行 Unsloth Studio 或 Unsloth CLI 微调时：
- 认为这个工作流已经在 Windows 上跑通。
- Linux、WSL、macOS 在目标机器复核前都视为未验证。
- 训练前先探测本机 Unsloth 路径、Python 环境、GPU 可见性和依赖版本。
- 长任务前必须先做 dry-run 或 1-step smoke test。
- 对 Windows 已验证的 Qwen3.5 双卡 Studio API 训练，默认使用 gpu_ids=[0,1]
  和 load_in_4bit=false，除非目标机器复核证明其他配置可用。
- 不要把数据集、模型输出、checkpoint、日志、缓存、运行状态、API key 或本机
  运行记录写入仓库。
- 汇报实际模式、GPU ID、量化设置、最终状态、final step/loss、输出目录、
  LoRA 产物是否生成，以及失败时的明确失败类型。
```

## 使用方式

把 `skills/unsloth-studio-trainer` 安装或复制到你的自动化环境所使用的 skill 目录。

在新机器上，建议让该 skill 依次完成：

1. 探测本机 Unsloth Studio 和 CLI 安装位置；
2. 检查 GPU 可见性和依赖版本；
3. 确认数据集是合法的 UTF-8 JSONL；
4. 先运行短 smoke test；
5. smoke test 成功后再启动完整训练；
6. 汇报最终状态、loss、输出目录和 LoRA 产物是否生成。

## 模板

- `qwen35_dual_gpu_windows_api.template.json`
  - Qwen3.5 双卡 Studio API 长任务模板
  - 默认使用 Windows 已验证的非 4bit 双卡路径
- `qwen35_dual_gpu_windows_api.smoke.template.json`
  - Qwen3.5 双卡 1-step smoke test 模板
  - 用于在新环境上验证能否跑通

模板里的本地路径都是占位符，使用前需要替换为真实的数据集路径和输出路径。

## 数据和运行边界

本仓库不包含数据集、训练后模型、checkpoint、编译缓存、Unsloth 运行状态、
API key、日志或本机运行记录。

训练输出应该写入用户明确指定的输出目录，不应该写入 skill 目录。日志、临时文件、
运行状态和缓存也应该放在清晰命名的本次运行目录中。

## 许可证

MIT。
