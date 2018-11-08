from pymysql import *
class Mypysql:
    def __init__(self,database,host='localhost',user='root',password='123456',charset='utf8',port=3306):
        self.database = database
        self.host = host
        self.user = user
        self.password = password
        self.charset = charset
        self.port = port

    # 创建数据库连接和游标对象
    def open(self):
        self.db = connect(host=self.host,user=self.user,password=self.password,database=self.database,charset=self.charset,port=self.port)
        self.cur = self.db.cursor()

    # 关闭游标对象和数据库对象
    def close(self):
        self.cur.close()
        self.db.close()
    def zhixing(self,sql,L=[]):
        self.open()
        self.cur.execute(sql,L)
        self.db.commit()
        self.close()
    def all(self,sql,L=[]):
        self.open()
        self.cur.execute(sql,L)
        result = self.cur.fetchall()
        self.close()
        return result
if __name__=='__main__':
    sqlh = Mypysql('db5')
    upd = 'update t1 set score=100 where name ="白居易"'
    sqlh.zhixing(upd)
    sel = 'select * from t1'
    print(sqlh.all(sel))