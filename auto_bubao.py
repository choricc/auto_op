import datetime
import requests
import json
import time

today = datetime.datetime.today().strftime('%Y-%m-%d')


# print(datetime.datetime.today().strftime('%Y-%m-%d'))
class Auto_bubao(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def get_token(self):
        header = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Connection': 'keep-alive',
            'Content-Length': '77',
            'Content-Type': 'application/json;charset=UTF-8',
            'Host': '10.251.3.100:8088',
            'Referer': 'http://10.251.3.100:8088/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203'
        }

        body = {
            'password': self.password,
            'username': self.username,
        }

        s = requests.session()
        login_url = 'http://10.251.3.100:8088/dpmon-integrate/login'
        response = s.post(login_url, headers=header, json=body)
        #print(response.text)
        json_data = json.loads(response.text)
        token = json_data['data']['token']
        #print(token)
        #token = 2
        return token

    def get_num(self, token):
        url = 'http://10.251.3.100:8088/check.txt'
        headers = {

            'content-type': 'application/json;charset=UTF-8',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203',
            'token': token
        }
        respone = requests.get(url=url, headers=headers, timeout=10)
        # print(respone.text)
        data = respone.text
        lines = data.splitlines()
        last_line = lines[-1].strip()
        count = int(last_line)
        #count = 3
        return count

    def bubao(self, token):
        url = 'http://10.251.3.100:8088/dpmon-third-party/monResourceKafka/sendKafkaByDateTime'
        json_date = {
            'datatime': today
        }
        header = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Connection': 'keep-alive',
            'Content-Length': '77',
            'Content-Type': 'application/json;charset=UTF-8',
            'Host': '10.251.3.100:8088',
            'Referer': 'http://10.251.3.100:8088/',
            'token': token,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203',
        }
        feedback = requests.post(url=url, headers=header, json=json_date)
        time.sleep(15)
        json_data = json.loads(feedback.text)
        print(json_data['message'])
        print(json_data['time'])

    def check_num(self, token):
        url = 'http://10.251.3.100:8088/dpmon-third-party/pdbOperationTrappingLog/getPageList'
        headers = {
            'content-type': 'application/json;charset=UTF-8',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203',
            'token': token
        }
        json_data = {
            'implTime': today,
            'pageIndex': '1',
            'pageSize': '20',
        }
        response = requests.post(url=url, headers=headers, json=json_data)
        # print(response.text)
        json_data = json.loads(response.text)
        if 'records' in json_data:
            return True
        else:
            return False
        # print(json_data['data']['records'])

def main():
    auto = Auto_bubao('FYyIjEsZebw0ExeWBjIHpQ', 'CMpiK3gqRSYaOJ0JFy5CLQ==')
    token = auto.get_token()
    count = auto.get_num(token)
    while count < 5830:
        count = auto.get_num(token)
        time.sleep(30)
    status = auto.check_num(token)
    if count > 5830 and status == False:
        auto.bubao(token)

if __name__ == '__main__':
    main()
