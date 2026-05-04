---
type: source
date: 2026-05-04
source: raw/rednote/skill实战：从0到1写一个你自己的skill.md
platform: xiaohongshu
video_id: 4iELqFXf4C0
author: 未知用户
tags: [skill, claude-code, ai-tooling, workflow]
---

# 来源：skill实战：从0到1写一个你自己的skill

## 视频信息
- **作者**：未知用户
- **发布时间**：2026-05-04
- **视频链接**：http://xhslink.com/o/4iELqFXf4C0
- **字幕来源**：WHISPER

## 核心要点
1. **Skill 本质**：就是一个文件夹，核心是 skill.md 文档，包含元数据（告诉 AI 我是谁）和操作指南（告诉 AI 怎么干）
2. **按需加载**：AI 靠 description 匹配，不是全部读入，类似图书馆目录卡片
3. **六步流程**：想清楚问题 → 告诉 AI 创建 → 回答提问 → AI 生成 → 测试调试 → 分享出去
4. **核心三件事**：想清楚问题、告诉 AI 需求、测试调试迭代

## 视频内容摘要

### Skill 的本质
- Skill 本质是一个文件夹
- 核心是 skill.md 文档，相当于 skill 的大脑
- skill.md 包含两部分：
  - **元数据**：告诉 AI 我是谁、我能干什么
  - **操作指南**：告诉 AI 我具体应该怎么干
- 可选文件夹：scripts（脚本）、reference（模板/配置）

### 六步创建流程

**第一步：想清楚要解决什么问题**
- 问自己：哪个环节重复超过三次？
- 例：每日 AI 新闻速递 → 爬取、翻译、整理、排版

**第二步：告诉 AI 要创建技能**
- 对 Claude Code 说"帮我创建一个新的技能"或"我要做一个棒棒的 skill"
- 前提：已安装 Skill Creator 工具

**第三步：回答 AI 的问题**
- AI 像产品经理一样问细节
- 第一轮：网站、内容、格式、保存位置
- 第二轮：抓取数量、翻译、自定义网站
- description 越精准，AI 匹配越准

**第四步：AI 自动生成技能文件**
- 完全由 AI 执行，等待几秒即可

**第五步：测试调试**
- 直接试运行，看执行结果
- 出问题就看执行过程，修改 .md 文件
- 改个两三轮基本就稳了

**第六步：分享出去**
- 铺到 GitHub 或投到 skillsmp 平台
- skill 会自己长大，随时改 .md 文件，永久生效

## 关键信息
- Skill 没有任何代码门槛
- 建议：打开 Claude Code，想一个每天重复的事，花 20 分钟变成第一个 skill

## 与其他来源的关系
- 与 [[2026-04-13-小红书视频-skill实战]] 同一主题的更新版本
- 与 [[2026-05-04-vibecoding-9-steps]] 都涉及 AI 辅助工作流

## 衍生概念
- [[claude-code]] - Claude Code IDE
- [[skill]] - Skill 概念
- [[on-demand-loading]] - 按需加载机制
