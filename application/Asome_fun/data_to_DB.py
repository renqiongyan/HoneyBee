#  ### mysql建数据库导入csv数据
import os
import pandas as pd
from pymysql import connect


class CsvToMysql(object):
    def __init__(self, hostname, port, user, passwd, db):
        self.dbname = db
        self.conn = connect(host=hostname, port=port, user=user, passwd=passwd, db=db)
        self.cursor = self.conn.cursor()

    def read_csv(self, filename):
        df = pd.read_csv(filename, keep_default_na=False, encoding='utf-8')
        table_name = '`' + os.path.split(filename)[-1].split('.')[0].replace(' ', '_') + '`'
        self.csv2mysql(db_name=self.dbname, table_name=table_name, df=df)

    def make_table_sql(self, df):
        columns = df.columns.tolist()  # 将csv中的字段类型转换成mysql中的字段类型
        types = df.ftypes
        make_table = []
        make_field = []
        for item in columns:
            item1 = '`' + item.replace(' ', '_').replace(':', '') + '`'
            if 'int' in types[item]:
                char = item1 + ' INT'
            elif 'float' in types[item]:
                char = item1 + ' FLOAT'
            elif 'object' in types[item]:
                char = item1 + ' VARCHAR(255)'
            elif 'datetime' in types[item]:
                char = item1 + ' DATETIME'
            else:
                char = item1 + ' VARCHAR(255)'
            make_table.append(char)
            make_field.append(item1)
        return ','.join(make_table), ','.join(make_field)

    def csv2mysql(self, db_name, table_name, df):
        field1, field2 = self.make_table_sql(df)
        print
        "create table {} (id int AUTO_INCREMENT not null primary key, {})".format(table_name, field1)
        self.cursor.execute('drop table if exists {}'.format(table_name))
        self.cursor.execute(
            "create table {} (id int AUTO_INCREMENT not null primary key,{})".format(table_name, field1))
        values = df.values.tolist()
        s = ','.join(['%s' for _ in range(len(df.columns))])
        try:
            print
            len(values[0]), len(s.split(','))
            print
            'insert into {}({}) values ({})'.format(table_name, field2, s), values[0]
            self.cursor.executemany('insert into {}({}) values ({})'.format(table_name, field2, s), values)
        except Exception as e:
            print
            e.message
        finally:
            self.conn.commit()


if __name__ == "__main__":
    hostname = '127.0.0.1'
    port = 3306
    user = 'root'
    passwd = 'root'
    db = 'honeybee'
    M = CsvToMysql(hostname=hostname, port=port, user=user, passwd=passwd, db=db)
    # csv文件目录
    dir = 'E:/A`毕业设计/蜜蜂数据处理/蜜蜂test/数据库蜜蜂表/csv文件格式'
    file_list = os.listdir(dir)
    for i in range(len(file_list)):
        file_path = os.path.join(dir, file_list[i])
        if os.path.isfile(file_path):
            M.read_csv(file_path)
