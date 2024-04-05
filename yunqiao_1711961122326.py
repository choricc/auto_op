import time
import requests
import json
from datetime import datetime, timedelta
from gooey import Gooey, GooeyParser
import sys
import pymysql

# 假设有一个config.py文件包含以下配置：
from config import API_URL, headers, token

from gooey.gui.formatters import dropdown
from pymysql_comm import UsingMysql


today = datetime.today()
tomorrow = today + timedelta(days=1)


@Gooey(progress_regex=r"^progress: (\d+)/(\d+)$",
       progress_expr="x[0] / x[1] * 100",
       disable_progress_bar_animation=True,
       language='chinese')
def main():
    # ...
    # 保持函数逻辑不变，注意从config中获取token
    get_cicd(args.token, poolcicd)
    get_count(args.check)


def choose_pool(poold):
    # ...
    return replace_list, poolcicd


def get_cicd(token, poolcicd):
    # 注意使用配置中的URL和headers
    for i in range(len(poolcicd)):
        for num in range(20):
            # ...
            response = requests.post(url=API_URL, headers=headers, json=json_data)
            # ...


class DatabaseManager:
    def __init__(self, log_time=True):
        with UsingMysql(log_time=log_time) as um:
            self.cursor = um.cursor

    def execute_sql(self, sql, params):
        self.cursor.execute(sql, params)
        um.connection.commit()

    def create_one(self, data_source, resourceId, count, date):
        sql = "insert into yunqiao_check(data_source,resourceId,count,date) values(%s,%s,%s,%s)"
        self.execute_sql(sql, (data_source, resourceId, count, date))

    def update_by_pk(self, count, resourceId):
        sql = "update yunqiao_check set count= %s where resourceId= %s "
        self.execute_sql(sql, (count, resourceId))

    def get_count(self, count, data_source):
        sql = "select * from yunqiao_check where num < %s and data_source=%s"
        self.execute_sql(sql, (count, data_source))


def check_id(dic, token, poolcicd, count):
    # ...
    database_manager = DatabaseManager()
    # 使用方法调用进行数据库操作
    # ...


if __name__ == "__main__":
    sys.exit(main())
