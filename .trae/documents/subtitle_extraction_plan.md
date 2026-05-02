# 视频字幕提取实现计划

## 1. 概述

实现从小红书视频中提取字幕的功能，采用三级提取策略：
1. **优先级1**: 从视频元数据中提取（优先）
2. **优先级2**: 从视频流中提取内置字幕
3. **优先级3**: 从音频中识别转换为字幕

最终将字幕保存为Markdown格式，用于LLM Wiki ingest。

**前端增强**: 添加处理过程步骤展示和结果展示界面。

## 2. 当前代码库分析

### 现有模块
- `app.py`: 主API服务
- `modules/video_downloader/`: 视频下载模块
  - `video_downloader.py`: 视频下载
  - `video_fetcher.py`: 视频信息获取
  - `link_parser.py`: 链接解析
- `frontend/src/App.jsx`: 前端React应用

### 当前流程
1. 解析视频链接
2. 获取视频信息
3. 下载视频到临时目录
4. 返回下载路径

## 3. 实现方案

### 3.1 后端模块结构

```
backend/src/modules/
└── subtitle_extractor/
    ├── __init__.py
    ├── subtitle_extractor.py       # 主字幕提取模块
    ├── metadata_subtitle.py        # 从元数据提取
    ├── video_subtitle.py           # 从视频提取
    └── audio_subtitle.py           # 从音频提取
```

### 3.2 新增依赖

在 `requirements.txt` 中添加：

```
ffmpeg-python>=0.2.0
openai-whisper>=20231117
pydub>=0.25.1
python-dotenv>=1.0.0
```

**说明**:
- `ffmpeg-python`: 视频/音频处理
- `openai-whisper`: 语音识别（开源，无需API key）
- `pydub`: 音频处理辅助

### 3.3 后端模块功能设计

#### 3.3.1 `subtitle_extractor.py` (主模块)

**功能**:
- 协调三级字幕提取策略
- 统一的字幕格式化输出
- Markdown格式转换
- 实时进度通知（WebSocket/事件流）

**核心函数**:
```python
def extract_subtitles(
    video_path: str,
    video_info: Dict[str, Any],
    output_dir: str,
    progress_callback: Optional[Callable] = None
) -> Dict[str, Any]:
    """
    提取字幕主函数
    
    提取策略:
    1. 先尝试从视频元数据提取
    2. 失败则从视频流提取
    3. 最后从音频识别
    
    Returns:
        {
            "subtitles": str,           # Markdown格式字幕
            "source": str,              # 来源: metadata/video/audio
            "confidence": float,        # 置信度(音频识别时)
            "md_path": str,             # Markdown文件路径
            "timestamps": List[Dict]    # 时间戳信息(可选)
        }
    """
```

#### 3.3.2 `metadata_subtitle.py` (元数据提取)

**功能**:
- 从小红书页面HTML中提取文字描述
- 提取笔记内容作为字幕

**核心函数**:
```python
def extract_from_metadata(video_info: Dict[str, Any]) -> Optional[str]:
    """
    从视频元数据提取字幕
    解析视频页面的HTML，提取:
    - 笔记标题
    - 笔记正文
    - 评论精选
    """
```

#### 3.3.3 `video_subtitle.py` (视频提取)

**功能**:
- 使用ffmpeg提取视频内置字幕
- 支持多种字幕格式（SRT, ASS, VTT等）

**核心函数**:
```python
def extract_from_video(video_path: str) -> Optional[str]:
    """
    从视频文件提取内置字幕
    使用ffmpeg检查并提取字幕轨道
    """
```

#### 3.3.4 `audio_subtitle.py` (音频识别)

**功能**:
- 从视频提取音频
- 使用Whisper进行语音识别
- 支持中文和英文识别

**核心函数**:
```python
def extract_from_audio(
    video_path: str,
    language: str = "zh",
    progress_callback: Optional[Callable] = None
) -> Dict[str, Any]:
    """
    从视频音频中识别字幕
    使用OpenAI Whisper进行语音转文字
    """
```

### 3.4 后端API增强

在 `app.py` 中添加进度报告机制，使用Server-Sent Events (SSE) 推送处理进度。

### 3.5 前端增强

#### 3.5.1 处理过程展示

**步骤指示器**:
1. ✅ 解析视频链接
2. 🔄 下载视频文件
3. 🔄 提取字幕信息
   - 尝试从元数据提取
   - 尝试从视频提取
   - 尝试从音频识别
4. ✅ 生成Markdown文件
5. ✅ 完成处理

