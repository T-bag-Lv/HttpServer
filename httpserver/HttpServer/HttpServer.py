"""
httpserver.py
功能 : httpserver 部分的主程序
"""
from socket import *
from threading import Thread
from config import *
import re
import json

# 服务器地址
ADDR = (HOST, PORT)

def connect_frame(env):
    """
        实现与frame交互的接口
    :param env: 得到要发送给frame的请求字典
    :return: 从frame得到的数据
    """
    # 建立socket客户端
    sockfd = socket()
    try:
        sockfd.connect((frame_ip, frame_prot))
    except Exception as e:
        print(e)
        return
    # 将env字典转化为json字串  env = {"method":'GET',"info":'/'}
    data = json.dumps(env)
    sockfd.send(data.encode())
    # 从frame接收返回数据(1M)
    data = sockfd.recv(1024*1024).decode()
    # print(data)
    return json.loads(data)  # 将返回的字串转化为字典

# 实现http功能
class HTTPServer:
    def __init__(self):
        self.address = ADDR
        self.create_socket()
        self.bind()

    # 创建套接字
    def create_socket(self):
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, DEBUG)

    # 绑定地址
    def bind(self):
        self.sockfd.bind(self.address)
        self.ip = self.address[0]
        self.port = self.address[1]

    # 启动服务
    def server_forever(self):
        self.sockfd.listen(3)
        print("Listen the port %d"%self.port)
        while True:
            connfd,addr = self.sockfd.accept()
            print("Connect from :",addr)
            # 完成多线程并发模型
            client = Thread(target = self.handle, args = (connfd, ))
            client.setDaemon(True)
            client.start()

    # 处理浏览器请求
    def handle(self, connfd):
        request = connfd.recv(4096).decode()
        # print(request)
        pattern = r"(?P<method>[A-Z]+)\s+(?P<info>/\S*)"
        try:
            env = re.match(pattern, request).groupdict()
        except:
            connfd.close()
            return
        else:
            # data = {"status":'200',"data":'ccccc'}
            data = connect_frame(env)   # 用户与frame交互
            if data:
                self.response(connfd, data)

    # 将data数据组织为response 发送给浏览器
    def response(self, connfd, data):
        if data["status"] == "200":
            responseHeaders = "HTTP/1.1 200 OK\r\n"
            responseHeaders += "Content-Type:text/html\r\n"
            responseHeaders += "\r\n"
            responseBody = data["data"]
        elif data["status"] == "404":
            responseHeaders = "HTTP/1.1 404 Not Found\r\n"
            responseHeaders += "Content-Type:text/html\r\n"
            responseHeaders += "\r\n"
            responseBody = data["data"]
        elif data["status"] == "500":
            pass

        # 将数据发送
        response_data = responseHeaders + responseBody
        connfd.send(response_data.encode())



# 启动服务
httpd = HTTPServer()
httpd.server_forever()
