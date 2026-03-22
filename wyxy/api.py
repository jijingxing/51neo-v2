import urllib.request
import urllib.parse
import json
from . import config
import httpx
import warnings

# 获取配置
apiconfig = config.APIConfig.from_env()

# 定义API地址
api_base = "https://iapis.51school.com/"

# 使用伪造的MAC地址以绕过检测
fake_mac_address = ""

# 定义API地址
intfapp_api = f"{api_base}intfapp/"
one_api = f"{api_base}one/"
show_message_api = f"{intfapp_api}showpadmessage.do"
show_user_info_api = f"{intfapp_api}user/showruserinfo.do"
lookup_card_id_by_account_api = f"{intfapp_api}checkcreditnumber.do"

# 构造headers字典
headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "zh-CN,zh;q=0.9",
    "content-type": "application/x-www-form-urlencoded",
    "priority": "u=1, i",
    "sec-ch-ua": '""',
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-platform": '""',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "x-agent-with": "axios",
    "x-requested-with": "XMLHttpRequest",
    "x-user-agent": "appwebkit",
}

# 遗留函数
def call51api_legacy(url, data):
     warnings.warn(
        "call51api_legacy 已弃用，请改用 httpx.post",
        DeprecationWarning,
        stacklevel=2
     )
     with httpx.Client() as client:
        response = client.post(url, data=data,headers=headers)
        return response.json()

def show_message(cardid):
    data = {"mac": fake_mac_address, "CardID": cardid}
    return call51api_legacy(show_message_api, data)


def get_user_info(cardid):  # 通过卡ID检索用户信息
    data = {"mac": fake_mac_address, "cardNo": cardid}
    return call51api_legacy(show_user_info_api, data)


def lookup_card_id_by_account(creditNumber):  # 从账户ID（通讯码）中检索卡ID
    data = {"mac": fake_mac_address, "creditNumber": "@" + str(creditNumber)}
    return call51api_legacy(lookup_card_id_by_account_api, data)["cardNo"]

def get_student_info(id):
    resp = httpx.get(url=f"https://iapis.51school.com/one/yuser/liststudent.do?pageSize=1&r_userType=2&q_cn_id={id}",headers=headers,cookies=apiconfig.cookies)
    return resp.json()
# 使用 __all__ 控制暴露的资源
__all__ = [
    "lookup_card_id_by_account",
    "show_message",
    "get_user_info",
    "get_student_info",
]  # 暴露外部资源
