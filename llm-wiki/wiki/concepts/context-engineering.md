---
type: concept
created: 2026-05-04
updated: 2026-05-04
sources: [2026-05-04-harness-闪客]
---

# Context Engineering（上下文工程）

## 定义
通过补充必要的上下文信息来提升LLM回答质量的技术方法，是Prompt Engineering的进化阶段。

## 关键信息

### 核心方法
- **RAG**：通过检索增强生成动态查询向量数据库
- **工具调用**：调用API返回必要信息
- **Long Memory**：历史对话压缩等技术
- **手动补充**：以图或文字形式提供必要上下文

### 演进背景
Context Engineering是AI对话范式的第二阶段：
- 当模型能力越来越强，不再需要太多提示词技巧
- 关键变成了上下文信息的补充
- 视频中比喻：不是指令不够清晰，而是缺少必要的上下文信息（来源：[[2026-05-04-harness-闪客]]）

### 局限性
- 视频认为"Context Engineering"这个词的流行，部分原因是资本需要造新词来体现工作量
- 提示词工程可以理解为包含在上下文工程内，这个词就可以扔掉了

## 与其他概念的关系
- [[prompt-engineering]] - Prompt Engineering是前置阶段
- [[harness-engineering]] - Harness工程是更全面的驾驭体系，包括约束制定
- [[agent]] - Agent可以在更高级别自动化上下文管理

## 关联
- 相关概念：[[on-demand-loading]] - 按需加载是一种上下文管理策略
- 相关概念：[[feedback-loop]] - 反馈回路验证上下文补充的效果
