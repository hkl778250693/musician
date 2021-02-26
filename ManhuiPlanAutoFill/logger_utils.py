from functools import wraps
from logging import handlers
from datetime import timedelta, datetime
import os
import time
import logging


class Logger(object):
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }

    def __init__(self, filename, level='info', when='D', backCount=3):
        log_path = os.path.dirname(filename)
        if not os.path.exists(log_path):
            os.mkdir(log_path)
        fmt = '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt)  # 设置日志格式
        self.logger.setLevel(self.level_relations.get(level))  # 设置日志级别
        sh = logging.StreamHandler()  # 往屏幕上输出
        sh.setFormatter(format_str)  # 设置屏幕上显示的格式
        th = handlers.TimedRotatingFileHandler(filename=filename, when=when, backupCount=backCount, encoding='utf-8')#往文件里写入#指定间隔时间自动生成文件的处理器
        # S 秒
        # M 分
        # H 小时、
        # D 天、
        # W 每星期（interval==0时代表星期一）
        # midnight 每天凌晨
        th.setFormatter(format_str)  # 设置文件里写入的格式
        self.logger.addHandler(sh)   # 把对象加到logger里
        self.logger.addHandler(th)


def clock_it(func):
    @wraps(func)
    def inner_func(*args, **kwargs):
        print("EXECUTE FUNC: {}".format(func.__name__))
        print("START TIME: {}".format(time.strftime("%Y-%m-%d-%H-%M-%S")))
        start_time = time.time()
        result = func(*args, **kwargs)
        print("END TIME: {}".format(time.strftime("%Y-%m-%d-%H-%M-%S")))
        end_time = time.time()
        print("EXECUTE TIME: {:.3f} s".format((end_time-start_time)))
        return result
    return inner_func


def parse_pub_time(pub_time):
    pub_time = pub_time.strip()
    now = datetime.now()
    if ':' in pub_time:
        delta = timedelta(days=0)
        n_days = now + delta
        return n_days.strftime('%Y-%m-%d ') + pub_time[:-2]  # 去掉发布两个字
    elif '1天' in pub_time:
        delta = timedelta(days=-1)
        n_days = now + delta
        return n_days.strftime('%Y-%m-%d')
    elif '2天' in pub_time:
        delta = timedelta(days=-2)
        n_days = now + delta
        return n_days.strftime('%Y-%m-%d')
    elif '3天' in pub_time:
        delta = timedelta(days=-3)
        n_days = now + delta
        return n_days.strftime('%Y-%m-%d')
    elif '-' in pub_time:
        return pub_time


def parse_job_addr(ls):
    addr = ''
    for i in ls:
        addr = addr + i.strip()
    return addr.strip('查看地图')


def list_isempty(ls):
    """
    xpath规则的结果可能为空，针对这种情况，不为空返回第一个值，为空返回空串
    :param ls:
    :return:
    """
    if ls:
        return ls[0].strip()
    else:
        return ''
