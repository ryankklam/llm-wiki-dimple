"""
主字幕提取模块
"""
import os
import datetime
import re
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


def _add_punctuation_to_segment(text: str) -> str:
    """
    为单个字幕分段添加合适的标点符号
    
    Args:
        text: 字幕分段文本
    
    Returns:
        添加了标点的文本
    """
    if not text:
        return text
    
    text = text.strip()
    
    # 检查末尾是否已有标点符号
    has_punct = bool(re.search(r'[。！？!?，,；;：:」』」』》》，,、.……]$', text))
    if not has_punct:
        text += '。'
    
    return text


def _process_text_with_timestamps(result: Dict[str, Any]) -> str:
    """
    按时间分段处理文本，添加标点
    
    Args:
        result: 字幕结果字典
    
    Returns:
        处理后的完整文本
    """
    timestamps = result.get('timestamps', [])
    
    if not timestamps:
        # 如果没有时间戳，直接处理整个文本
        text = result.get('text', '')
        return _add_proper_punctuation(text)
    
    # 按时间分段处理每个字幕
    processed_segments = []
    for ts in timestamps:
        segment_text = ts.get('text', '').strip()
        if segment_text:
            processed_text = _add_punctuation_to_segment(segment_text)
            processed_segments.append(processed_text)
    
    return ''.join(processed_segments)


def _add_proper_punctuation(text: str) -> str:
    """
    为完整文本添加合适的标点符号（备用方法）
    
    Args:
        text: 原始文本
    
    Returns:
        添加了标点的文本
    """
    if not text:
        return text
    
    # 首先清理多余的空行
    cleaned_text = re.sub(r'\n\s*\n', '\n\n', text.strip())
    
    # 为每行末尾添加合适的标点
    lines = cleaned_text.split('\n')
    processed_lines = []
    
    for line in lines:
        line = line.strip()
        if not line:
            processed_lines.append('')
            continue
        
        # 检查末尾是否已有标点符号
        has_punct = bool(re.search(r'[。！？!?，,；;：:」』」』》》，,、.……]$', line))
        if not has_punct:
            line += '。'
        
        processed_lines.append(line)
    
    return '\n'.join(processed_lines)


def _format_and_save(
    result: Dict[str, Any],
    video_info: Dict[str, Any],
    output_dir: str
) -> Dict[str, Any]:
    """格式化字幕并保存为Markdown文件"""
    try:
        # 生成文件名（包含时间戳，时分秒用下划线）
        video_id = video_info.get('video_id', 'unknown')
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d-%H_%M_%S')
        
        # 带时间戳的字幕文件
        md_filename = f'{video_id}-{timestamp}_timestamps.md'
        md_path = os.path.join(output_dir, md_filename)
        
        # 构建带时间戳的Markdown内容
        md_content = _build_markdown_content(result, video_info)
        
        # 保存带时间戳的文件
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        print(f"Subtitles with timestamps saved to: {md_path}")
        
        # 额外输出不带时间戳的纯文字字幕文件
        text_filename = f'{video_id}-{timestamp}.md'
        text_path = os.path.join(output_dir, text_filename)
        
        # 按时间分段处理，添加适当标点
        pure_text = _process_text_with_timestamps(result)
        
        # 构建纯文字文件内容
        text_content = f'# {video_info.get("title", "Untitled")}\n\n'
        text_content += f'## 来源: {result.get("source", "unknown")}\n\n'
        text_content += f'## 完整文本\n\n{pure_text}\n'
        
        # 保存纯文字文件
        with open(text_path, 'w', encoding='utf-8') as f:
            f.write(text_content)
        
        print(f"Text-only subtitles saved to: {text_path}")
        
        return {
            "success": True,
            "subtitles": md_content,
            "source": result.get('source'),
            "confidence": result.get('confidence', 0),
            "md_path": md_path,
            "text_only_path": text_path,
            "timestamps": result.get('timestamps', []),
            "video_info": video_info
        }
        
    except Exception as e:
        print(f"Error formatting and saving: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            "success": False,
            "error": str(e)
        }


def _build_markdown_content(result: Dict[str, Any], video_info: Dict[str, Any]) -> str:
    """构建Markdown格式的字幕内容"""
    title = video_info.get('title', 'Untitled Video')
    author = video_info.get('author', '未知用户')
    original_link = video_info.get('original_link', '')
    source = result.get('source', 'unknown')
    extract_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    video_id = video_info.get('video_id', 'unknown')
    
    timestamps = result.get('timestamps', [])
    full_text = result.get('text', '')
    
    # 构建来源描述
    source_desc = {
        'metadata': '视频元数据',
        'video': '视频内置字幕',
        'audio': 'WHISPER'
    }.get(source, source.upper() if source else '未知')
    
    # 构建Markdown
    md_parts = []
    
    md_parts.append(f'# {title}\n')
    md_parts.append('\n## 视频信息\n')
    md_parts.append(f'- **视频ID**: {video_id}\n')
    md_parts.append(f'- **作者**: {author}\n')
    md_parts.append(f'- **来源**: {original_link}\n')
    md_parts.append(f'- **日期**: {extract_time}\n')
    md_parts.append(f'- **字幕来源**: {source_desc}\n')
    
    if source == 'audio':
        lang = result.get('language', 'zh')
        model = result.get('model', 'small')
        md_parts.append(f'- **识别语言**: {lang}\n')
        md_parts.append(f'- **Whisper模型**: {model}\n')
    
    md_parts.append('\n---\n')
    
    # 字幕内容表格
    if timestamps:
        md_parts.append('\n## 字幕内容\n')
        md_parts.append('\n| 时间 | 字幕 |\n')
        md_parts.append('|------|------|\n')
        
        for ts in timestamps:
            start_str = _format_time(ts.get('start', 0))
            text = ts.get('text', '').replace('|', '\\|').replace('\n', ' ')
            md_parts.append(f'| {start_str} | {text} |\n')
        
        md_parts.append('\n---\n')
    
    # 完整文本
    md_parts.append('\n## 完整文本\n\n')
    md_parts.append(full_text)
    md_parts.append('\n')
    
    return ''.join(md_parts)


def _format_time(seconds: float) -> str:
    """将秒数格式化为时间字符串"""
    try:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        
        if hours > 0:
            return f'{hours:02d}:{minutes:02d}:{secs:02d}'
        else:
            return f'{minutes:02d}:{secs:02d}'
    except Exception:
        return '00:00'
