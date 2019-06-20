"""
    用于httpserver的检测
"""

from socket import *
import json

sockfd = socket()
sockfd.bind(("0.0.0.0", 8080))
sockfd.listen(3)


connfd,addr = sockfd.accept()

data = connfd.recv(1024).decode()
print(data)

d = {"status":'200',"data":'From text'}
data = json.dumps(d)
connfd.send(data.encode())

connfd.close()
sockfd.close()
