#搭建网络链接
'''
Chatroom
env: python3.5
exc: sockfet and fork
'''
from socket import *
import os,sys

#用于存储用户{name:addr}
user = {}

#处理登录
def do_login(s,name,addr):
    if name in user:
        s.sendto('该用户已存在'.encode(),addr)
        return
    s.sendto('OK'.encode(),addr)
    #通知其他人
    msg = '欢迎 %s 进入聊天室'%name
    for i in user:
        s.sendto(msg.encode(),user[i])
    #将用户加入user
    user[name] = addr

def do_chat(s,name,text):
    msg = '%s : %s'%(name,text)
    for i in user:
        if i != name:
            s.sendto(msg.encode(),user[i])

def do_requests(s):
    while True:
        data,addr = s.recvfrom(1024)
        msgList = data.decode().split(' ')
        #区分请求类型
        if msgList[0] == 'L':
            do_login(s,msgList[1],addr)
        elif msgList[0] == 'C':
            #重新组织消息内容
            text = ' '.join(msgList[2:])
            do_chat(s,msgList[1],text)
        


#创建网络链接
def main():
    ADDR = ('0.0.0.0',8888)
    #创建套接字
    s = socket(AF_INET,SOCK_DGRAM)
    s.bind(ADDR)

    #处理各种客户端请求
    do_requests(s)

if __name__ == '__main__':
    main()