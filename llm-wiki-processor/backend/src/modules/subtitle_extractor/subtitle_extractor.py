"""
主字幕提取模块
"""
import os
import datetime
from typing import Dict, Optional, List, Callable, Any
from .metadata_subtitle import extract_from_metadata
from .video_subtitle import extract_from_video
from .audio_subtitle import extract_from_audio


def extract_subtitles(
    video_path: str,
    video_info: Dict[str, Any],
    output_dir: str,
    progress_callback: Optional[Callable] = None
) -> Dict[str, Any]:
    """
    提取字幕主函数

    提取策略:
    1. 先尝试从视频元数据提取（需要包含实质性内容）
    2. 失败则从视频流提取
    3. 最后从音频识别

    Args:
        video_path: 视频文件路径
        video_info: 视频信息字典
        output_dir: 输出目录
        progress_callback: 进度回调函数

    Returns:
        包含字幕信息的字典
    """
    try:
        os.makedirs(output_dir, exist_ok=True)

        # 1. 先尝试从元数据提取
        if progress_callback:
            progress_callback({"step": "metadata_extract", "progress": 5, "message": "Trying to extract from metadata..."})

        metadata_result = extract_from_metadata(video_info)

        # 检查元数据是否包含实质内容（不只是标题）
        # 只有当元数据包含描述或笔记内容时才使用，否则继续尝试其他方法
        if metadata_result and len(metadata_result.get('text', '')) > 50:
            print("Successfully extracted from metadata (with substantial content)")
            return _format_and_save(metadata_result, video_info, output_dir)
        else:
            print("Metadata only contains title, trying other methods...")

        # 2. 尝试从视频提取内置字幕
        if progress_callback:
            progress_callback({"step": "video_subtitle", "progress": 15, "message": "Trying to extract from video subtitles..."})

        video_result = extract_from_video(video_path)
        if video_result:
            print("Successfully extracted from video")
            return _format_and_save(video_result, video_info, output_dir)
        else:
            print("No subtitles found in video, trying audio extraction...")

        # 3. 最后从音频识别
        if progress_callback:
            progress_callback({"step": "audio_extract", "progress": 25, "message": "Starting audio extraction and transcription..."})

        audio_result = extract_from_audio(video_path, "zh", progress_callback)
        if audio_result:
            print("Successfully extracted from audio")
            return _format_and_save(audio_result, video_info, output_dir)

        # 都失败了，返回错误
        return {
            "success": False,
            "error": "All subtitle extraction methods failed"
        }

    except Exception as e:
        print(f"Error in extract_subtitles: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            "success": False,
            "error": str(e)
        }


def _format_and_save(
    result: Dict[str, Any],
    video_info: Dict[str, Any],
    output_dir: str
) -> Dict[str, Any]:
    """格式化字幕并保存为Markdown文件"""
    try:
        # 生成文件名
        video_id = video_info.get('video_id', 'unknown')
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d')
        md_filename = f"{timestamp}-{video_id}.md"
        md_path = os.path.join(output_dir, md_filename)

        # 构建Markdown内容
        md_content = _build_markdown_content(result, video_info)

        # 保存文件
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(md_content)

        print(f"Subtitles saved to: {md_path}")

        return {
            "success": True,
            "subtitles": md_content,
            "source": result.get('source'),
            "confidence": result.get('confidence', 0),
            "md_path": md_path,
            "timestamps": result.get('timestamps', [])
        }

    except Exception as e:
        print(f"Error formatting and saving: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


def _build_markdown_content(result: Dict[str, Any], video_info: Dict[str, Any]) -> str:
    """构建Markdown格式的字幕内容"""
    title = video_info.get('title', 'Untitled Video')
    author = video_info.get('author', 'Unknown')
    original_link = video_info.get('original_link', '')
    source = result.get('source', 'unknown')
    extract_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    timestamps = result.get('timestamps', [])
    full_text = result.get('text', '')

    # 构建来源描述
    source_desc = {
        'metadata': '视频元数据（标题/描述）',
        'video': '视频内置字幕轨道',
        'audio': '音频识别（Whisper）'
    }.get(source, source)

    # 构建Markdown
    md_parts = []

    md_parts.append(f"# {title}\n")
    md_parts.append("\n## 基本信息\n")
    md_parts.append(f"- **来源**: {source_desc}\n")
    if original_link:
        md_parts.append(f"- **视频链接**: {original_link}\n")
    md_parts.append(f"- **作者**: {author}\n")
    md_parts.append(f"- **提取时间**: {extract_time}\n")

    md_parts.append("\n---\n")

    # 字幕内容表格
    if timestamps:
        md_parts.append("## 字幕内容\n")
        md_parts.append("\n| 时间 | 字幕 |\n")
        md_parts.append("|------|------|\n")

        for ts in timestamps:
            start_str = _format_time(ts.get('start', 0))
            text = ts.get('text', '').replace('|', '\\|').replace('\n', ' ')
            md_parts.append(f"| {start_str} | {text} |\n")

        md_parts.append("\n---\n")

    # 完整文本
    md_parts.append("## 完整文本\n\n")
    md_parts.append(full_text)
    md_parts.append("\n")

    return ''.join(md_parts)


def _format_time(seconds: float) -> str:
    """将秒数格式化为时间字符串"""
    try:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)

        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes:02d}:{secs:02d}"
    except Exception:
        return "00:00"
