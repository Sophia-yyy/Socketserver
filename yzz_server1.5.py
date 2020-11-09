import socketserver
import time


class Handler(socketserver.BaseRequestHandler):

    def setup(self):
        """连接成功，塞入连接池"""
        self.request.sendall("connect success!".encode(encoding='gbk'))  # 向客户端发送连接成功信息
        print("Connected by ", self.client_address)
        socket_request_pool.append(self.request)  # 当前socket连接对象放入连接池

    def handle(self):
        """ 收到消息处理，异常或空消息，断开连接，心跳则返回消息"""

        try:
            while True:
                self.data = self.request.recv(1024)
                print("online num", len(socket_request_pool))
                if not self.data:
                    print("Connection lost")
                    self.remove()
                    break
                self.data_str = self.data.decode('GBK')  # 接收到的数据从byte-->str ，gbk编码
                self.data_content = self.data_str.strip('$#')  # 去掉首尾字符
                if len(self.data_content) == 6:
                    self.request.sendall(self.data)  # 发送收到的内容,即心跳协议的响应
                    time.sleep(2)
                    print("服务端发送心跳响应成功" + ' ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        except Exception as e:
            print(self.client_address, "Connection lost")
            self.remove()

        finally:
            self.request.close()

    def finish(self):
        """ 环境清理，在handle()之后执行清除操作，默认什么都不做，
        如果setup()和handle()方法都不生成异常,则无需调用该方法"""
        print("client clean", self.client_address)

    def remove(self):
        """连接断开后，从连接池中删除socket对象"""
        print("client remove")
        socket_request_pool.remove(self.request)
        print("online num: ", len(socket_request_pool))


ADDRESS = ('127.0.0.1', 50009)
socket_request_pool = []  # 连接池
server = socketserver.TCPServer(ADDRESS, Handler)
server.serve_forever()
