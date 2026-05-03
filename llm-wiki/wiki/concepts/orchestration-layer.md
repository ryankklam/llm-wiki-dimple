---
type: concept
created: 2026-05-02
updated: 2026-05-02
sources: [2026-05-02-harness-engineering]
---

# Orchestration Layer（编排层）

## 定义

编排层是 Harness Engineering 四层架构的第四层，主要解决复杂任务拆解问题。通过将大任务拆分为并行子任务，多个 Agent 分工协作，中间通过 hooks 和中间件协调状态。

## 解决的问题

复杂工程任务的处理：
- 单个模型能力有限
- 需要多 Agent 协作
- 中间状态管理复杂

## 核心机制

### 任务拆解
将大任务拆分为多个并行子任务，由不同 Agent 分别处理。

### 协作模式
- 多 Agent 分工协作
- 中间可能有 hooks 钩子
- 中间件协调状态

## 效果

让系统可以处理**远超本次对话能力上限的工程任务**。

## 关联

- [[harness-engineering]] - 上层概念
- [[memory-layer]] - 记忆层
- [[execution-layer]] - 执行层
- [[feedback-layer]] - 反馈层
- [[agent]] - Agent 概念

## 开放问题

- 如何设计有效的任务拆解策略？
- 多 Agent 协作时如何保证一致性和效率？
