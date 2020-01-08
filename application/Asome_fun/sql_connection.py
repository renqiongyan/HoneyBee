import pymysql

con = pymysql.connect(
    host="localhost", user="root", password="root", database="honeybee", port=3306
)  # 创建连接
cur = con.cursor()  # 创建游标对象

# cur.close()  # 关闭游标连接
# con.close()  # 关闭数据库连接