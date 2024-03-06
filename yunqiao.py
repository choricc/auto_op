import time
import requests
import json
from datetime import datetime, timedelta
from gooey import Gooey, GooeyParser
import sys

from gooey.gui.formatters import dropdown

from pymysql_comm import UsingMysql

today = datetime.today()
tomorrow = today + timedelta(days=1)


@Gooey(progress_regex=r"^progress: (\d+)/(\d+)$",
       progress_expr="x[0] / x[1] * 100",
       disable_progress_bar_animation=True,
       language='chinese')
def main():
    parser = GooeyParser(description="云窍数据检查")
    parser.add_argument('--token', type=str, widget="TextField",metavar='f12获取token')
    parser.add_argument('--js', widget="CheckBox", action="store_true", metavar="江苏")
    parser.add_argument('--gs', widget="CheckBox", action="store_true", metavar="甘肃")
    parser.add_argument('--hb', widget="CheckBox", action="store_true", metavar="河北")
    parser.add_argument('--tj', widget="CheckBox", action="store_true", metavar="天津")
    parser.add_argument('--sx', widget="CheckBox", action="store_true", metavar="山西")
    parser.add_argument('--nmg', widget="CheckBox", action="store_true", metavar="内蒙古")
    parser.add_argument('--qh', widget="CheckBox", action="store_true", metavar="青海")

    parser.add_argument('--check', type=str, metavar="查询", widget="Dropdown", choices=['江苏',
                                                                                         '甘肃',
                                                                                         '河北',
                                                                                         '天津',
                                                                                         '山西',
                                                                                         '内蒙古',
                                                                                         '广西',
                                                                                         '青海'])

    args = parser.parse_args(sys.argv[1:])
    dic_pool = {
        '江苏': '6180578038500323',
        '甘肃': '6180578038500313',
        '河北': '6180578038500318',
        '天津': '6180578038500334',
        '山西': '6180578038500333',
        '内蒙古': '6180578038500326',
        '广西': '6180578038500314',
        '青海': '6180578038500328'
    }
    CheckPool = [args.js,args.gs,args.hb,args.tj,args.sx,args.nmg,args.qh]
    CheckPool_list,_ = choose_pool(CheckPool)
    _,poolcicd = choose_pool(CheckPool)
    #PoolCicd = dic_pool.get(args.check)
    get_cicd(args.token, poolcicd)
    get_count(args.check)
    #print(CheckPool_list)
    #print(poolcicd)
def choose_pool(poold):
    replace_list = []
    poolcicd = []
    dic_pool = {
        '江苏': '6180578038500323',
        '甘肃': '6180578038500313',
        '河北': '6180578038500318',
        '天津': '6180578038500334',
        '山西': '6180578038500333',
        '内蒙古': '6180578038500326',
        '广西': '6180578038500314',
        '青海': '6180578038500328'
    }
    poolist = ['江苏', '甘肃', '河北', '天津', '山西', '内蒙古', '青海']
    for i in range(len(poold)):
        if poold[i]:
            replace_list.append(poolist[i])
            poolcicd.append(dic_pool.get(poolist[i]))
    return replace_list, poolcicd

def get_cicd(token, poolcicd):
    url = 'http://172.16.21.225/portal/monitorAxios/device/adapter/getDevices'
    headers = {

        'content-type': 'application/json;charset=UTF-8',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67',
        'token': token
    }
    dic = {}
    count = 0
    for i in range(len(poolcicd)):
        for num in range(20):
            json_data = {
                "page":
                    {
                        'current': num + 1,
                        'size': '500',
                        'total': '388894'
                    },
                "query":
                    {
                        'areaCiCode': "6170301785850243",
                        'devType': "Server",
                        'deviceDescribe': "KVM宿主机,裸金属服务器Linux,VMware宿主机,裸金属legacy,裸金属服务器Windows",
                        'deviceStatus': "运行",
                        'exactIp': 'false',
                        'resourcePoolCiCode': poolcicd[i]
                    }
            }
            response = requests.post(url=url, headers=headers, json=json_data)
            # print(response.text)
            json_data = json.loads(response.text)
            for i in range(len(json_data['data']['records'])):
                count += 1
                key = json_data['data']['records'][i]['resourceId']
                value = json_data['data']['records'][i]['ciCode']
                dic[key] = value
        print(count)
        check_id(dic, token, poolcicd[i], count)


def create_one(data_source, resourceId, count, date):
    with UsingMysql(log_time=True) as um:
        sql = "insert into yunqiao_check(data_source,resourceId,count,date) values(%s,%s,%s,%s)"
        params = (data_source, resourceId, count, date)
        um.cursor.execute(sql, params)


def update_by_pk(count, resourceId):
    with UsingMysql(log_time=True) as um:
        sql = "update yunqiao_check set count= '%s' where resourceId= '%s' " % (count, resourceId)
        um.cursor.execute(sql)


def get_count(count, data_source):
    with UsingMysql(log_time=True) as um:
        sql = "select * from yunqiao_check where num < '%s' and data_source='%s'" % (count, data_source)
        um.cursor.execute(sql)

def check_id(dic, token, poolcicd, count):
    b_time = today.strftime('%Y-%m-%d') + ' 00:00:00'
    e_time = tomorrow.strftime('%Y-%m-%d') + ' 00:00:00'
    H = today.strftime('%H')
    num = int(H) * 12
    url = 'http://172.16.21.225/portal/monitorAxios/device/metricQuery/metricQueryByDevResourceId'
    headers = {
        'content-type': 'application/json;charset=UTF-8',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67',
        'token': token
    }
    pool_dic = {
        '6180578038500323': '江苏',
        '6180578038500313': '甘肃',
        '6180578038500318': '河北',
        '6180578038500334': '天津',
        '6180578038500333': '山西',
        '6180578038500326': '内蒙古',
        '6180578038500314': '广西',
        '6180578038500328': '青海'
    }
    for i in range(len(poolcicd)):
        value = pool_dic.get(poolcicd[i])
        # hanzi = str(value)
        data_source = str(value)
        i = 0
        for key, value in dic.items():
            i += 1
            print("progress: {}/{}".format(i, count))
            sys.stdout.flush()
            json_data = {
                "page": {
                    "current": 1,
                    "size": 10
                },
                "query": {
                    "beginTime": b_time,
                    "ciCode": value,
                    "dataSource": [
                        "31省"
                    ],
                    "0": "31省",
                    "endTime": e_time,
                    "maxVal": "",
                    "metricNames": [
                        "cpu_usage_percent"
                    ],
                    "0": "cpu_usage_percent",
                    "minVal": "",
                    "orderBy": "",
                    "timeType": "ts"
                }
            }
            max_retries = 5
            retry_count = 0
            while retry_count < max_retries:
                try:
                    response = requests.post(url=url, headers=headers, json=json_data)
                    response.raise_for_status()  # 检查请求是否成功，如果不成功会抛出异常
                    # data = response.json()  # 尝试将响应内容解析为 JSON
                    # 如果成功获取到数据，可以在这里执行下一行代码
                    # print("Data retrieved successfully:", data)
                    data = json.loads(response.text)
                    check_point = int(data['data']['total'])
                    create_one(data_source, key, check_point, today)
                    break  # 跳出循环，继续执行下一行代码
                except requests.RequestException as e:
                    print("Error:", e)
                    retry_count += 1
                    print(f"Retrying... (Attempt {retry_count}/{max_retries})")
                    time.sleep(1)  # 在重试之前等待一秒
            # response = requests.post(url=url, headers=headers, json=json_data)
            # print(response.text)


if __name__ == "__main__":
    sys.exit(main())
