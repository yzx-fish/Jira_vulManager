#!/usr/bin/python
# _*_ coding:utf-8 _*_
import time

JIRA_URL = "http://jira.xxx.sg:80/browse/"


class Html(object):
    def __init__(self, vul_info):
        self.titles = ["软件名称", "处理人", "漏洞数量", "JIRA问题单"]
        self.vul_info = vul_info

    def get_html(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml">' \
               '<head><meta http-equiv="Content-Type" content="text/html; charset=utf-8" /><body>'
        table_str = Table().get_table(self.titles, self.vul_info)
        html += table_str + "</body></html>"
        return html


class Table(object):
    def __init__(self):
        self.title_table_name = "漏扫平台安全问题单"
        self.title_table_name = '<table width="90%" align="center"><tbody>'\
                                + '<tr class="firstRow"> <td align="center" style="font-size:28px;color:#255E95;">'\
                                + self.title_table_name + '</td></tr>'\
                                + '<tr><td align="right"> 时间：'\
                                + time.strftime('%Y-%m-%d', time.localtime(time.time())) + '        ' + '</td></tr>'\
                                + '<tr><td align="left">' \
                                + '<p>1,该数据取自Jira系统，如安全问题已修改，请将问题单设置为"wait for test",漏扫系统会自动重新扫描，问题不存在则关闭问题单。</p>'\
                                + '<p>2,下列开源软件软件，如果该软件不需要使用，可进行卸载；如果业务需要使用，可进行软件升级处理。</p>' \
                                + '</td></tr>'\
                                + '<tr><td>&nbsp;</td></tr></tbody></table><p></p>'

    def get_table_first_line(self, titles):
        '''
        <tr class="firstRow">
        <td rowspan="2" style="text-align: center;border-color: rgb(12, 12, 12);" width="%17">
            软件名称
        </td>
        <td rowspan="2" style="text-align: center;border-color: rgb(12, 12, 12);" width="%20">
            经办人
        </td>
        <td rowspan="2" style="text-align: center;border-color: rgb(12, 12, 12);" width="%10">
            漏洞数量
        </td>
        <td rowspan="2" style="text-align: center;border-color: rgb(12, 12, 12);" width="%50">
            JIRA问题单
        </td>
        </tr>
        <tr></tr>
        '''

        str = ''
        for title in titles[:-1]:
            str += '<td rowspan="2" style="border-width: 1px; border-style: inset; border-color: rgb(12, 12, 12); padding: 0px;" width="%17">' + title + '</td>'
        str += '<td rowspan="2" style="border-width: 1px; border-style: inset; border-color: rgb(12, 12, 12); padding: 0px;">' + titles[-1] + '</td>'
        return '<tr class="firstRow">' + str + '</tr><tr></tr>'

    @staticmethod
    def get_table_for_software_handler(handler, vuls):
        '''
        <td style="border-color: rgb(12, 12, 12);">
            handler
        </td>
        <td style="border-color: rgb(12, 12, 12);">
            num
        </td>
        <td style="border-color: rgb(12, 12, 12);">
            <p>
                <a href="http://aaa.com:8080/browse/SEC-393">主机[1.1.1.1] 存在漏洞[75143] Memcached 未授权访问漏洞</a>
            </p>
            <p>
                <a href="http://aaa.com:8080/browse/SEC-393">主机[1.1.1.1] 存在漏洞[75143] Memcached 未授权访问漏洞</a>
            </p>
        </td>
        '''

        str = '<td style="border-width: 1px;border-style: inset;border-color: rgb(12, 12, 12);padding: 0">' + handler + '</td>'
        str += '<td style="border-width: 1px;border-style: inset;border-color: rgb(12, 12, 12);padding: 0">' + '%s' % len(vuls) + '</td>'

        def get_vuls_str():
            vul_str = ''
            for vul in vuls:
                vul_str += '<p><a href="' + JIRA_URL + vul[0] + '">' + vul[1] + '</a></p>'
            vul_str += '<p></p>'
            return vul_str
        str += '<td style="border-width: 1px;border-style: inset;border-color: rgb(12, 12, 12);padding: 0">' + get_vuls_str() + '</td>'
        return str

    def get_table_for_software(self, software_vul_info):
        str = ""
        for software, vul_info in software_vul_info.iteritems():
            handler_num = len(vul_info)
            handlers_sort = [(len(vuls), handler) for handler, vuls in vul_info.iteritems()]
            handlers_sort.sort(reverse=True)
            flag = True
            for handler in handlers_sort:
                handler = handler[1]
                vuls = vul_info[handler]
                if flag:  # 标示software下第一行
                    str += '<tr><td style="border-width: 1px;border-style: inset;border-color: rgb(12, 12, 12);padding: 0" rowspan="%s" colspan="1">' % handler_num + software + '</td>'
                else:
                    str += "<tr>"
                flag = False
                str += self.get_table_for_software_handler(handler, vuls) + "</tr>"
        return str

    def get_table(self, titles, software_vul_info):
        str = self.title_table_name
        str += '<table width="%90" align="center" border="1" align="center" cellpadding="0" cellspacing="0" ><tbody>'
        str += self.get_table_first_line(titles)
        str += self.get_table_for_software(software_vul_info)
        str += '</tbody></table>'
        return str
