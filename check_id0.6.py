import concurrent.futures
import time
import requests
import json
from datetime import datetime, timedelta
from gooey import Gooey, GooeyParser
import sys

today = datetime.today()
tomorrow = today + timedelta(days=1)


@Gooey(progress_regex=r"^progress: (\d+)/(\d+)$",
       progress_expr="x[0] / x[1] * 100",
       disable_progress_bar_animation=True,
       language='chinese')
def main():
    parser = GooeyParser(description="云窍数据检查")
    parser.add_argument('--token', type=str, help='f12获取token')
    parser.add_argument('--js', widget="CheckBox", action="store_true", metavar="江苏")
    parser.add_argument('--gs', widget="CheckBox", action="store_true", metavar="甘肃")
    parser.add_argument('--hb', widget="CheckBox", action="store_true", metavar="河北")
    parser.add_argument('--tj', widget="CheckBox", action="store_true", metavar="天津")
    parser.add_argument('--sx', widget="CheckBox", action="store_true", metavar="山西")
    parser.add_argument('--nmg', widget="CheckBox", action="store_true", metavar="内蒙古")
    parser.add_argument('--qh', widget="CheckBox", action="store_true", metavar="青海")

    args = parser.parse_args(sys.argv[1:])
    CheckPool = [args.js, args.gs, args.hb, args.tj, args.sx, args.nmg, args.qh]

    poolcicds = choose_pool(CheckPool)
    get_cicd(args.token, poolcicds)
    #print(poolcicd[0])

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
    return poolcicd
def get_cicd(token, poolcicds):
    url = 'http:///portal/monitorAxios/device/adapter/getDevices'
    headers = {

        'content-type': 'application/json;charset=UTF-8',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67',
        'token': token
    }

    for poolcicd in poolcicds:
        count = 0
        dic = {}
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
                        'resourcePoolCiCode': poolcicd
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
        #return dic, count
        check_id(dic, token, poolcicd, count)


def check_id(dic_cicd, token, poolcicd, numbers):
    # ... （保留原有变量初始化和文件打开部分）...
    b_time = today.strftime('%Y-%m-%d') + ' 00:00:00'
    e_time = tomorrow.strftime('%Y-%m-%d') + ' 00:00:00'
    H = today.strftime('%H')
    count = int(H) * 12
    url = 'http:///portal/monitorAxios/device/metricQuery/metricQueryByDevResourceId'
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
    value = pool_dic.get(poolcicd)
    filename = str(value) + '.txt'
    i = 0
    with open(filename, 'a+') as f:
        f.truncate(0)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for key, value in dic_cicd.items():
                future = executor.submit(
                    process_cicd_entry,
                    key,
                    value,
                    b_time,
                    e_time,
                    url,
                    filename,
                    headers,
                    count
                )
                futures.append(future)

            for future in concurrent.futures.as_completed(futures):
                i += 1
                print("progress: {}/{}".format(i, numbers))
                sys.stdout.flush()
                result = future.result()
                print(result)
    f.close()
    # ... （保留文件关闭部分）...


def process_cicd_entry(key, value, b_time, e_time, url, filename, headers, count, ):
    max_retries = 5
    retry_count = 0
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

    def fetch_data():
        response = requests.post(url=url, headers=headers, json=json_data)
        response.raise_for_status()
        return json.loads(response.text)

    while retry_count < max_retries:
        try:
            data = fetch_data()
            if data['data']['total'] < count - 10:
                with open(filename, 'a+') as f:
                    f.write(key + '\t')
                    f.write(str(data['data']['total']) + '\n')
            break
        except requests.RequestException as e:
            print("Error:", e)
            retry_count += 1
            print(f"Retrying... (Attempt {retry_count}/{max_retries})")
            time.sleep(1)

    # 不再需要单独关闭文件，因为每次写入都在 `with open` 语句中完成


if __name__ == "__main__":
    sys.exit(main())
