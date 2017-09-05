"""
client class, to simulate a sim client to grab data and preform actions from remote server.
V0.1 2017/04/01 By:cosformula
"""
import base64
import re
import time
from bs4 import BeautifulSoup
import requests
import json

proxiess = None


class Client(object):
    def __init__(self, card_id, password, captcha=''):
        self.card_id = card_id
        self.password = password
        self.captcha_img = ''
        self.captcha = captcha
        self.site = ''
        self.subject = ''
        self.session = requests.Session()
        self.data = ''

    def action(self):
        pass

    def verify_user(self):
        pass

    def format_data(self):
        pass

    def get_json(self):
        pass

    def set_account(self, card_id, password, captcha):
        self.card_id = card_id
        self.password = password
        self.captcha = captcha


class Tiyu(Client):
    proxies = None
    url_prefix = 'http://202.120.127.149:8989/spims'

    def login(self):
        self.s = requests.Session()
        post_data = {'UNumber': self.card_id,
                     'Upwd': self.password,
                     'USnumber': u'上海大学'}
        r = self.session.get(
            self.url_prefix + '/login/index.jsp', timeout=30, proxies=self.proxies)
        r = self.session.post(self.url_prefix + '/login.do?method=toLogin', data=post_data, timeout=30,
                              proxies=self.proxies)
        if r.headers['Content-Length'] == '784':
            self.is_login = True
        return True

    def get_data(self):
        r = self.session.get(
            self.url_prefix + '/exercise.do?method=seacheload', timeout=10, proxies=self.proxies)
        string = r.text
        content = re.search(
            r'<table cellpadding="3" cellspacing="1" class="table_bg">([\s\S]*)</table>', string, flags=0).group(0)
        content = re.sub(
            r'<table cellpadding="3" cellspacing="1" class="table_bg">', '<table>', content)
        self.data = content
        return True

    def to_html(self):
        return self.data

    def to_json(self):
        return {
            'type': 'html',
            'data': self.data
        }


class Services(Client):
    url_prefix = 'http://services.shu.edu.cn'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    def login(self):
        post_data = {
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            'txtUserName': self.card_id,
            'txtPassword': self.password,
            'btnOk': '提交(Submit)'
        }
        r = self.session.post(
            'http://services.shu.edu.cn/Login.aspx', data=post_data, headers=self.headers)
        if r.text.find('用户名密码错误!') == -1 and r.text.find('系统出错了!') == -1 and r.text.find('工号') == -1:
            return True
        return False

    def get_data(self):
        r = self.session.get(
            self.url_prefix + '/User/userPerInfo.aspx', timeout=10)
        name = re.search(
            r'<span id="userName">([\s\S]*?)</span>', r.text, flags=0).group(1)
        nickname = re.search(
            r'<span id="nickname">([\s\S]*?)</span>', r.text, flags=0).group(1)
        self.data = {
            'name': name,
            'nickname': nickname
        }
        self.session.get(self.url_prefix + '/User/Logout.aspx')
        return True

    def to_html(self):
        return self.data

    def to_json(self):
        return self.data


class Lehu(Client):
    url_prefix = 'http://card.lehu.shu.edu.cn'

    def login(self):
        post_data = {'username': self.card_id,
                     'password': self.password,
                     'url': 'http://www.lehu.shu.edu.cn/'}
        r = self.session.post(
            'http://passport.lehu.shu.edu.cn/ShowOrgUserInfo.aspx', data=post_data, timeout=30)
        return r.text != u'1|password|一卡通账号不存在或密码错误！'

    def get_data(self):
        r = self.session.get(
            self.url_prefix + '/CardTradeDetail.aspx', timeout=30)
        content = re.search(
            r'<span id="ctl00_Contentplaceholder1_Label1">([\s\S]*)</form>', r.text, flags=0).group(0)
        self.data = content
        return True

    def to_html(self):
        return self.data

    def to_json(self):
        return {
            'type': 'html',
            'data': self.data
        }


