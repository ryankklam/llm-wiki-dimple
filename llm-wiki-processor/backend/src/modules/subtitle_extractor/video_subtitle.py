"""
从视频提取字幕
"""
import subprocess
import os
import re
from typing import Dict, Optional, List


def extract_from_video(video_path: str) -> Optional[Dict[str, Any]]:
    """
    从视频文件提取内置字幕
    
    Args:
        video_path: 视频文件路径
        
    Returns:
        包含字幕和时间戳的字典，失败返回None
    """
    try:
        # 检查ffmpeg是否可用
        if not _check_ffmpeg():
            print("FFmpeg not available")
            return None
        
        # 检查视频文件是否存在
        if not os.path.exists(video_path):
            print(f"Video file not found: {video_path}")
            return None
        
        # 首先检查是否有字幕轨道
        subtitle_tracks = _find_subtitle_tracks(video_path)
        if not subtitle_tracks:
            print("No subtitle tracks found in video")
            return None
        
        print(f"Found {len(subtitle_tracks)} subtitle track(s)")
        
        # 提取第一个字幕轨道
        result = _extract_subtitle_track(video_path, subtitle_tracks[0])
        if result:
            return result
        
        return None
        
    except Exception as e:
        print(f"Error extracting from video: {str(e)}")
        return None


def _check_ffmpeg() -> bool:
    """检查ffmpeg是否可用"""
    try:
        subprocess.run(
            ['ffmpeg', '-version'],
            capture_output=True,
            text=True,
            timeout=10
        )
        return True
    except Exception:
        return False


def _find_subtitle_tracks(video_path: str) -> List[int]:
    """查找视频中的字幕轨道"""
    try:
        cmd = ['ffprobe', '-v', 'error', '-select_streams', 's', '-show_entries', 'stream=index', '-of', 'csv=p=0', video_path]
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        tracks = []
        if result.returncode == 0 and result.stdout:
            for line in result.stdout.strip().split('\n'):
                line = line.strip()
                if line:
                    try:
                        tracks.append(int(line))
                    except ValueError:
                        pass
        
        return tracks
        
    except Exception as e:
        print(f"Error finding subtitle tracks: {str(e)}")
        return []


def _extract_subtitle_track(video_path: str, track_index: int) -> Optional[Dict[str, Any]]:
    """提取指定字幕轨道"""
    try:
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.srt', delete=False) as tmp:
            subtitle_path = tmp.name
        
        try:
            cmd = [
                'ffmpeg', '-i', video_path,
                '-map', f'0:s:{track_index}',
                '-c:s', 'srt',
                '-y', subtitle_path
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0 and os.path.exists(subtitle_path):
                # 解析SRT文件
                text, timestamps = _parse_srt(subtitle_path)
                if text:
                    os.unlink(subtitle_path)
                    return {
                        'text': text,
                        'timestamps': timestamps,
                        'source': 'video'
                    }
            
            # 清理临时文件
            if os.path.exists(subtitle_path):
                os.unlink(subtitle_path)
            
            return None
            
        except Exception:
            if os.path.exists(subtitle_path):
                try:
                    os.unlink(subtitle_path)
                except Exception:
                    pass
            raise
        
    except Exception as e:
        print(f"Error extracting subtitle track: {str(e)}")
        return None


def _parse_srt(srt_path: str) -> tuple[str, List[Dict[str, any]]]:
    """解析SRT字幕文件"""
    try:
        with open(srt_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        subtitles = []
        timestamps = []
        
        # SRT格式解析
        blocks = re.split(r'\n\s*\n', content.strip())
        
        for block in blocks:
            lines = block.strip().split('\n')
            if len(lines) >= 3:
                # 第一行是序号
                # 第二行是时间戳
                # 后面的是字幕文本
                time_line = lines[1]
                text_line = '\n'.join(lines[2:])
                
                # 解析时间戳
                start_sec = _parse_timestamp(time_line.split(' --> ')[0])
                end_sec = _parse_timestamp(time_line.split(' --> ')[1])
                
                subtitles.append(text_line)
                timestamps.append({
                    'start': start_sec,
                    'end': end_sec,
                    'text': text_line
                })
        
        return '\n\n'.join(subtitles), timestamps
        
    except Exception as e:
        print(f"Error parsing SRT: {str(e)}")
        return '', []


def _parse_timestamp(timestamp: str) -> float:
    """解析SRT时间戳为秒"""
    try:
        # 格式: 00:00:00,000
        parts = timestamp.split(':')
        hours = int(parts[0])
        minutes = int(parts[1])
        seconds_part = parts[2].replace(',', '.')
        seconds = float(seconds_part)
        
        return hours * 3600 + minutes * 60 + seconds
        
    except Exception:
        return 0.0
