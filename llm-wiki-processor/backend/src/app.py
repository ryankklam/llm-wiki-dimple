#!/usr/bin/env python3
"""
LLM Wiki Processor 后端应用
提供视频处理 API 接口
使用 Python 内置 HTTP 服务器
"""

import http.server
import socketserver
import json
import urllib.parse
import os
import sys

# 添加模块路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.video_downloader import download_video, parse_xiaohongshu_link, fetch_video_info
from modules.subtitle_extractor import extract_subtitles

PORT = 3001


class RequestHandler(http.server.SimpleHTTPRequestHandler):
    """请求处理器"""
    
    def _send_response(self, status_code, content):
        """发送响应"""
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(content).encode('utf-8'))
    
    def do_OPTIONS(self):
        """处理 OPTIONS 请求"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_GET(self):
        """处理 GET 请求"""
        if self.path == '/api/health':
            self._send_response(200, {'status': 'ok', 'message': 'LLM Wiki Processor is running'})
        elif self.path == '/':
            self._send_response(200, {
                "message": "Welcome to LLM Wiki Processor API",
                "docs": "/docs",
                "health": "/api/health",
                "process": "/api/process"
            })
        else:
            self._send_response(404, {'error': 'Not found'})
    
    def do_POST(self):
        """处理 POST 请求"""
        if self.path == '/api/process':
            try:
                # 读取请求体
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                video_url = data.get('video_url')
                if not video_url:
                    self._send_response(400, {'status': 'error', 'error': 'No video URL provided'})
                    return
                
                # 解析视频链接
                link_info = parse_xiaohongshu_link(video_url)
                if link_info.get('error'):
                    self._send_response(400, {'status': 'error', 'error': link_info['error']})
                    return
                
                video_id = link_info.get('video_id')
                if not video_id:
                    self._send_response(400, {'status': 'error', 'error': 'Invalid video ID'})
                    return
                
                # 获取视频信息（传入原始链接）
                video_info = fetch_video_info(video_id, video_url)
                if video_info.get('error'):
                    self._send_response(500, {'status': 'error', 'error': video_info['error']})
                    return
                
                # 创建临时目录和输出目录
                temp_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'temp')
                output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'output')
                os.makedirs(temp_dir, exist_ok=True)
                os.makedirs(output_dir, exist_ok=True)
                
                # 下载视频
                download_path = download_video(video_info, temp_dir)
                if not download_path:
                    self._send_response(500, {'status': 'error', 'error': 'Failed to download video'})
                    return
                
                # 提取字幕
                subtitle_result = extract_subtitles(
                    download_path,
                    video_info,
                    output_dir
                )
                
                # 构建响应
                response = {
                    "status": "success",
                    "video_info": video_info,
                    "download_path": download_path,
                    "subtitle_result": subtitle_result,
                    "message": "Video processed successfully"
                }
                
                self._send_response(200, response)
                
            except Exception as e:
                print(f"Error processing video: {str(e)}")
                import traceback
                traceback.print_exc()
                self._send_response(500, {'status': 'error', 'error': f'Error processing video: {str(e)}'})
        else:
            self._send_response(404, {'error': 'Not found'})


def main():
    """主函数"""
    print(f'Starting server on port {PORT}...')
    print(f'Server will be available at http://localhost:{PORT}')
    print(f'Health check: http://localhost:{PORT}/api/health')
    print(f'Process endpoint: http://localhost:{PORT}/api/process')
    print('Press Ctrl+C to stop the server')
    
    with socketserver.TCPServer(('', PORT), RequestHandler) as httpd:
        httpd.serve_forever()


if __name__ == '__main__':
    main()
