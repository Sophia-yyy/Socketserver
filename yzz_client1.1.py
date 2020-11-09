import socket
import threading
import time

HOST = '127.0.0.1'
POST = 50009
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 建立连接:
s.connect((HOST, POST))


def loop():
    n = 0
    while n < 10:
        n = n + 1
        data_heartbeat = b'$000001#'
        s.sendall(data_heartbeat)
        time.sleep(1)
        print(s.recv(1024).decode("gbk"))  # 打印接收服务端的数据


t = threading.Thread(target=loop, name='LoopThread').start()
