# 文档地址：https://help.aliyun.com/document_detail/102231.html?spm=a2c4g.11186623.6.543.c6b35aa5nXdBNn
# sdk获取命令：
# pip install aliyun-python-sdk-core                        # 阿里云核心库
# pip install aliyun-python-sdk-alidns==2.6.29              # dns库

import json
from .Log import Log


class Sdk:
    def __init__(self):
        f = open("./api/key.json", encoding='utf-8')
        infile = f.read()
        f.close()
        api = json.loads(infile)
        self.key_id = str(api['key_id'])
        self.secret = str(api['secret'])

    def record(self, msg, met):
        log = Log()
        log.record(msg, met)
