# -*- coding: utf-8 -*-
# @Project: amateurPythonProject
# @Author: hkl
# @File name: toutiao_from_index
# @Create time: 2021/4/29 13:58

import requests
from pprint import pprint


"""
    爬取今日头条首页分类新闻数据
"""
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
}


def get_signature(encrypt_url):
    url = "http://127.0.0.1:3333/get_signature"
    data = {
        "encrypt_url": encrypt_url
    }
    res = requests.post(url, data=data)
    signature = res.json()['signature']
    print(signature)
    return signature


def main():
    # 今日头条类别信息
    channel_info = {
        "recommmend": {"channel_id": 0, "category": "pc_profile_recommend"},                   # 推荐
        "hot": {"channel_id": 3189398996, "category": "pc_profile_channel"},                   # 热点
        "finance": {"channel_id": 3189399007, "category": "pc_profile_channel"},               # 财经
        "technology": {"channel_id": 3189398999, "category": "pc_profile_channel"},            # 科技
        "entertainment": {"channel_id": 3189398972, "category": "pc_profile_channel"},         # 娱乐
        "sports": {"channel_id": 3189398957, "category": "pc_profile_channel"},                # 体育
        "fashion": {"channel_id": 3189398984, "category": "pc_profile_channel"},               # 时尚
        "food": {"channel_id": 3189399002, "category": "pc_profile_channel"},                  # 美食
        "international": {"channel_id": 3189398968, "category": "pc_profile_channel"},         # 国际
        "health": {"channel_id": 3189398959, "category": "pc_profile_channel"},                # 养生
        "travel": {"channel_id": 3189398983, "category": "pc_profile_channel"},                # 旅游
        "military": {"channel_id": 3189398960, "category": "pc_profile_channel"},              # 军事
        "image": {"channel_id": 5443492141, "category": "pc_profile_channel"},                 # 图片
        "parenting": {"channel_id": 3189399004, "category": "pc_profile_channel"},             # 育儿
        "history": {"channel_id": 3189398965, "category": "pc_profile_channel"},               # 历史
        "game": {"channel_id": 3189398995, "category": "pc_profile_channel"},                  # 游戏
        "digital": {"channel_id": 3189398981, "category": "pc_profile_channel"},               # 数码
    }
    url = "https://www.toutiao.com/api/pc/list/feed"
    for key in channel_info:
        params = {
            "channel_id": channel_info[key]["channel_id"],
            "min_behot_time": 0,
            "category": channel_info[key]["category"],
            # "refresh_count": 1,
            "_signature": get_signature(url)
        }
        res = requests.get(url, params=params, headers=headers)
        pprint(res.json())
        print("---------------------------------------------I'm line--------------------------------------------------")


if __name__ == '__main__':
    main()
