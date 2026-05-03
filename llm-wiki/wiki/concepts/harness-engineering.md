---
type: concept
created: 2026-05-02
updated: 2026-05-02
sources: [2026-05-02-harness-engineering]
---

# Harness Engineering

## 定义

Harness Engineering（工具工程）是围绕大语言模型（LLM）构建基础设施系统的总称，旨在更好地驾驭模型的能力。其名称来源于马的"挽具"——马本身有力量，但需要挽具（缰绳、马鞍）才能将力量转化为实际可用的输出；同样，LLM 有强大的能力，但需要额外的系统来使其产生稳定、可重复的好输出。

## 核心观点

1. **模型有能力 ≠ 能给出好输出**：LLM 虽然知识渊博，但直接输出可能不稳定、不可靠

2. **比 Prompt Engineering 更大一个量级**：不仅是优化提示词，而是构建完整的基础设施系统

3. **解决 LLM 的结构性缺陷**：在模型本身性质的基础上建造系统，让模型完成原本无法独立完成的任务

## 与 Prompt Engineering 的区别

| 维度 | Prompt Engineering | Harness Engineering |
|------|-------------------|---------------------|
| 范围 | 优化提示词 | 构建完整系统 |
| 层次 | 应用层 | 基础设施层 |
| 能力 | 有限的 | 更强大的 |
| 目标 | 更好的单次输出 | 稳定可靠的系统 |

## 关联

- [[memory-layer]] - 记忆层
- [[execution-layer]] - 执行层
- [[feedback-layer]] - 反馈层
- [[orchestration-layer]] - 编排层
- [[feedback-loop]] - 反馈回路

## 开放问题

- 如何在不同场景下选择合适的 Harness 架构组合？
- 小型团队如何高效构建和维护 Harness 系统？
