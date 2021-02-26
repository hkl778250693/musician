# -*- coding: utf-8 -*-
# @Project: amateurPythonProject
# @Author: hkl
# @File name: plan_auto_fill
# @Create time: 2021/2/25 17:14

import requests
import time
from selenium import webdriver
from collections import OrderedDict
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import os
from logger_utils import *
import random
from urllib.parse import quote, urlencode

plan_content = {
    "remark": "已完成                 "          # 计划说明内容，自行修改
}


driver_path = "./chromedriver_88.exe"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--start-maximized')  # 设置全屏
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])   # 设置为开发者模式
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument("disable-blink-features=AutomationControlled")
chrome_options.add_argument('--no-sandbox=1')


class LoginUtils:
    """
    满惠日常计划自动填报
    """
    def __init__(self, account_name, pwd, headless=None, proxy=None):
        self.account_name = account_name
        self.pwd = pwd
        self.cookies_cache = {}
        self.session = requests.session()
        self.session.headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
        }
        if headless:
            chrome_options.add_argument(headless)

        if proxy:
            chrome_options.add_argument('--proxy-server={0}'.format(proxy))

        self.browser = webdriver.Chrome(executable_path=driver_path, chrome_options=chrome_options)
        self.wait = WebDriverWait(self.browser, 60)

        self.logger = Logger("log/LoginUtils.log", level="info").logger
        self.cookies_tmp_path = os.path.join(os.getcwd(), "cookies_tmp.txt")
        self.is_login_success = False
        self.item = {}

    # 登陆满惠
    def login(self):
        self.browser.delete_all_cookies()
        self.browser.get('http://www.manhuicloud.com/#/login')
        self.logger.info("准备登录满惠...")
        self.save_browser_cookies()
        user_name = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='username']")))
        # user_name = self.browser.find_element_by_xpath("//input[@id='loginId']")
        user_name.clear()
        self.logger.info(f"输入账号:{self.account_name}")
        user_name.send_keys(self.account_name)
        time.sleep(1)
        password = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='password']")))
        # password = self.browser.find_element_by_xpath("//input[@id='password']")
        password.clear()
        self.logger.info(f"输入密码:{self.pwd}")
        password.send_keys(self.pwd)
        time.sleep(1)
        login_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[@type='button']")))
        login_btn.click()
        time.sleep(1)
        count = 0
        while True:
            try:
                ele = self.browser.find_element_by_xpath("//input[@name='username']")
                print(ele)
                count += 1
                print(f"登陆检测控件循环次数：{count}")
            except NoSuchElementException:
                self.is_login_success = True
                self.logger.info(f"登陆成功~")
                self.save_browser_cookies()
                self.browser.close()
                break
            else:
                if count == 50:
                    self.logger.info(f"登陆失败，检测一哈网络嘛~")

        if self.is_login_success:
            self.logger.info(f"准备获取进行中计划列表...")
            self.get_going_plan()

    def save_browser_cookies(self):
        """
        # 保存selenium自动化获取的cookies，self.browser.get_cookies()返回的是列表
        # 列表每个元素是一个字典：[{'domain': '.youth.cn', 'httpOnly': False, 'name': 'Hm_lpvt_969516094b342230ceaf065c844d82f3', 'path': '/', 'secure': False, 'value': '1610156026'}]
        :return:
        """
        cookie_list = self.browser.get_cookies()
        with open(self.cookies_tmp_path, "w", encoding="utf-8") as f:
            for cookie in cookie_list:
                self.cookies_cache[cookie['name']] = cookie['value']
            self.session.cookies = requests.utils.cookiejar_from_dict(self.cookies_cache)
            f.write(json.dumps(self.cookies_cache))

    # 获取进行时的计划
    def get_going_plan(self):
        url = "http://www.manhuicloud.com/plan/stagingPlan/going"
        page = 0
        while True:
            payload = {
                "pageIndex": str(page),
                "pageSize": "10",
                "nodeName": "",
                "nodePropertyId": "",
                "nodeTypeId": "",
                "itemId": "",
                "yearMonth": "",
                "dateType": "2"
            }
            # 根据执行人筛选的时候提交的表单
            filter_payload = {
                "pageIndex": str(page),
                "pageSize": "10",
                "nodeName": "",
                "nodePropertyId": "",
                "nodeTypeId": "",
                "itemId": "",
                "yearMonth": "",
                "dateType": "2",
                "key": "",
                "executive": "袁洪",
                "responsible": ""
            }
            response = self.session.post(url, data=payload)
            print(response.text)
            json_data = response.json()
            print(f"获取到{json_data['total']}条进行时计划")
            if json_data["total"] == "0":
                print("没有数据，退出while循环")
                break
            # 翻页
            page += 1
            plan_list = json_data["data"]
            for plan in plan_list:
                # (planType=3 月度计划)   (planType=4 日常计划)
                if plan["state"] == "2" and plan["planType"] == "4":
                    self.item["plan_id"] = plan["id"]  # 计划id
                    self.item["node_name"] = plan["nodeName"]  # 节点名称
                    self.item["date"] = plan["beginDate"]  # 填写日期
                    if plan["id"] == "988266":   # 此处用来测试提交一条计划，如果没问题，则删除判断
                        self.submit_plan()

    # 提交计划
    def submit_plan(self):
        url = "http://www.manhuicloud.com/plan/monthlyPlanExecution/saveKeyFruitArchives"
        payload = {
            "data": {
                "detailinfos": [],
                "planNode": {
                    "nodeNames": self.item["node_name"],
                    "isComplete": "1",
                    "rate": "100",
                    "expectDate": "",
                    "overDate": self.item["date"],
                    "planType": "4",
                    "newPlanflag": "0",
                    "releaseManager": "",
                    "fileUrl": "",
                    "fileName": "",
                    "id": self.item['plan_id'],
                    "completeDate": self.item["date"],
                    "remark": plan_content["remark"]      # 计划说明内容自己改
                }
            }
        }
        print(payload)
        response = self.session.post(url, data=urlencode(payload))
        print(response.text)
        if response.json()["code"] == "200":
            print(f"{self.item['node_name']}---计划保存成功~")
            current_time = int(time.time() * 1000)
            url = f"http://www.manhuicloud.com/plan/monthlyPlanExecution/audit?id={int(response.json()['message'])}&_={current_time}"
            res = self.session.get(url)
            print(res.json())
            if res.json()["code"] == "200":
                print(f"{self.item['node_name']}---计划上传成功~")
            else:
                print(f"{self.item['node_name']}---计划上传失败~")
        else:
            print(f"{self.item['node_name']}---计划保存失败~")


if __name__ == '__main__':
    # , headless='--headless'
    # 账号密码改成自己的
    login_util = LoginUtils("huangkuiliang", "456258", headless='--headless')
    login_util.login()
