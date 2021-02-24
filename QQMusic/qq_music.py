# -*- coding: utf-8 -*-
# @Project: amateurPythonProject
# @Author: hkl
# @File name: wangyiyun
# @Create time: 2021/2/22 14:11

import requests
import re
import json
import os


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/87.0.4280.88 Safari/537.36 "
}
video_num_total = 0


class QQMusicSpider:
    def __init__(self):
        self.page = 0
        self.singer_name = ""
        self.song_name = ""
        self.item = {}
        self.stop_turn_page = False

    def main(self):
        while True:
            url = f"https://c.y.qq.com/soso/fcgi-bin/client_search_cp?p={self.page}&n=99&w={self.singer_name}"
            response = requests.get(url, headers=headers)
            print(response.text)
            music_list = json.loads(re.search(r"callback\((.*)\)", response.text, re.DOTALL).group(1))["data"]["song"]["list"]
            # print(music_list)
            print(len(music_list))
            for music in music_list:
                # print(music)
                self.item["songmid"] = music["songmid"]
                self.item["song_name"] = music["songname"]
                # url_vkey = f"https://u.y.qq.com/cgi-bin/musics.fcg?sign=zzag2kcr41jovhc792dff8670f2cd1c89be66f5cdc2c8099&data=%7B%22req%22%3A%7B%22module%22%3A%22CDN.SrfCdnDispatchServer%22%2C%22method%22%3A%22GetCdnDispatch%22%2C%22param%22%3A%7B%22guid%22%3A%223753482398%22%2C%22calltype%22%3A0%2C%22userip%22%3A%22%22%7D%7D%2C%22req_0%22%3A%7B%22module%22%3A%22vkey.GetVkeyServer%22%2C%22method%22%3A%22CgiGetVkey%22%2C%22param%22%3A%7B%22guid%22%3A%223753482398%22%2C%22songmid%22%3A%5B%22{music['songmid']}%22%5D%2C%22songtype%22%3A%5B0%5D%2C%22uin%22%3A%220%22%2C%22loginflag%22%3A1%2C%22platform%22%3A%2220%22%7D%7D%2C%22comm%22%3A%7B%22uin%22%3A0%2C%22format%22%3A%22json%22%2C%22ct%22%3A24%2C%22cv%22%3A0%7D%7D"
                url_vkey = f"https://u.y.qq.com/cgi-bin/musicu.fcg?format=json&data=%7B%22req_0%22%3A%7B%22module%22%3A%22vkey.GetVkeyServer%22%2C%22method%22%3A%22CgiGetVkey%22%2C%22param%22%3A%7B%22guid%22%3A%223753482398%22%2C%22songmid%22%3A%5B%22{self.item['songmid']}%22%5D%2C%22songtype%22%3A%5B0%5D%2C%22uin%22%3A%22%22%2C%22loginflag%22%3A1%2C%22platform%22%3A%2220%22%7D%7D%2C%22comm%22%3A%7B%22uin%22%3A%22%22%2C%22format%22%3A%22json%22%2C%22ct%22%3A24%2C%22cv%22%3A0%7D%7D"
                # url_vkey = f"https://u.y.qq.com/cgi-bin/musics.fcg?loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0&data=%7B%22req_0%22%3A%7B%22module%22%3A%22vkey.GetVkeyServer%22%2C%22method%22%3A%22CgiGetVkey%22%2C%22param%22%3A%7B%22guid%22%3A%223753482398%22%2C%22songmid%22%3A%5B%22{self.item['songmid']}%22%5D%2C%22songtype%22%3A%5B0%5D%2C%22uin%22%3A%22""%22%2C%22loginflag%22%3A1%2C%22platform%22%3A%2220%22%7D%7D%2C%22comm%22%3A%7B%22uin%22%3A""%2C%22format%22%3A%22json%22%2C%22ct%22%3A24%2C%22cv%22%3A0%7D%7D"
                response = requests.get(url_vkey, headers=headers)
                print(f"vkey:{response.text}")
                downlaod_param = response.json()["req_0"]["data"]["testfile2g"].split("&uin=&fromtag=3")[0]
                downlaod_url = f"https://isure.stream.qqmusic.qq.com/{downlaod_param}&uin=0&fromtag=66"
                self.music_download(downlaod_url)

    def music_download(self, downlaod_url):
        print(f"downlaod_url:{downlaod_url}")
        download_headers = {
            # "Range": "bytes=0-",
            "Host": "ws.stream.qqmusic.qq.com",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9"
        }
        response = requests.get(downlaod_url, headers=download_headers)
        print(response.encoding)
        global video_num_total
        try:
            self.item['music_content'] = response.content
            dir_path = os.path.join("F:/", "")
            if not os.path.exists(dir_path):
                os.makedirs(dir_path, mode=0o777)
                print(f"成功创建dir_path:{dir_path}")
            else:
                print("dir_path已存在")
            music_path = os.path.join(dir_path, f"{self.item['song_name']}.mp4")
            print(f"音乐路径：{music_path}")
            is_exist = os.path.exists(music_path)
        except Exception as e:
            print(f"文件目录创建失败！{e.args}")
        else:
            if not is_exist:
                try:
                    with open(music_path, 'wb') as f:
                        f.write(self.item['music_content'])
                    video_num_total += 1
                    print(self.singer_name + "的歌曲：" + self.item['song_name'] + "下载完成！")
                except Exception as e:
                    print(f"下载失败！{e.args}")
            else:
                print("该音乐已存在，不用重复下载！！")


if __name__ == '__main__':
    qq = QQMusicSpider()
    qq.singer_name = input("请输入歌手名：")
    qq.song_name = input("请输入歌名(不输入默认下载全部歌曲)：")
    qq.main()