**进度条**:
- 每个步骤的进度百分比
- 实时状态更新

**日志展示**:
- 实时显示处理日志
- 支持展开/收起详情

#### 3.5.2 结果展示

**视频信息卡片**:
- 视频封面
- 标题、作者
- 视频链接

**字幕内容展示**:
- 带时间戳的字幕列表
- 可滚动查看
- 支持搜索

**Markdown预览**:
- 实时预览生成的Markdown
- 下载按钮
- 复制内容按钮

**来源标识**:
- 显示字幕来源（元数据/视频/音频）
- 音频识别显示置信度

### 3.6 Markdown格式设计

字幕Markdown文件格式：

```markdown
# {视频标题}

## 基本信息
- **来源**: {字幕来源}
- **视频链接**: {原始链接}
- **作者**: {作者}
- **提取时间**: {时间}

---

## 字幕内容

| 时间 | 字幕 |
|------|------|
| {时间戳0} | {字幕文本0} |
| {时间戳1} | {字幕文本1} |
...

---

## 完整文本

{合并的完整文本内容}
```

## 4. 文件修改清单

### 4.1 后端 - 新增文件
1. `backend/src/modules/subtitle_extractor/__init__.py`
2. `backend/src/modules/subtitle_extractor/subtitle_extractor.py`
3. `backend/src/modules/subtitle_extractor/metadata_subtitle.py`
4. `backend/src/modules/subtitle_extractor/video_subtitle.py`
5. `backend/src/modules/subtitle_extractor/audio_subtitle.py`

### 4.2 后端 - 修改文件
1. `backend/requirements.txt` - 添加新依赖
2. `backend/src/app.py` - 集成字幕提取功能，添加SSE进度推送

### 4.3 前端 - 修改文件
1. `frontend/src/App.jsx` - 添加处理步骤展示和结果展示
2. `frontend/src/App.css` - 添加新界面样式

## 5. 实现步骤

### 阶段1: 后端基础设施搭建
1. 创建 `subtitle_extractor` 模块目录结构
2. 更新 `requirements.txt`
3. 创建 `__init__.py` 导出接口

### 阶段2: 后端元数据字幕提取
1. 实现 `metadata_subtitle.py`
2. 增强 `video_fetcher.py` 提取更多元数据
3. 添加测试

### 阶段3: 后端视频字幕提取
1. 实现 `video_subtitle.py`
2. 集成ffmpeg
3. 添加字幕格式转换

### 阶段4: 后端音频字幕提取
1. 实现 `audio_subtitle.py`
2. 集成Whisper
3. 添加音频预处理和进度回调

### 阶段5: 后端主模块集成
1. 实现 `subtitle_extractor.py` 主协调逻辑
2. 实现Markdown格式化
3. 集成到 `app.py` API
4. 添加SSE进度推送

### 阶段6: 前端处理过程展示
1. 添加步骤指示器组件
2. 添加进度条组件
3. 添加实时日志展示
4. 集成SSE接收进度

### 阶段7: 前端结果展示
1. 添加视频信息卡片
2. 添加字幕内容展示区
3. 添加Markdown预览
4. 添加下载/复制功能

### 阶段8: 测试与优化
1. 完整流程测试
2. 错误处理优化
3. 性能调优
4. UI/UX优化

## 6. 风险与注意事项

### 6.1 依赖风险
- Whisper模型下载可能需要较长时间
- FFmpeg需要系统安装

**缓解措施**:
- 提供安装指引
- 添加依赖检查和友好错误提示
- 前端显示模型下载进度

### 6.2 性能风险
- Whisper处理长视频可能较慢
- 大文件处理内存占用高

**缓解措施**:
- 提供进度提示
- 分块处理机制
- 可配置模型大小
- 前端显示预计剩余时间

### 6.3 质量风险
- 音频识别准确率受限于语音质量
- 元数据可能不完整

**缓解措施**:
- 多级降级策略
- 置信度标注
- 允许人工修正

## 7. 输出结果

完成后将实现：
1. **后端**: 完整的三级字幕提取系统
2. **后端**: Markdown格式输出
3. **后端**: SSE实时进度推送
4. **前端**: 处理过程步骤展示（步骤指示器、进度条、日志）
5. **前端**: 结果展示（视频信息、字幕内容、Markdown预览）
6. **集成**: 与现有API无缝集成
7. **完善**: 完善的错误处理和日志
8. **标准**: 可用于LLM Wiki ingest的标准格式
