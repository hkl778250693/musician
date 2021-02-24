# -*- coding: utf-8 -*-
# @Project: amateurPythonProject
# @Author: hkl
# @File name: aiqiyi_video
# @Create time: 2021/2/24 13:47

import requests
from urllib.parse import unquote

url = "https://vd.l.qq.com/proxyhttp"
headers = {
    # "cookie": "pgv_pvid=3753482398; RK=oQYF/0geW0; ptcz=98a112293f4fb576c811147933f32e6b44d03dfe308767801638bb7a883461bc; o_cookie=778250693; pac_uid=1_778250693; tvfe_boss_uuid=198398c28f645384; appuser=DEC601C4A2FB6C77; psrf_access_token_expiresAt=1621580516; psrf_qqopenid=A73B663BCFD5C76B4A83D901D4BD28A8; tmeLoginType=2; euin=7iSFow4z7wEi; psrf_qqaccess_token=8A004F8C24B770A71E095746078253CA; psrf_qqrefresh_token=227DBC874A31C6EC2AA23832577CAB5E; psrf_qqunionid=; pgv_info=ssid=s898407130; cm_cookie=V1,110064&__M-MZID__&AQEBdLuGeHb0a60m6iZw9iux6iZ609O5ZnRa&210209&210209,110066&UKMEl05QKK10&AQEBdLuGeHb0a63f2oC6YmyoWG0ua-BRyh4b&210205&210223,110279&G6oEl07XPM10&AQEBdLuGeHb0a62fpH0C_2D5PJOqRRPbOMDE&210209&210224; lv_play_index=46; o_minduid=L5u_m3N7-36oY9GiFM1sRssljkWotiZZ; Lturn=59; LKBturn=318; LPVLturn=697; LPLFturn=62; _qpsvr_localtk=0.2883039568368959; uid=42452328",
    # "Range": "bytes=0-",
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}
payload = {"buid":"vinfoad","adparam":"pf=in&ad_type=LD%7CKB%7CPVL&pf_ex=pc&url=https%3A%2F%2Fv.qq.com%2Fx%2Fcover%2F8zqwf5rgbiq4kam.html&refer=https%3A%2F%2Fv.qq.com%2Fchannel%2Fmovie&ty=web&plugin=1.0.0&v=3.5.57&coverid=8zqwf5rgbiq4kam&vid=h0036tgs5o4&pt=&flowid=5638687ce83180e31a97da147486b24f_10201&vptag=www_baidu_com%7C%E9%A1%B6%E9%83%A8%E5%AF%BC%E8%88%AA%E5%8C%BA%3A%E5%A4%B4%E5%83%8F&pu=-1&chid=0&adaptor=2&dtype=1&live=0&resp_type=json&guid=cc0d8af7376c4cf65979236b2ad5a590&req_type=1&from=0&appversion=1.0.157&uid=208879853&tkn=TRinSg0M0B-wPpE3TZ5M_Q..&lt=qq&platform=10201&opid=6E18A5FF9634BA8830D41EF74AB64C62&atkn=4C0363D22490E306BA022CC02E55F796&appid=101483052&tpid=1&rfid=c19885c7edd345079020f009884f6199_1614151654","vinfoparam":"spsrt=1&charge=1&defaultfmt=auto&otype=ojson&guid=cc0d8af7376c4cf65979236b2ad5a590&flowid=5638687ce83180e31a97da147486b24f_10201&platform=10201&sdtfrom=v1010&defnpayver=1&appVer=3.5.57&host=v.qq.com&ehost=https%3A%2F%2Fv.qq.com%2Fx%2Fcover%2F8zqwf5rgbiq4kam.html&refer=v.qq.com&sphttps=1&tm=1614151764&spwm=4&logintoken=%7B%22main_login%22%3A%22qq%22%2C%22openid%22%3A%226E18A5FF9634BA8830D41EF74AB64C62%22%2C%22appid%22%3A%22101483052%22%2C%22access_token%22%3A%224C0363D22490E306BA022CC02E55F796%22%2C%22vuserid%22%3A%22208879853%22%2C%22vusession%22%3A%22TRinSg0M0B-wPpE3TZ5M_Q..%22%7D&unid=e8d3dfab6ab411eb89cd6c92bf48bcb2&vid=h0036tgs5o4&defn=&fhdswitch=0&show1080p=1&isHLS=1&dtype=3&sphls=2&spgzip=1&dlver=2&drm=32&hdcp=0&spau=1&spaudio=15&defsrc=1&encryptVer=9.1&cKey=oYnCG1PWjgF6L5EItZs_lpJX5WB4a2CdS8kFdd8PVaqtHEZQ1c_W6myJ8hQFnmDCG4R5CJCUbjvj2vPBr-xE-uhvZyEMY131vUh1H4pgCXe2OsoF6nD9e7B6yRF3qqJnpX0sVBkIXYfWkOdABnbLUo4RgzSXkBHF3N3K7dNKPg_56X9JO3gwBMyBeAex05x8SbbQKY5AXaDVSM7hsBQ8XEeHzIEGJzlCt94OJgnPQjUjce85npYbs1lnrduiZ-DclSKkRfXJvCgPorVuLVB8vGkZ9SUNglJgQYGpVikdTUgXRIOHHObmqSLLKn50YS2SSf217vSEFHs10rjN4XCGkz9M2B1jN4G6cQZ9VJOeKqjUkL9hI3YkNr-ubL0EBAQEJPXuUQ&fp2p=1&spadseg=3"}
payload = {"buid":"vinfoad","adparam":"pf=in&ad_type=LD%7CKB%7CPVL&pf_ex=pc&url=https%3A%2F%2Fv.qq.com%2Fx%2Fcover%2F8zqwf5rgbiq4kam.html&refer=https%3A%2F%2Fv.qq.com%2Fchannel%2Fmovie&ty=web&plugin=1.0.0&v=3.5.57&coverid=8zqwf5rgbiq4kam&vid=h0036tgs5o4&pt=&flowid=8060135347593c47b2ca7f2c36338870_10201&vptag=www_baidu_com%7Cmovie_v3_new%3Aimg%3A%E6%8B%86%E5%BC%B9%E4%B8%93%E5%AE%B62&pu=-1&chid=0&adaptor=2&dtype=1&live=0&resp_type=json&guid=cc0d8af7376c4cf65979236b2ad5a590&req_type=1&from=0&appversion=1.0.157&uid=208879853&tkn=TRinSg0M0B-wPpE3TZ5M_Q..&lt=qq&platform=10201&opid=6E18A5FF9634BA8830D41EF74AB64C62&atkn=4C0363D22490E306BA022CC02E55F796&appid=101483052&tpid=1&rfid=5ef9fd2d6f01091f95ef0dd6bd94a38c_1614154858","vinfoparam":"spsrt=1&charge=1&defaultfmt=auto&otype=ojson&guid=cc0d8af7376c4cf65979236b2ad5a590&flowid=8060135347593c47b2ca7f2c36338870_10201&platform=10201&sdtfrom=v1010&defnpayver=1&appVer=3.5.57&host=v.qq.com&ehost=https%3A%2F%2Fv.qq.com%2Fx%2Fcover%2F8zqwf5rgbiq4kam.html&refer=v.qq.com&sphttps=1&tm=1614155190&spwm=4&logintoken=%7B%22main_login%22%3A%22qq%22%2C%22openid%22%3A%226E18A5FF9634BA8830D41EF74AB64C62%22%2C%22appid%22%3A%22101483052%22%2C%22access_token%22%3A%224C0363D22490E306BA022CC02E55F796%22%2C%22vuserid%22%3A%22208879853%22%2C%22vusession%22%3A%22TRinSg0M0B-wPpE3TZ5M_Q..%22%7D&unid=e8d3dfab6ab411eb89cd6c92bf48bcb2&vid=h0036tgs5o4&defn=&fhdswitch=0&show1080p=1&isHLS=1&dtype=3&sphls=2&spgzip=1&dlver=2&drm=32&hdcp=0&spau=1&spaudio=15&defsrc=1&encryptVer=9.1&cKey=Av4gxfChbN973pEItZs_lpJX5WB4a2CdS8kFddLtVaqtHEZQ1c_W6myJ8hQFnmDCG4R5CJCUbjvU2vPBr-xE-uhvZyEMY131vUh1H4pgCXe2OsoF6nD9e7B6yRF3qqJnpX0sVBkIXYfWkOdABnbLUo4RgzSXkBHF3N3K7dNKPg_56X9JO3gwBMyBeAex05x8SbbQKY5AXaDVSM7hsBQ8XEeHzIEGJzlCt8VJJAjXQisjJPo_gJVSjFF-rcb6be3-3j6jS-jFlDsiorcxfjOX4sZ1M3_m5y43KO_aZBbbFaNs2dk6K9XRn0H-STghNyTBSK7g76WBQ3w00OvC5Jzt3MOzaIn-MTspF6IosGQDAwN-9bLO&fp2p=1&spadseg=3"}

response = requests.post(url, json=payload, headers=headers)
print(response.text)