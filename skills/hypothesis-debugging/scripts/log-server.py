#!/usr/bin/env python3
"""
Debug Mode 日志收集服务器

启动方式：
    python log-server.py

日志文件：
    日志将写入固定路径 ~/.codeflicker/debug.log

端口：
    默认从 7491 开始，如果被占用自动尝试下一个端口

停止服务：
    按 Ctrl+C
"""

import json
import os
import socket
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime


class LogHandler(BaseHTTPRequestHandler):
    """处理日志收集请求"""
    
    log_file = '.codeflicker/debug.log'
    
    def do_POST(self):
        """接收并存储日志"""
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length == 0:
            self.send_error(400, 'Empty body')
            return
        
        body = self.rfile.read(content_length)
        
        try:
            log_entry = json.loads(body.decode('utf-8'))
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            self.send_error(400, f'Invalid JSON: {e}')
            return
        
        if 'timestamp' not in log_entry:
            log_entry['timestamp'] = int(datetime.now().timestamp() * 1000)
        
        log_dir = os.path.dirname(self.log_file)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)
        
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
        except IOError as e:
            self.send_error(500, f'Failed to write log: {e}')
            return
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(b'{"status":"ok"}')
    
    def do_OPTIONS(self):
        """处理 CORS 预检请求"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_GET(self):
        """健康检查端点"""
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {
                'status': 'ok',
                'log_file': os.path.abspath(self.log_file),
                'exists': os.path.exists(self.log_file)
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_error(404, 'Not found')
    
    def log_message(self, format, *args):
        """静默模式，不输出请求日志"""
        pass


def is_port_available(port):
    """检查端口是否可用"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('127.0.0.1', port))
            return True
        except OSError:
            return False


def find_available_port(start_port=7491, max_attempts=10):
    """从 start_port 开始找一个可用端口"""
    for i in range(max_attempts):
        port = start_port + i
        if is_port_available(port):
            return port
    return None


def main():
    log_file = os.path.expanduser('~/.codeflicker/debug.log')
    LogHandler.log_file = log_file
    
    # 确保日志目录存在
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    # 自动找可用端口
    port = find_available_port()
    if port is None:
        print('ERROR: 无法找到可用端口 (7491-7500)', file=sys.stderr)
        sys.exit(1)
    
    server = HTTPServer(('127.0.0.1', port), LogHandler)
    
    # 输出启动信息（JSON 格式，方便 Agent 解析）
    print(json.dumps({
        'status': 'started',
        'port': port,
        'endpoint': f'http://127.0.0.1:{port}',
        'log_file': log_file
    }))
    sys.stdout.flush()
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == '__main__':
    main()
