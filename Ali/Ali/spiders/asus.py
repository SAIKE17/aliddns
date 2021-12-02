import scrapy
import base64
import json
import re
from ..api.Domain import Domain


class AsusSpider(scrapy.Spider):
    """爬取路由器ip地址

    1、登录路由器
    2、获取路由器ip地址
    3、获取阿里云解析ip地址
    4、ip地址进行对比，不相同则跟新阿里云解析

    Args:
        name(str): ”“
        domains_pre(int) : ”“
        start_urls(srt): ”“

    Returns:
        None
    """

    name = 'asus'
    # allowed_domains = ['saike.asuscomm.com']
    domains_pre = 'https://saike.asuscomm.com:8443'
    start_urls = [domains_pre + '/Main_Login.asp']

    def __init__(self):
        f = open("./api/key.json", encoding='utf-8')
        infile = f.read()
        f.close()
        api = json.loads(infile)
        self.username = str(api['username'])
        self.passwd = str(api['passwd'])

    def parse(self, response):
        # base64编码的用户名和密码  username:passwd
        login_auth = str(base64.b64encode((self.username + ':' + self.passwd).encode('utf-8')), 'utf-8')
        login_post_data = {
            'group_id': '',
            'action_mode': '',
            'action_script': '',
            'action_wait': '5',
            'current_page': 'Main_Login.asp',
            'next_page': 'index.asp',
            'login_authorization': login_auth,
        }
        yield scrapy.FormRequest.from_response(
            response,
            formdata=login_post_data,
            callback=self.parse_item
        )

    def parse_item(self, response):
        # 获取路由器ip地址
        win_ip = re.findall(r"first_wanlink_ipaddr\(\) \{ return \'(.+?)\';\}", response.body.decode())[0]
        print(win_ip)
        # 获取阿里云解析地址
        domain = Domain()
        record_tmp = domain.get_describe_domain_records_request({"domain_name": "saike.ltd"})
        record_tmp = str(record_tmp, encoding="utf-8")
        record_tmp = json.loads(record_tmp)
        for item in record_tmp['DomainRecords']['Record']:
            record_ip = item['Value']
            record_rr = item['RR']
            record_record_id = item['RecordId']
            record_type = item['Type']
            print(record_ip, record_rr, record_record_id, record_type)
            if win_ip != record_ip:
                print(record_ip)
                recode_data = {
                    "rr": record_rr,
                    "record_id": record_record_id,
                    "type": record_type,
                    "ip": win_ip,
                }
                domain.update_domain_record_request(recode_data)
