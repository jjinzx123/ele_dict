'''
code = utf-8
上传字典数据到sql数据库
'''
from pymysql import *
import re
def read_file():
    f = open('./dict.txt')
    pattern = r'(?P<word>[a-z]+)\s+(?P<explanation>[a-z]+.+)'
    while 1:
        line = f.readline()
        if not line:
            f.close()
            break
        # print(line)
        # print(re.findall(pattern,line))
        try:
            env = re.search(pattern,line).groupdict()
        except:
            print('无法匹配，不能导入进数据库')
            continue
        upload_data(**env)
    
def upload_data(word,explanation):
    db = connect(host = 'localhost',user = 'root',password = '123456',database = 'ele_dict',charset = 'utf8')
    cur = db.cursor()
    inse = 'insert into datas(word,explanation) values(%s,%s)'
    try:
        cur.execute(inse,[word,explanation])
        db.commit()
    except:
        db.rollback()
    cur.close()
    db.close()

    
if  __name__ == '__main__':
    read_file()
        