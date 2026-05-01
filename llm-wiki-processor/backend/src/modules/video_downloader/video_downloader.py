"""视频下载模块"""

import os
import subprocess
from typing import Dict, Optional, Any
from .link_parser import parse_xiaohongshu_link
from .video_fetcher import fetch_video_info, fetch_video_content


def download_video(video_info: Dict[str, Any], output_dir: str) -> Optional[str]:
    """
    下载视频到指定目录
    
    Args:
        video_info: 视频信息字典
        output_dir: 输出目录
    
    Returns:
        下载的视频文件路径或None
    """
    try:
        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)
        
        # 获取视频ID和原始链接
        video_id = video_info.get('video_id')
        original_link = video_info.get('original_link')
        video_url = video_info.get('video_url')
        
        print(f"Downloading video with ID: {video_id}")
        print(f"Original link: {original_link}")
        print(f"Video URL: {video_url}")
        print(f"Output directory: {output_dir}")
        
        if not video_id:
            print("Error: No video ID provided")
            return None
        
        # 生成输出文件名
        output_filename = f"{video_id}.mp4"
        output_path = os.path.join(output_dir, output_filename)
        print(f"Output path: {output_path}")
        
        # 优先尝试直接下载真实的视频URL
        if video_url and video_url != '' and 'example.com' not in video_url:
            print("Trying direct download first (real video URL)...")
            if _try_direct_download(video_url, output_path):
                print(f"Video downloaded successfully with direct download: {output_path}")
                return output_path
            else:
                print("Direct download failed")
        
        # 尝试使用 yt-dlp 下载原始链接
        if original_link:
            print("Trying to download with yt-dlp using original link...")
            if _try_yt_dlp(original_link, output_path):
                print(f"Video downloaded successfully with yt-dlp: {output_path}")
                return output_path
            else:
                print("yt-dlp failed with original link")
        
        # 尝试使用 you-get 下载原始链接
        if original_link:
            print("Trying to download with you-get using original link...")
            if _try_you_get(original_link, output_dir):
                # you-get 会自动生成文件名
                # 查找下载的文件
                for file in os.listdir(output_dir):
                    if file.endswith('.mp4'):
                        print(f"Video downloaded successfully with you-get: {file}")
                        return os.path.join(output_dir, file)
            else:
                print("you-get failed with original link")
        
        # 尝试使用 yt-dlp 下载视频URL
        if video_url:
            print("Trying to download with yt-dlp using video URL...")
            if _try_yt_dlp(video_url, output_path):
                print(f"Video downloaded successfully with yt-dlp: {output_path}")
                return output_path
            else:
                print("yt-dlp failed with video URL")
        
        # 尝试使用 you-get 下载视频URL
        if video_url:
            print("Trying to download with you-get using video URL...")
            if _try_you_get(video_url, output_dir):
                # you-get 会自动生成文件名
                # 查找下载的文件
                for file in os.listdir(output_dir):
                    if file.endswith('.mp4'):
                        print(f"Video downloaded successfully with you-get: {file}")
                        return os.path.join(output_dir, file)
            else:
                print("you-get failed with video URL")
        
        # 检查是否安装了必要的下载工具
        if not _check_download_tools():
            print("Error: No video download tools installed. Please install yt-dlp or you-get.")
            return None
        
        print("Error: All download methods failed")
        return None
        
    except Exception as e:
        print(f"Error downloading video: {str(e)}")
        return None


def _try_yt_dlp(video_url: str, output_path: str) -> bool:
    """
    使用 yt-dlp 下载视频
    
    Args:
        video_url: 视频URL
        output_path: 输出路径
    
    Returns:
        是否下载成功
    """
    try:
        # 构建 yt-dlp 命令
        command = [
            'yt-dlp',
            '-o', output_path,
            video_url
        ]
        
        # 执行命令
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        return result.returncode == 0
        
    except Exception:
        return False


def _try_you_get(video_url: str, output_dir: str) -> bool:
    """
    使用 you-get 下载视频
    
    Args:
        video_url: 视频URL
        output_dir: 输出目录
    
    Returns:
        是否下载成功
    """
    try:
        # 构建 you-get 命令
        command = [
            'you-get',
            '-o', output_dir,
            video_url
        ]
        
        # 执行命令
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        return result.returncode == 0
        
    except Exception:
        return False


def _try_direct_download(video_url: str, output_path: str) -> bool:
    """
    直接下载视频
    
    Args:
        video_url: 视频URL
        output_path: 输出路径
    
    Returns:
        是否下载成功
    """
    try:
        video_content = fetch_video_content(video_url)
        if video_content:
            with open(output_path, 'wb') as f:
                f.write(video_content)
            return True
        return False
        
    except Exception:
        return False


def _check_download_tools() -> bool:
    """
    检查是否安装了必要的下载工具
    
    Returns:
        是否安装了至少一个下载工具
    """
    try:
        # 检查 yt-dlp
        result = subprocess.run(
            ['yt-dlp', '--version'],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            return True
        
        # 检查 you-get
        result = subprocess.run(
            ['you-get', '--version'],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            return True
        
        return False
        
    except Exception:
        return False
