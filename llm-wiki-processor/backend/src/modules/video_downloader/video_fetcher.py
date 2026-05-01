"""视频信息获取模块"""

import requests
import re
import json
from typing import Dict, Optional, Any
from urllib.parse import urlparse, parse_qs


def fetch_video_info(video_id: str, original_link: Optional[str] = None) -> Dict[str, Any]:
    """
    根据视频ID和原始链接获取视频信息
    
    Args:
        video_id: 视频ID
        original_link: 原始链接（xhslink或小红书链接）
    
    Returns:
        视频信息字典
    """
    try:
        video_url = None
        title = f'小红书视频 {video_id}'
        author = '未知用户'
        description = ''
        cover_url = ''
        
        if original_link:
            print(f"Fetching video info from original link: {original_link}")
            
            # 访问原始链接（跟随重定向）
            response = requests.get(original_link, allow_redirects=True, timeout=30)
            response.raise_for_status()
            
            # 从响应中提取视频URL
            html_content = response.text
            
            # 查找视频URL（支持多种格式）
            video_patterns = [
                r'(https?://[^\s<>"\']+\.mp4)',
                r'(https?://[^\s<>"\']+\.m3u8)',
                r'videoUrl["\']\s*[:=]\s*["\']([^"\']+)',
                r'media["\']\s*[:=]\s*["\']([^"\']+)',
                r'originVideoKey["\']\s*[:=]\s*["\']([^"\']+)',
            ]
            
            for pattern in video_patterns:
                matches = re.findall(pattern, html_content)
                if matches:
                    # 找到第一个匹配的视频URL
                    for match in matches:
                        if match and ('sns-video' in match or '.mp4' in match or '.m3u8' in match):
                            video_url = match
                            print(f"Found video URL: {video_url}")
                            break
                    if video_url:
                        break
            
            # 尝试提取标题
            title_patterns = [
                r'<title>([^<]+)</title>',
                r'"title"["\']\s*[:=]\s*["\']([^"\']+)',
                r'"desc"["\']\s*[:=]\s*["\']([^"\']+)',
            ]
            
            for pattern in title_patterns:
                matches = re.findall(pattern, html_content)
                if matches:
                    title = matches[0].strip()
                    print(f"Found title: {title}")
                    break
            
            # 尝试提取作者
            author_patterns = [
                r'"nickname"["\']\s*[:=]\s*["\']([^"\']+)',
                r'"userName"["\']\s*[:=]\s*["\']([^"\']+)',
            ]
            
            for pattern in author_patterns:
                matches = re.findall(pattern, html_content)
                if matches:
                    author = matches[0].strip()
                    print(f"Found author: {author}")
                    break
        
        # 构建视频信息
        video_info = {
            'video_id': video_id,
            'title': title,
            'author': author,
            'description': description,
            'duration': 0,
            'cover_url': cover_url,
            'video_url': video_url,
            'original_link': original_link,
            'likes': 0,
            'comments': 0,
            'shares': 0,
            'error': None
        }
        
        if not video_url:
            video_info['error'] = 'Could not find video URL'
            print("Warning: Could not find video URL in the page")
        
        return video_info
        
    except Exception as e:
        print(f"Error fetching video info: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            'video_id': video_id,
            'error': f'Error fetching video info: {str(e)}'
        }


def fetch_video_content(video_url: str) -> Optional[bytes]:
    """
    获取视频内容
    
    Args:
        video_url: 视频URL
    
    Returns:
        视频内容字节流或None
    """
    try:
        response = requests.get(video_url, stream=True, timeout=30)
        response.raise_for_status()
        
        # 读取视频内容
        video_content = b''
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                video_content += chunk
        
        return video_content
        
    except Exception as e:
        print(f"Error fetching video content: {str(e)}")
        return None
