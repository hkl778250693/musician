# -*- coding: utf-8 -*-
# @Project: amateurPythonProject
# @Author: hkl
# @File name: crawl_video_from_user
# @Create time: 2021/4/25 15:00

import requests

signature = ""

headers = {
    "authority": "www.iesdouyin.com",
    "method": "GET",
    # "path": f"/web/api/v2/aweme/post/?sec_uid=MS4wLjABAAAANheWf682JcUxA1ZjErfjh14I04nvgJO4wLRw0d1-vlo&count=21&max_cursor=0&aid=1128&_signature=oLxPjgAAwERIZm3zgojXBaC8T5&dytk=",
    "scheme": "https",
    "accept": "application/json",
    # "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9",
    "cookie": "_tea_utm_cache_1243={%22utm_source%22:%22copy%22%2C%22utm_medium%22:%22ios%22%2C%22utm_campaign%22:%22client_share%22}",
    "referer": "https://www.iesdouyin.com/share/user/69380181984?u_code=l012gla0&sec_uid=MS4wLjABAAAANheWf682JcUxA1ZjErfjh14I04nvgJO4wLRw0d1-vlo&did=MS4wLjABAAAAtk5a8gUE0_ydLh64wesSMWc6SNFhA-bPFesLg6Vrt2w&iid=MS4wLjABAAAApuHmozJOGpTzlbqI5LehVEL0ux25eDGVN9gcRiuwuOc&with_sec_did=1&app=aweme&utm_campaign=client_share&utm_medium=ios&tt_from=copy&utm_source=copy",
    "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"90\", \"Google Chrome\";v=\"90\"",
    "sec-ch-ua-mobile": "?0",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36",
    # "x-requested-with": "XMLHttpRequest"
}


def get_signature():
    global signature
    uid = "69380181984"  # 用户ID
    # uid = "123"  # 用户ID
    url = "http://127.0.0.1:2222/get_signature"
    data = {
        "uid": uid
    }
    res = requests.post(url, data=data)
    signature = res.json()['signature']
    print(signature)
    return signature


def main():
    url = "https://www.iesdouyin.com/web/api/v2/aweme/post/"
    params = {
        "sec_uid": "MS4wLjABAAAANheWf682JcUxA1ZjErfjh14I04nvgJO4wLRw0d1-vlo",
        "count": 21,
        "max_cursor": 0,
        "aid": 1128,
        "_signature": get_signature(),
        "dytk": ""
    }
    res = requests.get(url=url, headers=headers, params=params)
    print(res.json())


if __name__ == '__main__':
    main()
