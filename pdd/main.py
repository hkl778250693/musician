import requests
import time
import json
import random
from pprint import pprint

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
    "Referer": "http://yangkeduo.com/catgoods.html?refer_page_name=index&opt_id=2701&opt_name=%E6%98%A5%E4%B8%8A%E6%96%B0&opt_type=2&goods_id=6878644091&refer_page_id=10002_1617933770298_yertpsxcoz&refer_page_sn=10002",
}


def get_anti_content():
    url = "http://127.0.0.1:1111/anti_content"
    data = {
        'scrollEvent': json.dumps([]),
        'mouseDownEvent': json.dumps([
            {
                "clientX": 702,
                "clientY": 837,
                "elementId": "",
                "timestamp": random.randint(2000, 20000),
            }
        ]),
        'href': "http://yangkeduo.com/catgoods.html?refer_page_name=index&opt_id=2701&opt_name=%E6%98%A5%E4%B8%8A%E6%96%B0&opt_type=2&goods_id=6878644091&refer_page_id=10002_1617933770298_yertpsxcoz&refer_page_sn=10002",
        'referrer': headers['Referer'],
        'ua': headers['User-Agent'],
        'requestTimes': 1,
        'initPageTime': int(time.time()),
        'nano_fp': "XpEanqXxnqTJXqTxn9_9_Qhvj9UkbDsVHECcFCqI",
        'pdd_user_id': "",
        'api_uid': "CkkIkWBmdXwLggBZBSO/Ag==",
        'pdd_vds': "gaMFXHZzXhpqphYYMrcqCrMvYYqFzXMXYzMHMzfcCYcFHWCZXzfFrpZzqpfH"
    }
    res = requests.post(url, data=data)
    anti_content = res.json()['anti_content']
    print(anti_content)
    return anti_content


def main():
    url = "http://yangkeduo.com/proxy/api/api/caterham/query/subfenlei_gyl_label"
    params = {
        "pdduid": 0,
        "page_sn": 10028,
        "support_types": "0_4",
        "opt_id": 2706,
        "opt_type": 3,
        "offset": 0,
        "count": 20,
        "list_id": "os7p1dirp9_2706",
        "anti_content": get_anti_content()
    }

    res = requests.get(url=url, headers=headers, params=params)
    pprint(res.json())


if __name__ == "__main__":
    main()
