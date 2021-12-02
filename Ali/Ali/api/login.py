import sys
import time
import base64
import requests
import pickle

gl_cookies = {}
gl_cookies_path = "cookies"


def save_cookies(requests_cookiejar, filename):
    with open(filename, 'wb+') as f:
        pickle.dump(requests_cookiejar, f)


def load_cookies(filename):
    try:
        with open(filename, 'rb') as f:
            return pickle.load(f)
    except Exception as e:
        return None
        raise
    else:
        pass
    finally:
        pass


def Main_Login(username, passwd):
    request_header = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Origin': 'https://saike.asuscomm.com:8443',
        'Upgrade-Insecure-Requests': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'https://saike.asuscomm.com:8443/Main_Login.asp',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }

    # base64编码的用户名和密码  username:passwd
    login_auth = str(base64.b64encode((username + ':' + passwd).encode('utf-8')), 'utf-8')

    login_post_data = {
        'group_id': '',
        'action_mode': '',
        'action_script': '',
        'action_wait': '5',
        'current_page': 'Main_Login.asp',
        'next_page': 'index.asp',
        'login_authorization': login_auth,
    }

    url_routerlogin = 'https://saike.asuscomm.com:8443/login.cgi'
    deviceLogin = requests.post(url_routerlogin,
                                headers=request_header,  # headers http 头部信息
                                data=login_post_data,
                                # params = {'_':int(time.time())}, #params 参数
                                # cookies = cookies,				  #cookies cookie
                                # allow_redirects = False,		  #allow_redirects 禁用跳转
                                timeout=0.5

                                )
    # print(deviceLogin.text)
    # print(deviceLogin.url)
    # print(deviceLogin.status_code) #状态码
    # print(deviceLogin.headers) #http 头部信息
    # print(deviceLogin.headers.get('Content-Length'))
    # print(deviceLogin.cookies['asus_token']) #cookie
    # httphtml = deviceLogin.text

    # errcode = httphtml
    # print(type(deviceLogin.text))
    httphtml = str(deviceLogin.text)

    if httphtml.find('error_status=') > 0:
        return int(httphtml[httphtml.find('error_status=') + 13])

    # print(deviceLogin.status_code) #状态码
    # print(deviceLogin.headers) #http 头部信息

    global gl_cookies
    if len(deviceLogin.cookies):
        gl_cookies = deviceLogin.cookies
        return 0
    return -1


def get_online_user(l_cookies):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Connection': 'close'
    }

    request_header = {
        # POST /login.cgi HTTP/1.1
        # 'Host': 'router.asus.com',
        # 'Content-Length': 156,
        # 'Cookie': 'traffic_warning_0=2018.2:1',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Origin': 'https://saike.asuscomm.com:8443',
        'Upgrade-Insecure-Requests': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'https://saike.asuscomm.com:8443/Main_Login.asp',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }

    # url_router = 'https://saike.asuscomm.com:8443/Main_Login.asp'
    # url_routerlogin = 'https://saike.asuscomm.com:8443/login.cgi'

    # 获取data

    update_networkmapd = 'https://saike.asuscomm.com:8443/index.asp'
    update_data = requests.get(update_networkmapd,
                               params={'_': int(time.time())},  # params 参数
                               headers=request_header,  # headers http 头部信息
                               cookies=l_cookies,  # cookies cookie
                               timeout=0.9
                               # data    = login_post_data,
                               # allow_redirects = False,		  #allow_redirects 禁用跳转
                               )
    print(update_data.text)
    f = open("index.html", "w", encoding='utf-8')
    f.write(update_data.text)
    f.close()
    # httphtml = str(update_data.text)
    # print(httphtml)
    # if httphtml.find('error_status=') > 0:
    #     return int(httphtml[httphtml.find('error_status=') + 13])

    # userdata = httphtml.split('\'')[1].replace('/>/g', ">").replace('/</g', "<").split('<')
    #
    # for dat in userdata:
    #     print(dat)

    return 0


if __name__ == "__main__":
    need_login = 1
    if (load_cookies(gl_cookies_path)):
        need_login = 0

    while True:
        if need_login:
            username = str(input('帐号:'))
            passwd = str(input('密码:'))
            if Main_Login(username, passwd):
                print("登录失败....")
            else:
                print("登录成功 ok")
                need_login = 0
                save_cookies(gl_cookies, gl_cookies_path)
        if need_login == 0:
            ret = get_online_user(load_cookies(gl_cookies_path))
            if ret == 0:
                break

    sys.exit(0)
