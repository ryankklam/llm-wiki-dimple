"""小红书链接解析模块"""

import re
from typing import Dict, Optional


def parse_xiaohongshu_link(link: str) -> Dict[str, Optional[str]]:
    """
    解析小红书视频链接，提取视频ID和其他参数
    
    Args:
        link: 小红书视频链接
    
    Returns:
        包含视频ID和其他参数的字典
    """
    try:
        # 验证链接格式
        if not link or not isinstance(link, str):
            return {'video_id': None, 'error': 'Invalid link format'}
        
        # 处理不同格式的小红书链接
        patterns = [
            # 官方视频链接格式
            r'xiaohongshu\.com/explore/([a-zA-Z0-9]+)',
            # 分享链接格式
            r'xhslink\.com/[^/]+/([a-zA-Z0-9]+)',
            # 其他可能的格式
            r'xiaohongshu\.com/video/([a-zA-Z0-9]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, link)
            if match and match.group(1):
                video_id = match.group(1)
                return {
                    'video_id': video_id,
                    'original_link': link,
                    'error': None
                }
        
        # 未匹配到任何格式
        return {'video_id': None, 'error': 'Unsupported link format'}
        
    except Exception as e:
        return {'video_id': None, 'error': f'Error parsing link: {str(e)}'}


def validate_xiaohongshu_link(link: str) -> bool:
    """
    验证是否为有效的小红书链接
    
    Args:
        link: 链接字符串
    
    Returns:
        是否为有效的小红书链接
    """
    if not link or not isinstance(link, str):
        return False
    
    # 检查是否包含小红书域名
    return 'xiaohongshu.com' in link or 'xhslink.com' in link
