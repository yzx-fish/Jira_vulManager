#!/usr/bin/python
# _*_ coding:utf-8 _*_

import jira_client
import html_generator
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys
import time


reload(sys)
sys.setdefaultencoding('utf-8')


class VulManager(object):
    def __init__(self):
        self.software_list = ["Memcached", "Apache HTTP Server", "OpenSSH", "nginx", "Tomcat", "MySQL", "Samba",
                              "PHP", "HP SMH"]
        self.jira = jira_client.JiraClient("http://jira.xxx.com:80/", "name", "passwd")
        self.vul_info = {}  # 漏洞查询结果
        self.handlers = set()   # 处理人

    def query_vul(self):
        for software in self.software_list:
            response = self.jira.search(software)
            handler_vul_map = {}
            for issue in response.get("issues"):
                key = issue.get("key")
                summary = issue.get("fields", {}).get("summary").replace(u"【原理扫描】", "")
                handler_name = issue.get("fields", {}).get("assignee", {}).get("name", "").replace("@xxx.com", "")
                if handler_name:
                    if not handler_vul_map.get(handler_name):
                        handler_vul_map[handler_name] = []
                    handler_vul_map[handler_name].append((key, summary))
                    self.handlers.add(handler_name)
            if handler_vul_map:
                self.vul_info[software] = handler_vul_map
        return self.vul_info, self.handlers


class Email(object):
    def __init__(self, subject, mail_to_list, mail_cc_list):
        self.mail_from = "xxx@xxx.com"
        self.passwd = "passwd"
        self.smtp_server = "mail.xxx.com"



        self.port = 587

        self.subject = subject
        self.mail_to = mail_to_list  # 发送
        self.mail_cc = mail_cc_list  # 抄送

    def send_mail(self, html_data):
        mcomroot = MIMEText(html_data, _subtype='html', _charset='utf-8')
        mcomroot['Subject'] = self.subject
        mcomroot['To'] = ", ".join(self.mail_to)
        mcomroot['Cc'] = ", ".join(self.mail_cc)
        mcomroot['From'] = self.mail_from
        send_smtp = smtplib.SMTP(self.smtp_server, self.port)
        send_smtp.ehlo()
        send_smtp.starttls()
        send_smtp.login(self.mail_from, self.passwd)
        send_smtp.sendmail(self.mail_from, self.mail_to + self.mail_cc, mcomroot.as_string())
        send_smtp.close()
        return True


def vul_mail_info():
    vul_info, handlers = VulManager().query_vul()
    html_data = html_generator.Html(vul_info).get_html()
    print html_data
    mail_to = [i+"@xxx.com" for i in handlers]
    mail_cc = ["aaa@xxx.com"]
    print "; ".join(mail_to)
    print "; ".join(mail_cc)
    print Email("漏扫平台安全问题单，请及时修复漏洞 %s" % time.strftime('%Y-%m-%d', time.localtime(time.time())),
                mail_to, mail_cc).send_mail(html_data)


vul_mail_info()

