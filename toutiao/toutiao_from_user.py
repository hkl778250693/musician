import os
import requests
import json


class NewToutiao():
    def __init__(self,url,type="全部"):
        if type == "全部":
            self.type = "profile_all"
        elif type == "文章":
            self.type = "pc_profile_article"
        elif type == "视频":
            self.type = "pc_profile_video"
        elif type == "微头条":
            self.type = "pc_profile_ugc"
        elif type == "合集":
            self.type = "profile_collection"
        elif type == "问答":
            self.type = "profile_wenda"
        self.max_behot_time = 0
        self.url = url
        self.session = requests.Session()
        # 这个就是返回数据的地方，可以自己封装一下
        while True:
            try:
                content = self.get_data()
                print(content)
            except Exception as e:
                print('已经没有数据了，或者被封IP了')

    # 获取_signature参数
    def get_signature(self,url):
        signature = os.popen('node sign.js {url}'.format(url='"'+url+'"')).read()
        return "&_signature=" + signature.replace('\n', '').replace(' ', '')

    # 获取结果
    def get_data(self):
        token = self.url.split('/')[-1] or self.url.split('/')[-2]
        base_url = 'https://www.toutiao.com/toutiao'
        path = '/api/pc/feed/?category={type}&utm_source=toutiao&visit_user_token={token}&max_behot_time={max_behot_time}'.format(type=self.type, token=token, max_behot_time=self.max_behot_time)
        base_url += path
        signature = self.get_signature(base_url)
        path += signature
        base_url += signature
        headers = {
            'authority': 'www.toutiao.com',
            'method': 'GET',
            'path': path,
            'scheme': 'https',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            # 'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            # 'cookie': 'tt_webid=6914941639271646728; ttcid=08524be5cf054540a905b77885de6fd521; tt_webid=6914941639271646728; csrftoken=039e83eadb6ab2e6f914f7f45929a084; s_v_web_id=verify_kjmo6pbs_EOesm9nQ_kCQH_4The_BSZr_L38GgLJFsKQ8; MONITOR_WEB_ID=1f61fc34-1173-459b-b814-85655b4f1c05; tt_scid=8Zxkg1DsW6cUSbbD1XgqpXo9GGZaI1EUM2zabUHVwVKldLXkZACwghe1dha-TMGsad54',
            'pragma': 'no-cache',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
        }
        response = requests.get(base_url.replace('/toutiao', ''), headers=headers)
        content = json.loads(response.text)
        self.max_behot_time = content['next']['max_behot_time']
        return content


if __name__ == '__main__':
    # 修改用户链接就可以直接获取了，type是你要爬取的类型，比如：全部，文章，视频，微头条等
    NewToutiao('https://www.toutiao.com/c/user/token/MS4wLjABAAAAzHj3Nx8o7swEMOeE61Y8tzeXORNWzcXvBa7NNxQhSFg', type="全部")