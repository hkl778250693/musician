# -*- coding: utf-8 -*-
# @Project: amateurPythonProject
# @Author: hkl
# @File name: craw_video_from_user
# @Create time: 2021/4/29 15:37
import os

import requests
from pprint import pprint

headers = {
    "accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Content-Length": "891",
    "content-type": "application/json",
    "Cookie": "did=web_64fd081df37145cb9e35352a014c4bba; clientid=3; client_key=65890b29; kpn=GAME_ZONE; Hm_lvt_86a27b7db2c5c0ae37fee4a8a35033ee=1612763509; didv=1619681123000; kuaishou.live.bfb1s=477cb0011daca84b36b3a4676857e5a1; userId=2212268005; kuaishou.live.web_st=ChRrdWFpc2hvdS5saXZlLndlYi5zdBKgAYYMqcgOGkYViXj9ySOXsj14DlJcZfYaa-WYVn1WRBgPSXQtlpeAWZcdwG5Xr-eNza5YydAM14VsQgHv1iirMs3SmicRo_8-kGTmvfUIGWCWR40EUNvDmFlHfL1KMMU35FoSxtFIA4yCaMutTvyOFO8z8Jr81mXPB46zsQCAngSfawNGVmoNWhrjIqRm_wz2u4iFkjgSWdOO1zrftLVD-6kaEoJNhwQ4OUDtgURWN6k9Xgm8PSIglllnUo3NbrxJWAuCN6aJ5rI1f1IA9RJiY5VmiDxSwBgoBTAB; kuaishou.live.web_ph=fbc23ec454538f8d7ad1c4d3f907ced424aa; userId=2212268005",
    "Host": "live.kuaishou.com",
    "Origin": "https://live.kuaishou.com",
    "Referer": "https://live.kuaishou.com/profile/cqgqt_tuantuan?fid=904372618&cc=share_copylink&followRefer=151&shareMethod=TOKEN&kpn=KUAISHOU&subBiz=PROFILE&shareId=289797088629&shareToken=X-41Ji9QJErVf6sm_A&shareMode=APP&originShareId=289797088629&appType=1&shareObjectId=904372618&shareUrlOpened=0",
    "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"90\", \"Google Chrome\";v=\"90\"",
    "sec-ch-ua-mobile": "?0",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
}

proxies = {
    'http': 'http://1.163.88.127:8088',
    'https': 'http://1.163.88.127:8088'
}


class Kuaishou:
    def __init__(self):
        self.pcursor = ""
        self.url = "https://live.kuaishou.com/live_graphql"

    def parse_video_list(self):
        try:
            while True:
                data = {"operationName": "privateFeedsQuery",
                        "variables": {"principalId": "cqgqt_tuantuan",
                                      "pcursor": self.pcursor,
                                      "count": 24},
                        "query": "query privateFeedsQuery($principalId: String, $pcursor: String, $count: Int) {\n  privateFeeds(principalId: $principalId, pcursor: $pcursor, count: $count) {\n    pcursor\n    list {\n      id\n      thumbnailUrl\n      poster\n      workType\n      type\n      useVideoPlayer\n      imgUrls\n      imgSizes\n      magicFace\n      musicName\n      caption\n      location\n      liked\n      onlyFollowerCanComment\n      relativeHeight\n      timestamp\n      width\n      height\n      counts {\n        displayView\n        displayLike\n        displayComment\n        __typename\n      }\n      user {\n        id\n        eid\n        name\n        avatar\n        __typename\n      }\n      expTag\n      isSpherical\n      __typename\n    }\n    __typename\n  }\n}\n"}
                res = requests.post(self.url, headers=headers, json=data, proxies=proxies, verify=False, timeout=4)
                print(res.json())
                json_data = res.json()
                self.pcursor = json_data["data"]["privateFeeds"]["pcursor"]
                if self.pcursor == "no_more":
                    print("已是最后一页，退出循环")
                    break

                self.parse_video(res)
        except Exception as e:
            print("parse_video_list:", e.args)

    def parse_video(self, response):
        try:
            json_data = response.json()
            video_list = json_data["data"]["privateFeeds"]["list"]
            if len(video_list) == 0:
                return
            for video in video_list:
                item = {}
                item["title"] = video["caption"]
                item["video_id"] = video["id"]
                data = {"operationName": "SharePageQuery",
                        "variables": {"photoId": item["video_id"], "principalId": "cqgqt_tuantuan"},
                        "query": "query SharePageQuery($principalId: String, $photoId: String) {\n  feedById(principalId: $principalId, photoId: $photoId) {\n    currentWork {\n      playUrl\n      __typename\n    }\n    __typename\n  }\n}\n"}
                res = requests.post(self.url, json=data, headers=headers)
                item["play_url"] = res.json()["data"]["feedById"]["currentWork"]["playUrl"]
                self.video_download(item)
        except Exception as e:
            print(e.args)

    def video_download(self, item):
        try:
            header = {
                "Range": "bytes=0-",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
            }
            res = requests.get(item["play_url"], headers=header)
            item['video_content'] = res.content
            dir_path = os.path.join(os.getcwd(), "ks")
            if not os.path.exists(dir_path):
                os.makedirs(dir_path, mode=0o777)
                print(f"成功创建dir_path：{dir_path}")
            else:
                print("文件目录已存在")
            video_path = os.path.join(dir_path, f"{item['title']}.mp4")
            print(video_path)
            is_exist = os.path.exists(video_path)
        except Exception as e:
            print(f"文件目录创建失败！{e.args}")
        else:
            if not is_exist:
                try:
                    with open(video_path, 'wb') as f:
                        f.write(item['video_content'])
                    print("快手视频:" + item['title'] + "下载完成！")
                except Exception as e:
                    print(f"下载失败！{e.args}")
            else:
                print("视频已存在，不用重复下载！")


if __name__ == '__main__':
    ks = Kuaishou()
    ks.parse_video_list()
