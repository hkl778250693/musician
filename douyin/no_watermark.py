# -*- coding: utf-8 -*-
# @Project: plan_win
# @Author: hkl
# @File name: test
# @Create time: 2021/4/23 16:43

import re

import requests

headers = {
    'User-Agent': 'User-Agent", "Mozilla/5.0 (iPhone; CPU iPhone OS 12_1_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16D57 Version/12.0 Safari/604.1',
}

url = 'https://v.douyin.com/JFmwXkr/'  # 抖音分享的链接，自行更改
response = requests.get(url, headers=headers)

now_url = response.url
pat_item_ids = '/video/(.*?)/'
item_ids = re.compile(pat_item_ids, re.S).findall(now_url)

pat_dytk = 'dytk: "(.*?)"'
dytk = re.compile(pat_dytk, re.S).findall(response.text)

url = 'https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/'
params = {
    'item_ids': item_ids,
    # 'dytk': dytk
}
response = requests.get(url, headers=headers, params=params).json()
true_url = response['item_list'][0]['video']['play_addr']['url_list'][0]
true_url = true_url.replace('playwm','play')
response = requests.get(true_url, headers=headers)
true_url = response.url
print(true_url)