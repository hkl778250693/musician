# -*- coding: utf-8 -*-
# @Project: amateurPythonProject
# @Author: hkl
# @File name: kugou
# @Create time: 2021/2/23 16:45

import time
from hashlib import md5
import json
import requests
import re
import os


class KuGouMusic(object):
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}

    def MD5Encrypt(self, text):
        # 返回当前时间的时间戳(1970纪元后经过的浮点秒数)
        k = time.time()
        k = int(round(k * 1000))
        info = ["NVPh5oo715z5DIWAeQlhMDsWXXQV4hwt", "bitrate=0", "callback=callback123",
                "clienttime={}".format(k), "clientver=2000", "dfid=-", "inputtype=0",
                "iscorrection=1", "isfuzzy=0", "keyword={}".format(text), "mid={}".format(k),
                "page=1", "pagesize=30", "platform=WebFilter", "privilege_filter=0",
                "srcappid=2919", "tag=em", "userid=-1", "uuid={}".format(k), "NVPh5oo715z5DIWAeQlhMDsWXXQV4hwt"]
        # 创建md5对象
        new_md5 = md5()
        info = ''.join(info)
        # 更新哈希对象
        new_md5.update(info.encode(encoding='utf-8'))
        # 加密
        signature = new_md5.hexdigest()
        url = 'https://complexsearch.kugou.com/v2/search/song?callback=callback123&keyword={0}' \
              '&page=1&pagesize=30&bitrate=0&isfuzzy=0&tag=em&inputtype=0&platform=WebFilter&userid=-1' \
              '&clientver=2000&iscorrection=1&privilege_filter=0&srcappid=2919&clienttime={1}&' \
              'mid={2}&uuid={3}&dfid=-&signature={4}'.format(text, k, k, k, signature.upper())
        return url

    def get_html(self, url):
        # 加一个cookie
        cookie = 'kg_mid=61a73ea098eb98e7c6f4fbc66cd7f367; kg_dfid=3LfODQ2G5XMN0x1liv3DeyjX; kg_dfid_collect=d41d8cd98f00b204e9800998ecf8427e; Hm_lvt_aedee6983d4cfc62f509129360d6bb3d=1599906321; Hm_lpvt_aedee6983d4cfc62f509129360d6bb3d=1599922649'.split(
            '; ')
        cookie_dict = {}
        for co in cookie:
            co_list = co.split('=')
            cookie_dict[co_list[0]] = co_list[1]
        try:
            response = requests.get(url, headers=self.headers, cookies=cookie_dict)
            response.raise_for_status()
            response.encoding = 'utf-8'
            return response.text
        except Exception as err:
            print(err)
            return '请求异常'

    def parse_text(self, text):
        count = 0
        hash_list = []
        print('{:*^100}'.format('搜索结果如下'))
        print('{0:{6}<5}{1:{6}<15}{2:{6}<10}{3:{6}<10}{4:{6}<20}{5:{6}<20}'.format('序号', '歌名', '歌手', '时长(s)', '专辑', '专辑ID', chr(12288)))
        print('{:-^104}'.format('-'))
        song_list = json.loads(text)['data']['lists']
        for song in song_list:
            singer_name = song['SingerName']
            # <em>本兮</em> 正则提取
            # 先匹配'</em>'这4中字符, 然后将其替换
            pattern = re.compile('[</em>]')
            singer_name = re.sub(pattern, '', singer_name)
            song_name = song['SongName']
            song_name = re.sub(pattern, '', song_name)
            album_id = song['AlbumID']
            album_name = song['AlbumName']
            # 时长
            duration = song['Duration']
            file_hash = song['FileHash']
            file_size = song['FileSize']

            # 音质为HQ, 高品质
            hq_file_hash = song['HQFileHash']
            hq_file_size = song['HQFileSize']

            # 音质为SQ, 超品质, 即无损, 后缀为flac
            sq_file_hash = song['SQFileHash']
            sq_file_size = song['SQFileSize']

            # MV m4a
            mv_hash = song['MvHash']
            m4a_size = song['M4aSize']

            hash_list.append([file_hash, hq_file_hash, sq_file_hash, album_id])

            print('{0:{6}<5}{1:{6}<15}{2:{6}<10}{3:{6}<10}{4:{6}<20}{5:{6}<20}'.format(count, song_name, singer_name, duration, album_name, album_id,
                                                                             chr(12288)))
            count += 1
            if count == 10:
                # 为了测试方便, 这里只显示了10条数据
                break
        print('{:*^80}'.format('*'))
        return hash_list

    def save_file(self, song_text):
        filepath = './download'
        if not os.path.exists(filepath):
            os.mkdir(filepath)
        text = json.loads(song_text)['data']
        audio_name = text['audio_name']
        author_name = text['author_name']
        album_name = text['album_name']
        img_url = text['img']
        lyrics = text['lyrics']
        play_url = text['play_url']
        print(f"play_url:{play_url}")
        response = requests.get(play_url, headers=self.headers)
        with open(os.path.join(filepath, audio_name) + '.mp3', 'wb') as f:
            f.write(response.content)
            print("下载完毕!")


if __name__ == '__main__':
    kg = KuGouMusic()
    search_info = input("请输入歌名或歌手: ")
    search_url = kg.MD5Encrypt(search_info)

    search_text = kg.get_html(search_url)
    # print(f"search_text:{search_text}")
    hash_list = kg.parse_text(search_text[12:-2])
    print(f"hash_list:{hash_list}")

    while True:
        input_index = eval(input("请输入要下载歌曲的序号(-1退出): "))
        if input_index == -1:
            break
        download_info = hash_list[input_index]
        song_url = 'https://wwwapi.kugou.com/yy/index.php?r=play/getdata&hash={0}&mid=005e51c942c8bcdbbbbaabc961fc3427&album_id={1}'.format(download_info[0], download_info[-1])
        print(f"song_url:{song_url}")
        song_text = kg.get_html(song_url)
        print(f"song_text:{song_text}")
        kg.save_file(song_text)
