---
type: overview
created: 2026-04-12
---

# 知识库概览

> 本 Wiki 由 LLM 自动维护。你负责选题和提问，LLM 负责总结、交叉引用、归档和维护。

## 当前状态
- 来源数量：8
- 总页面数：27（含 index、log、overview）
- 最近更新：2026-05-05

## 核心发现

### Harness Engineering 三阶段演进
基于 [[2026-05-04-harness-闪客]]，AI对话范式经历了三个阶段：
1. **Prompt Engineering（提示词工程）** - 优化输入给LLM的提示词来激发模型潜力
2. **Context Engineering（上下文工程）** - 补充必要的上下文信息（RAG、工具调用、Long Memory等）
3. **Harness Engineering（驾驭工程）** - 除了信息和工具，还要对AI进行约束（权限、规则、颗粒度等）

### 两层驾驭模型
视频提出的新视角：
- **Agent 驾驭 大模型**：类似公司管理员工的方式
- **人类 驾驭 Agent**：类似公司制定规章制度的方式

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

### VibeCoding 工程化框架
基于 [[2026-05-04-vibecoding-9-steps]]，VibeCoding 需要工程流程支撑：
1. **开发前 9 步骤**：定图纸（需求、PRD、视觉）→ 打地基（边界、技术栈、架构）→ 立规矩（文档、规范、Git）
2. **开发中 5 关键点**：小步迭代、人类介入、限制 AI 权限、死守安全底线、科学应对报错
3. **核心原则**：人类负责编辑和验收，AI 负责体系化

### 四大设计模式
- [[on-demand-loading]] - 渐进式信息披露，避免上下文窗口压力
- [[sandbox-isolation]] - 沙箱隔离，降低试错成本
- 仓库即真理来源 - 规范写进代码仓库
- 机械化执行约束 - 架构约束编码进 Linter
