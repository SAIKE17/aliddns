# 调用示例
# from api.Mail import Mail
#
# mail_tmp = Mail()
# msg = {
#     "title": "标题",
#     "content": "内容",
#     "sender_name": "发送人",
#     "receiver_name": "接收人"
# }
# print(mail_tmp.send_mail('test@qq.com', msg))
import json
import smtplib
from email.mime.text import MIMEText
from email.header import Header


class Mail:
    """发送邮件

    1、SMTP邮件发送

    Args:
        sender: 发送邮箱账号
        smtp： 邮箱服务器

    Returns:
        是否成功
    """

    def __init__(self):
        f = open("./api/key.json", encoding='utf-8')
        infile = f.read()
        f.close()
        api = json.loads(infile)
        self.sender = str(api['mail_sender'])
        smtp_code = str(api['smtp_code'])
        # 配置服务器
        self.smtp_obj = smtplib.SMTP_SSL('smtp.qq.com', 465)
        self.smtp_obj.login(self.sender, smtp_code)  # 邮件发送账号， 授权码（不是qq密码，是邮箱中的配置的授权码）

    def send_mail(self, receivers, msg):
        receivers = receivers  # 接收邮件账号
        # 组装发送内容
        message = MIMEText(msg['content'], 'plain', 'utf-8')  # 发送的内容
        message['From'] = Header(msg['sender_name'], 'utf-8')  # 发件人名称
        message['To'] = Header(msg['receiver_name'], 'utf-8')  # 收件人名称
        message['Subject'] = Header(msg['title'], 'utf-8')  # 邮件标题

        try:
            self.smtp_obj.sendmail(self.sender, receivers, message.as_string())
        except Exception as e:
            return '邮件发送失败--' + str(e)
        return '邮件发送成功'