class XK(Client):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    url_prefix = 'http://xk.shu.edu.cn:8080'

    def __init__(self, card_id, password, captcha=''):
        Client.__init__(self, card_id, password, captcha)
        r = self.session.get(
            self.url_prefix + '/Login/GetValidateCode?GetTimestamp()', timeout=20, stream=True)
        self.captcha_img = r.raw.read()

    def login(self):
        post_data = {
            'txtUserName': self.card_id,
            'txtPassword': self.password,
            'txtValiCode': self.captcha}
        r = self.session.post(self.url_prefix + '/',
                              data=post_data, headers=self.headers, timeout=60)
        # if r.text.find(u'验证码错误') != -1 or r.text.find(u'帐号或密码错误')!=-1 or r.text.find(u'教学评估') != -1:
        return r.text.find('首页') != -1

    def get_data(self):
        time.sleep(2)
        r = self.session.get(
            self.url_prefix + '/StudentQuery/CtrlViewQueryCourseTable', timeout=20)
        self.session.get(self.url_prefix + '/Login/Logout')
        string = re.search(
            r'<table class="tbllist">([\s\S]*?)</table>', r.text, flags=0).group(0)
        self.data = string
        return True

    def to_html(self):
        return self.data

    def to_json(self):
        courselist = []
        soup = BeautifulSoup(self.data, "html.parser")
        table = soup.find("table")
        row = table.findAll("tr")
        names = ('no', 'name', 'teacher_no', 'teacher', 'credit',
                 'time', 'place', 'campus', 'q_time', 'q_place')
        for row in table.findAll("tr")[3:]:
            cells = row.findAll("td")
            if len(cells) == 11:
                course = {
                    names[key]: cell.get_text(strip=True) for (key, cell) in enumerate(cells[1:])
                }
                courselist.append(course)
        return json.dumps(courselist)


class Phylab(Client):
    url_prefix = 'http://www.phylab.shu.edu.cn'

    def __init__(self):
        Client.__init__(self)
        r = self.session.get(
            self.url_prefix + '/openexp/index.php/Public/login/', timeout=10)
        self.hash = re.search(
            r'<input type="hidden" name="__hash__" value="([\s\S]*)" />', r.text, flags=0).group(1)
        r = self.session.get(
            self.url_prefix + '/openexp/index.php/Public/verify/', timeout=10, stream=True)
        self.captcha_img = base64.b64encode(r.raw.read()).decode('utf-8')

    def login(self):
        post_data = {'_hash_': self.hash,
                     'account': self.card_id,
                     'ajax': '1',
                     'password': self.password,
                     'verify': self.captcha}
        r = self.session.post(
            self.url_prefix + '/openexp/index.php/Public/checkLogin/', data=post_data, timeout=10)
        return r.text.find(u'false') != -1

    def get_data(self):
        r = self.session.get(
            self.url_prefix + '/openexp/index.php/Public/main', timeout=10)
        string = re.search(
            r'(<TABLE([\s\S]*?)</TABLE>)', r.text, flags=0).group(0)
        string = re.sub(
            r'<TABLE id="checkList" class="list" cellpadding=0 cellspacing=0 >', '<table>', string)
        self.data = content
        return True

    def to_html(self):
        return self.data


class CJ(Client):
    url_prefix = 'http://cj.shu.edu.cn'

    def __init__(self):
        Client.__init__(self)
        r = self.session.get(self.url_prefix + '/', timeout=20)
        r = self.session.get(self.url_prefix + '/User/GetValidateCode?%20%20+%20GetTimestamp()', timeout=20,
                             stream=True)
        self.captcha_img = base64.b64encode(r.raw.read()).decode('utf-8')

    def login(self):
        post_data = {'url': '',
                     'txtUserNo': self.card_id,
                     'txtPassword': self.password,
                     'txtValidateCode': self.captcha}
        r = self.session.post(self.url_prefix + '/',
                              data=post_data, timeout=60)
        r = self.session.get(
            self.url_prefix + '/Home/StudentIndex', timeout=10)
        return r.text.find(u'首页') != -1

    def get_data(self):
        r = self.session.get(
            self.url_prefix + '/StudentPortal/ScoreQuery', timeout=20)
        content = re.search(
            r'<table class="tbllist">([\s\S]*?)</table>', r.text, flags=0).group(0)
        self.data = content
        return True

    def to_html(self):
        return self.data


class ComTest(Client):
    url_prefix = 'http://ea.cc.shu.edu.cn/login'

    def login(self):
        self.s = requests.Session()
        postData = {'username': self.card_id,
                    'password': self.password}
        r = self.s.post(self.url_prefix, data=postData,
                        timeout=30, proxies=proxies)
        if r.text != u'学号或密码错误':
            self.is_login = True
        return True

    def get_data(self):
        string = r.text
        content = re.search(
            r'<table class="table table-hover">([\s\S]*)</form>', string, flags=0).group(0)
        content = re.sub(r'<table class="table table-hover">',
                         '<table>', content)
        self.data = content
        return True

    def to_json(self):
        return {
            'type': 'html',
            'data': self.data
        }
