import random
import socket
import threading
import uvicorn
import webview
from main import app


def get_unused_port():
    """获取未被使用的端口"""
    while True:
        port = random.randint(1024, 65535)  # 端口范围一般为1024-65535
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.bind(("localhost", port))
            sock.close()
            return port
        except OSError:
            pass


port = get_unused_port()

t = threading.Thread(target=uvicorn.run, args=(app,), kwargs={"port": port})
t.daemon = True
t.start()

# 在PyWebview应用程序中加载FastAPI应用程序的URL
webview.create_window('FastAPI Desktop', f'http://localhost:{port}')
webview.start()