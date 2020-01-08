import re
import MySQLdb as mdb
import pymysql


class PymysqlHelper(object):
    """操作mysql数据库，基本方法"""

    def __init__(self, host="localhost", username="root", password="root", port=3306, database="honeybee"):
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.port = port
        self.con = None
        self.cur = None
        # try:
        self.con = pymysql.connect(host=self.host, user=self.username, passwd=self.password, port=self.port,
                                   db=self.database)
        # 所有的查询，都在连接 con 的一个模块 cursor 上面运行的
        self.cur = self.con.cursor()
        # except:
        #     raise ("DataBase connect error,please check the db config.")

    def close(self):
        """关闭数据库连接"""
        if not self.con:
            self.con.close()
        else:
            raise ("DataBase doesn't connect,close connectiong error;please check the db config.")

    def getVersion(self):
        """获取数据库的版本号"""
        self.cur.execute("SELECT VERSION()")
        return self.getOneData()

    def getOneData(self):
        # 取得上个查询的结果，所有结果
        data = self.cur.fetchall()
        return data

    def select(self, tablename, cond_dict='', order='', fields='*'):
        """查询数据
            args：
                tablename  ：表名字
                cond_dict  ：查询条件
                order      ：排序条件
            example：
                print mydb.select(table)
                print mydb.select(table, fields=["name"])
                print mydb.select(table, fields=["name", "age"])
                print mydb.select(table, fields=["age", "name"])
        """
        consql = ' '
        if cond_dict != '':
            for k, v in cond_dict.items():
                consql = consql + k + '=' + v + ' and'
        consql = consql + ' 1=1 '
        if fields == "*":
            sql = 'select * from %s where ' % tablename
        else:
            if isinstance(fields, list):
                fields = ",".join(fields)
                sql = 'select %s from %s where ' % (fields, tablename)
            else:
                raise ("fields input error, please input list fields.")
        sql = sql + consql + order
        print('select:' + sql)
        return self.executeSql(sql)


# 创建连接
# con = pymysql.connect(host="localhost", user="root", password="root", database="study", port=3306)
# cur = con.cursor()  # 创建游标对象


# cur.close()  # 关闭游标连接
# con.close()  # 关闭数据库连接


def select_seq(species=None, gene=None, function=None, seq=None):
    # 编写查询的sqbl
    sql = "select * from gene_seq where gene='%s'and species='%s' and function like '%%%%%s%%%%'" \
          % (gene, species, function)
    try:
        mydb = PymysqlHelper()
        mydb.cur.execute(sql)  # 执行sql
        result = mydb.cur.fetchall()  # 处理结果集
        count = 0  # result为查询结构，count为统计的查询结果条数
        for data in result:
            count += 1
        return result
    except Exception as e:
        print(e)
        print("查询seq序列表数据失败")


def select_loc(species=None, gene=None, chromosome=None, gstart=None, gend=None, direction=None):
    if gene is None:
        sql = """select * from gene_loc where species='{0}'and chromosome='{1}' and gstart>={2} and gend <={3}""" \
            .format(species, chromosome, gstart, gend)
    else:
        sql = """select * from gene_loc where species='{0}'and gene='{1}'""".format(species, gene)
    try:
        mydb = PymysqlHelper()
        mydb.cur.execute(sql)  # 执行sql
        result = mydb.cur.fetchall()  # 处理结果集
        count = 0  # result为查询结构，count为统计的查询结果条数
        for data in result:
            count += 1
        return result
    except Exception as e:
        print(e)
        print("查询loc位置表数据失败")


def select_seqwhere(species=None, function=None):
    str_where = "species='%s' and function like '%%%%%s%%%%'" % (species, function)
    species1 = re.findall(r"species='(.*)' and", str_where)
    function1 = re.findall(r"function like '(.*)'", str_where)
    try:
        if species1 is None:  # 进行子项的判断
            if function1 is None:  # 没有任何查询的限制条件
                where_condition = "None"
            else:
                where_condition = "function like '%%%%%s%%%%'" % (function)
        else:
            if function1 is None:
                where_condition = "species='%s'" % (species)
            else:
                where_condition = "species='%s' and function like '%%%%%s%%%%'" % (species, function)
    except Exception as e:
        print(e)
        print("判断查询条件失败")
    # print(where_condition)
    return where_condition


def select_locwhere(species=None, gene=None, chromosome=None, gstart=None, gend=None, direction=None):
    if gene is None:
        where_condition = """species='{0}'and chromosome='{1}' and gstart>={2} and gend <={3}""" \
            .format(species, chromosome, gstart, gend)
    else:
        where_condition = """species='{0}'and gene='{1}'""".format(species, gene)
    return where_condition


def select_table(where_condition):  # 根据查询条件定位到表
    tablenames = ['gene_loc', 'gene_seq', 'gene_struc']
    try:
        if 'chromosome' in where_condition or 'start' in where_condition \
                or 'end' in where_condition or 'direction' in where_condition \
                or 'gene' in where_condition:
            tablename = tablenames[0]
        elif 'function' in where_condition or 'seq' in where_condition:
            tablename = tablenames[1]
        elif 'struID' in where_condition or 'struName' in where_condition:
            tablename = tablenames[2]
        return tablename
    except Exception as e:
        print(e)
        print("查询所在表失败")


def select_all(table_name, list_view=None, where_condition=None):
    if list_view is not None:
        column = list_view.strip().split()
        str1 = ''
        for i in range(1, len(column)):
            str1 = ',' + str(column[i])
        str_view = str(column[0]) + ''.join(str1)
    else:
        str_view = '*'
    if where_condition is not None:
        sql = "select %s from %s where %s" % (str_view, table_name, where_condition)
    else:
        sql = "select %s from %s" % (str_view, table_name)
    try:
        mydb = PymysqlHelper()
        mydb.cur.execute(sql)  # 执行sql
        result = mydb.cur.fetchall()  # 处理结果集
        # 统计不同物种的基因数量
        number = {"Apis cerana": 0, "Apis dorsata": 0, "Apis florea": 0, "Apis mellifera": 0, "Bombus impatiens": 0}
        for i in range(len(result)):
            if result[i][1] == "Apis cerana":
                number['Apis cerana'] += 1
            elif result[i][1] == "Apis dorsata":
                number['Apis dorsata'] += 1
            elif result[i][1] == "Apis florea":
                number['Apis florea'] += 1
            elif result[i][1] == "Apis mellifera":
                number['Apis mellifera'] += 1
            elif result[i][1] == "Bombus impatiens":
                number['Bombus impatiens'] += 1
        return result, number
    except Exception as e:
        print(e)
        print("查询所有数据失败")


# species1 = "Bombus impatiens"
# gene = "XR_002948017.1"
# print(species1)
# where_condition1 = select_locwhere(species=species1, gene=gene)
# seqs1 = select_all(table_name="gene_loc", where_condition=where_condition1)
# print(len(seqs1[0]),seqs1)
#
# species2 = "Apis cerana"
# chromosome ="NW_016017455.1"
# gstart = 75132
# gend =228222
# print(species2)
# where_condition2 = select_locwhere(species=species2, chromosome=chromosome, gstart=gstart, gend=gend)
# seqs2 = select_all(table_name="gene_loc", where_condition=where_condition2)
# print(len(seqs2[0]),seqs2)