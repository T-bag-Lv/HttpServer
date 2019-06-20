"""
config.py  配置文件
功能:
httpserver  主程序不希望使用者修改
httpserver  中需要用户提供的信息可以写在配置文件中
"""

# [http server ip 配置]
HOST = "0.0.0.0"
PORT = 8956

# [debug] --> 用户自己决定是否要调试
DEBUG = True

# [frame address]
frame_ip = "127.0.0.1"
frame_prot = 8080