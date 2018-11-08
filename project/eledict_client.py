from socket import * 
import time
import sys
import getpass
HOST = '127.0.0.1'
PORT = 8000
ADDR = (HOST,PORT)   
def menu1():
    print('+----------------------+')
    print('|1)登录                |')
    print('|2)注册                |')
    print('|q)退出                |')
    print('+----------------------+')

def menu2():
    print('+----------------------+')
    print('|1)查单词              |')
    print('|2)查看历史记录        |')
    print('|q)注销                |')
    print('+----------------------+')

class User(object):
    def __init__(self):
        self.s = socket()
        self.s.connect(ADDR)
    def start(self):
        while 1:
            menu1()
            function = input('请选择：')
            msg1 = 'F '+function
            self.s.send(msg1.encode())
            msg = self.s.recv(1024).decode()
            if msg == 'log':
                self.do_log()
            elif msg == 'register':
                self.do_register()
            elif msg == 'quit':
                print('客户端已退出，谢谢')
                sys.exit()
            else:
                print(msg)

    def do_log(self):
        while 1:
            try:
                username = input('请输入用户名：')
                password = getpass.getpass('请输入密码：')
            except KeyboardInterrupt:
                print('客户端退出')
                self.s.close()
                sys.exit()
            self.s.send(username.encode())
            time.sleep(0.1)
            self.s.send(password.encode())
            msg = self.s.recv(1024).decode()
            if msg == 'error':
                print('输入的用户名不存在或密码错误,请重新输入')
                continue
            elif msg == 'ok':
                print('恭喜，登录成功！')
                self.show_sec(username)
            

    def do_register(self):
        while 1:
            try:
                username = input('请设置你的用户名:')   
            except KeyboardInterrupt:
                print('用户端退出')
                self.s.close()
                break
            if ' ' in username:
                print('错误：用户名不能有空格,请重新输入')
                continue
            self.s.send(username.encode())
            msg = self.s.recv(1024).decode()
            if msg == 'error':
                print('该用户名已存在,请重新设置')
                continue
            elif msg == 'ok':
                print('该用户名可以使用')
                try:
                    password = getpass.getpass('请输入设置密码')
                    password1 = getpass.getpass('请再输入一次密码')
                except KeyboardInterrupt:
                    print('用户端退出')
                    self.s.close()
                    sys.exit()
                if ' ' in password:
                    print('错误：密码不能有空格')
                    continue
                if password != password1:
                    print('错误：密码不一致')
                    continue
                print('恭喜，注册成功，已登录！')
                self.s.send(password.encode())
                self.show_sec(username)
            else:
                print('注册失败')
    
    def show_sec(self,username):  
        while 1:
            menu2()
            try:
                func = input('请选择功能：')
            except KeyboardInterrupt:
                print('用户端退出')
                sys.exit()
            msg2 = 'S ' + func
            self.s.send(msg2.encode())
            print('###')
            msg = self.s.recv(1024).decode()
            print('##')
            if msg == 'lookup':
                self.do_lookup(username) 
            elif msg == 'checkrecords':
                self.do_checkrecords(username)       
            elif msg == 'quit':
                print('返回到第一级界面')
                self.start()
            else:
                print(msg)
              
    def do_lookup(self,username):
        while 1:
            try:
                word = input('请输入要查找的单词，如果退出请输入#:')
            except KeyboardInterrupt:
                sys.exit('客户端退出')
            self.s.send(word.encode())
            time.sleep(0.1)
            self.s.send(username.encode())
            data = self.s.recv(1024).decode()
            if data == '#':
                break
            print('查找结果如下:\r\n',data)

        

    def do_checkrecords(self,username):
        self.s.send(username.encode())
        while 1:
            data2 = self.s.recv(1024).decode()
            if data2 == '##':
                break
            print(data2+'\r\n')
        return



if __name__ == '__main__':
    user = User()
    user.start()