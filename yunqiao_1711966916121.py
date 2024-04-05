import time
import requests
import json
from datetime import datetime, timedelta
from gooey import Gooey, GooeyParser
import sys
import concurrent.futures

today = datetime.today()
tomorrow = today + timedelta(days=1)


@Gooey(progress_regex=r"^progress: (\d+)/(\d+)$",
       progress_expr="x[0] / x[1] * 100",
       disable_progress_bar_animation=True,
       language='chinese')
def main():
    parser = GooeyParser(description="云窍数据检查")
    parser.add_argument('--token', type=str, help='f12获取token')
    parser.add_argument('--pool', type=str, widget="Dropdown", choices=['江苏',
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
    poolcicd = dic_pool.get(args.pool)
    get_cicd(args.token, poolcicd)
    #print(poolcicd)


def get_cicd(token, poolcicd):
    # ... （保持原有逻辑不变）
    count = get_device_count(token, poolcicd)
    device_ids = dic.keys()
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(check_single_id, token, poolcicd, device_id, count): device_id for device_id in device_ids}
        for future in concurrent.futures.as_completed(futures):
            device_id = futures[future]
            try:
                future.result()  # 这里会捕获由check_single_id抛出的异常
            except Exception as exc:
                print(f"Device ID: {device_id} generated an exception: {exc}")


def check_single_id(token, poolcicd, device_id, total_count):
    # 此处将check_id中针对单一设备id的操作提取出来
    b_time = today.strftime('%Y-%m-%d') + ' 00:00:00'
    e_time = tomorrow.strftime('%Y-%m-%d') + ' 00:00:00'
    value = dic[device_id]
    filename = str(value) + '.txt'

    with open(filename, 'a+') as f:
        f.truncate(0)
        json_data = build_json_data(b_time, e_time, value)
        max_retries = 5
        retry_count = 0
        while retry_count < max_retries:
            try:
                response = requests.post(url, headers=headers, json=json_data)
                response.raise_for_status()
                data = json.loads(response.text)
                if data['data']['total'] < total_count - 10:
                    f.write(device_id + '\t')
                    f.write(str(data['data']['total']) + '\n')
                break
            except requests.RequestException as e:
                print("Error for Device ID: {}, {}".format(device_id, e))
                retry_count += 1
                print(f"Retrying... (Attempt {retry_count}/{max_retries})")
                time.sleep(1)
        f.close()


def get_device_count(token, poolcicd):
    # ... （保持原有逻辑不变）

# 其余辅助函数保持不变...


if __name__ == "__main__":
    sys.exit(main())
