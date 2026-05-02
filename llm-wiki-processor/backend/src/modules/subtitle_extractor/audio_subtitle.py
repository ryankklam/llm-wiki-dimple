"""
从音频识别字幕
"""
import subprocess
import os
import tempfile
from typing import Dict, Optional, List, Callable, Any


def extract_from_audio(
    video_path: str,
    language: str = "zh",
    progress_callback: Optional[Callable] = None
) -> Optional[Dict[str, Any]]:
    """
    从视频音频中识别字幕
    
    Args:
        video_path: 视频文件路径
        language: 语言代码，默认为中文
        progress_callback: 进度回调函数
        
    Returns:
        包含字幕和时间戳的字典，失败返回None
    """
    try:
        # 检查视频文件是否存在
        if not os.path.exists(video_path):
            print(f"Video file not found: {video_path}")
            return None
        
        if progress_callback:
            progress_callback({"step": "audio_extraction", "progress": 10, "message": "Extracting audio from video..."})
        
        # 从视频中提取音频
        audio_path = _extract_audio(video_path)
        if not audio_path:
            print("Failed to extract audio")
            return None
        
        try:
            if progress_callback:
                progress_callback({"step": "audio_extraction", "progress": 30, "message": "Loading Whisper model..."})
            
            # 使用Whisper进行语音识别
            result = _transcribe_audio(audio_path, language, progress_callback)
            
            if result:
                return result
            
            return None
            
        finally:
            # 清理音频文件
            if audio_path and os.path.exists(audio_path):
                try:
                    os.unlink(audio_path)
                except Exception:
                    pass
        
    except Exception as e:
        print(f"Error extracting from audio: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def _extract_audio(video_path: str) -> Optional[str]:
    """从视频中提取音频为WAV文件"""
    try:
        # 检查ffmpeg是否可用
        if not _check_ffmpeg():
            print("FFmpeg not available")
            return None
        
        # 创建临时文件
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
            audio_path = tmp.name
        
        try:
            cmd = [
                'ffmpeg', '-i', video_path,
                '-vn', '-acodec', 'pcm_s16le', '-ar', '16000', '-ac', '1',
                '-y', audio_path
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode == 0 and os.path.exists(audio_path):
                return audio_path
            
            # 清理失败时的文件
            if os.path.exists(audio_path):
                os.unlink(audio_path)
            
            return None
            
        except Exception:
            if os.path.exists(audio_path):
                try:
                    os.unlink(audio_path)
                except Exception:
                    pass
            raise
        
    except Exception as e:
        print(f"Error extracting audio: {str(e)}")
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


def _transcribe_audio(
    audio_path: str,
    language: str,
    progress_callback: Optional[Callable] = None
) -> Optional[Dict[str, Any]]:
    """使用Whisper进行语音识别"""
    try:
        # 尝试导入whisper
        try:
            import whisper
        except ImportError:
            print("Whisper not installed, trying to install...")
            import subprocess
            subprocess.run(['pip', 'install', 'openai-whisper'], capture_output=True)
            import whisper
        
        if progress_callback:
            progress_callback({"step": "model_load", "progress": 40, "message": "Loading Whisper model..."})
        
        # 加载模型（使用small模型，平衡速度和准确度）
        model = whisper.load_model("small")
        
        if progress_callback:
            progress_callback({"step": "transcription", "progress": 50, "message": "Starting transcription..."})
        
        # 进行识别
        result = model.transcribe(audio_path, language=language, verbose=True)
        
        if progress_callback:
            progress_callback({"step": "transcription", "progress": 90, "message": "Processing results..."})
        
        # 处理结果
        full_text = result.get('text', '')
        segments = result.get('segments', [])
        
        timestamps = []
        for segment in segments:
            timestamps.append({
                'start': float(segment.get('start', 0)),
                'end': float(segment.get('end', 0)),
                'text': segment.get('text', '').strip()
            })
        
        if progress_callback:
            progress_callback({"step": "complete", "progress": 100, "message": "Transcription complete!"})
        
        return {
            'text': full_text,
            'timestamps': timestamps,
            'source': 'audio',
            'confidence': 0.85  # 模拟置信度
        }
        
    except Exception as e:
        print(f"Error transcribing audio: {str(e)}")
        import traceback
        traceback.print_exc()
        return None
