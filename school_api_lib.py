import urllib.request
import urllib.parse
import json

#定义API地址
api_base = "https://iapis.51school.com/"

#使用伪造的MAC地址以绕过检测
fake_mac_address = ""

#设置Cookies来进行登录
cookies = "geli-yuser-cardno=e32a96592fcefea39e15843f85f5572f1859aa20f072129594a3a4c144b7fab5ead4c00e7486fcd6;geli-session=7a6307b91acbc6855de60bd878f1a239;geli-yschool=eb9bf44e373fe980;geli-yuser=1191411"

#定义API地址
api_intfapp = f"{api_base}intfapp/"
show_message_api = f"{api_intfapp}showpadmessage.do"
show_user_info_api = f"{api_intfapp}user/showruserinfo.do"
lookup_card_id_by_account_api = f"{api_intfapp}checkcreditnumber.do"

# 构造headers字典
headers = {
    "Cookie": cookies,
    "accept": "application/json, text/plain, */*",
    "accept-language": "zh-CN,zh;q=0.9",
    "content-type": "application/x-www-form-urlencoded",
    "priority": "u=1, i",
    "sec-ch-ua": "\"\"",
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-platform": "\"\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "x-agent-with": "axios",
    "x-requested-with": "XMLHttpRequest",
    "x-user-agent": "appwebkit"
}

def call51api(url, data):  # 修改为接收data参数
    # 将data编码成URL编码格式，并转换为字节类型
    data = urllib.parse.urlencode(data).encode()

    # 创建请求对象
    req = urllib.request.Request(url, data=data, headers=headers, method='POST')

    # 发送请求并获取响应
    with urllib.request.urlopen(req) as response:
        response_data = response.read()  # 获取响应内容
        return json.loads(response_data.decode('utf-8'))  # 假设返回的内容是JSON格式

def show_message(cardid):
    data = {
        'mac': fake_mac_address,
        'CardID': cardid
    }
    return call51api(show_message_api, data)

def get_user_info(cardid):  # 通过卡ID检索用户信息
    data = {
        "mac": fake_mac_address,
        "cardNo": cardid
    }
    return call51api(show_user_info_api, data)

def lookup_card_id_by_account(creditNumber):  # 从账户ID（通讯码）中检索卡ID
    data = {
        "mac": fake_mac_address,
        "creditNumber": "@" + str(creditNumber)
    }
    return call51api(lookup_card_id_by_account_api, data)['cardNo']

# 使用 __all__ 控制暴露的资源
__all__ = ["lookup_card_id_by_account", "show_message", "get_user_info",fake_mac_address]  # 暴露外部资源
