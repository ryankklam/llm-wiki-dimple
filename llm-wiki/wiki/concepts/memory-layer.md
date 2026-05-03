---
type: concept
created: 2026-05-02
updated: 2026-05-02
sources: [2026-05-02-harness-engineering]
---

# Memory Layer（记忆层）

## 定义

记忆层是 Harness Engineering 四层架构的第一层，旨在解决 LLM 无状态的问题。通过文件系统持久化需要模型知道的信息，结构化存放，让模型每次工作都能检索到正确的背景信息。

## 解决的问题

LLM 的结构性缺陷之一：**无状态**
- 每次对话结束什么都不记得
- 不知道项目有什么规范
- 无法保持跨对话的一致性

## 实践方式

### 文件系统持久化
将需要模型知道的信息写入文件，结构化存放：
- `claude.md` - Claude 项目的规范和上下文
- `agents.md` - Agent 的配置和约束

### 不是百科全书，而是导航地图
记忆层文件不是详尽的知识库，而是告诉 Agent：
- 最关键的约束
- 基本的规则
- 导航信息

## 核心原则

> 只告诉 agents 最关键的一个约束和规则

## 关联

- [[harness-engineering]] - 上层概念
- [[execution-layer]] - 执行层
- [[feedback-layer]] - 反馈层
- [[orchestration-layer]] - 编排层

## 开放问题

- 如何平衡记忆层的信息量和上下文窗口限制？
- 如何保持记忆层文件的长期可维护性？
