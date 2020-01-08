# ###数据库创建表
import pymysql  # 导入pymysql

# 创建连接
con = pymysql.connect(
host="localhost", user="root", password="root", database="honeybee", port=3306
)

cur = con.cursor()  # 创建游标对象

# 编写创建表的sql
sql_geneLoc = """
    create table Gene_loc(
    species varchar(30) not null,
    gene varchar(50) primary key,
    chromosome varchar(50),
    start varchar(20),
    end varchar(20),
    direction varchar(5)
    )
"""
sql_geneStruc = """
    create table Gene_struc (
    species varchar(30) not null,
    gene varchar(50) primary key,
    struID varchar(40),
    struName varchar(50)
    )
"""

sql_geneSeq = """
    create table Gene_seq (
    species varchar(30) not null,
    gene varchar(50) primary key,
    function varchar(150),
    seq varchar(10000)
    )
"""

try:
    cur.execute(sql_geneLoc)  # 执行创建表的sql
    cur.execute(sql_geneStruc)  # 执行创建表的sql
    cur.execute(sql_geneSeq)  # 执行创建表的sql
    print("创建表成功")
except Exception as e:
    print(e)
    print("创建表失败")
finally:
    cur.close()  # 关闭游标连接
con.close()  # 关闭数据库连接
