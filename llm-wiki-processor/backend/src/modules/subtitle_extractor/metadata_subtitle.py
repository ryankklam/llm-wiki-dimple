"""
从视频元数据提取字幕
"""
import re
from typing import Dict, Optional, List


def extract_from_metadata(video_info: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    从视频元数据提取字幕
    
    Args:
        video_info: 视频信息字典，包含原始链接等信息
        
    Returns:
        包含字幕和时间戳的字典，失败返回None
    """
    try:
        subtitles_text = []
        timestamps = []
        
        # 获取视频标题
        title = video_info.get('title', '')
        if title:
            subtitles_text.append(title)
            timestamps.append({
                'start': 0,
                'end': 0,
                'text': title
            })
        
        # 获取视频描述
        description = video_info.get('description', '')
        if description:
            subtitles_text.append(description)
            timestamps.append({
                'start': 0,
                'end': 0,
                'text': description
            })
        
        # 检查是否有元数据笔记内容
        note_content = video_info.get('note_content', '')
        if note_content:
            subtitles_text.append(note_content)
            timestamps.append({
                'start': 0,
                'end': 0,
                'text': note_content
            })
        
        # 如果没有提取到内容，返回None
        if not subtitles_text:
            return None
        
        return {
            'text': '\n\n'.join(subtitles_text),
            'timestamps': timestamps,
            'source': 'metadata'
        }
        
    except Exception as e:
        print(f"Error extracting from metadata: {str(e)}")
        return None
