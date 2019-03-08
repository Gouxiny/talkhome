from socket import *
import os,sys
#服务器地址
ADDR = ('127.0.0.1',8888)

#
def send_msg(s,name):
    while True:
        text = input('发言:')
        msg = 'C %s %s'%(name,text)
        s.sendto(msg.encode(),ADDR)

def recv_sg(s):
    while True:
        data,addr = s.recvfrom(2048)
        print(data.decode())




#创建网络链接
def main():
    s = socket(AF_INET,SOCK_DGRAM)

    while True:
        name = input('请输入姓名:')
        msg = 'L ' + name
        s.sendto(msg.encode(),ADDR)
        #等待回应
        data,addr = s.recvfrom(1024)
        if data.decode() == 'OK':
            print('您已进入聊天室')
            break
        else:
            print(data.decode())
    #创建新的进程
    pid = os.fork()
    if pid < 0:
        sys.exit('Error!!')
    elif pid == 0:
        send_msg(s,name)
    else:
        recv_sg(s)


if __name__ == '__main__':
    main()