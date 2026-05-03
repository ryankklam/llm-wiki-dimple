---
type: overview
created: 2026-04-12
---

# 知识库概览

> 本 Wiki 由 LLM 自动维护。你负责选题和提问，LLM 负责总结、交叉引用、归档和维护。

## 当前状态
- 来源数量：4
- 总页面数：17（含 index、log、overview）
- 最近更新：2026-05-02

## 核心发现

### Harness Engineering 四层架构
基于 [[2026-05-02-harness-engineering]] 和 [[2026-04-13-小红书视频-skill实战]]，知识库构建了完整的 Harness Engineering 概念体系：

1. **记忆层**（Memory Layer）- 解决 LLM 无状态问题，通过文件系统持久化
2. **执行层**（Execution Layer）- 赋予模型实际执行能力（bash、代码运行、API调用）
3. **反馈层**（Feedback Layer）- 核心层，通过测试/Linter/CI 实现确定性验证
4. **编排层**（Orchestration Layer）- 复杂任务拆解，多 Agent 协作

### 反馈回路的不对称性原理
- 代码生成是**概率性的**
- 代码验证是**确定性的**
- 这种不对称性使得反馈回路可以完全自动化

### 四大设计模式
- [[on-demand-loading]] - 渐进式信息披露，避免上下文窗口压力
- [[sandbox-isolation]] - 沙箱隔离，降低试错成本
- 仓库即真理来源 - 规范写进代码仓库
- 机械化执行约束 - 架构约束编码进 Linter
