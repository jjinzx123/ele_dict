from threading import Thread
from socket import *
from settings import *
from mypysql import *
import time
import sys




class Ele_dict(object):
    def __init__(self):
        self.create_socket()

    def create_socket(self):
        self.s = socket()
        self.s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
        self.s.bind(ADDR)

    def start(self):
        self.s.listen(10)
        print('waiting..')
        while 1:
            try:
                c,addr = self.s.accept()
                print('Connected from',addr)
            except KeyboardInterrupt:
                print('服务器退出')
                self.s.close()
                break
            except Exception as e:
                print('出现错误:',e)
                continue
            dict_client = Thread(target = self.handle,args = (c,) )
            dict_client.setDaemon(True)
            dict_client.start()

    def handle(self,c):
        while 1:
            request = c.recv(1024).decode()
            if not request:
                print('客户端已退出')
                sys.exit()
            request_list = request.split(' ')
            if request_list[0] == 'F':
                if request_list[1] == '1':
                    c.send(b'log')
                    self.do_log(c)
                elif request_list[1] == '2':
                    c.send(b'register')
                    self.do_register(c)
                elif request_list[1] == 'q':
                    c.send(b'quit')
                    c.close()
                    sys.exit('客户端退出')
                else:
                    c.send(b'Wrong instructions!')
            elif request_list[0] == 'S':
                if request_list[1] == '1':
                    c.send(b'lookup')
                    self.do_lookup(c)
                elif request_list[1] == '2':
                    c.send(b'checkrecords')
                    self.do_checkrecords(c)
                elif request_list[1] == 'q':
                    c.send(b'quit')
                else:
                    c.send(b'Wrong instructions!')

    
    def do_log(self,c):
        username = c.recv(1024).decode()
        passwd = c.recv(1024).decode()
        sqlh = Mypysql('ele_dict')
        sel = 'select name,passwd from user where name=%s and passwd=%s'
        info_tuple = sqlh.all(sel,[username,passwd])
        print(info_tuple)
        if info_tuple == ():
            c.send(b'error')
        else:
            c.send(b'ok')   

    
    def do_register(self,c):
        while 1:
            username = c.recv(1024).decode()
            sqlh = Mypysql('ele_dict')
            sel = 'select name from user where name=%s'
            name_tuple = sqlh.all(sel,[username])
            if name_tuple == ():
                c.send(b'ok')
                password = c.recv(1024).decode()
                inse = 'insert into user(name,passwd) values(%s,%s)'
                sqlh.zhixing(inse,[username,password])
                return
            else:
                c.send(b'error')
                continue
    
    
    def do_lookup(self,c):
        while 1:
            word = c.recv(1024).decode()
            print(word)
            name = c.recv(128).decode()
            if word == '#':
                c.send(b'#')
                break
            print(name)
            sqlh = Mypysql('ele_dict')
            sel = 'select word,explanation from datas where word=%s'
            data_tuple = sqlh.all(sel,[word])
            print(data_tuple)
            if data_tuple == ():
                c.send(b'NO WORDS MACTHED')
                
            else:
                data = data_tuple[0][1]
                c.send(data.encode()) 
                inse = 'insert into records(name,word,time) values(%s,%s,%s)'
                sqlh.zhixing(inse,[name,word,time.ctime()])
                




    def do_checkrecords(self,c):
        name = c.recv(128).decode()
        sqlh = Mypysql('ele_dict')
        sel = 'select word,time from records where name=%s'   
        info_tuple = sqlh.all(sel,[name])
        if info_tuple == ():
            c.send(b'NO RECORDS')
        for info in info_tuple:
            word = info[0]
            time1 = info[1]
            data = word +':'+ time1 
            c.send(data.encode())
            time.sleep(0.1)
        time.sleep(0.1)
        c.send(b'##')
               


if __name__ == '__main__':
    edict = Ele_dict()
    edict.start()