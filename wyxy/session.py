import httpx
from . import config
import httpx
import warnings

# 获取配置
apiconfig = config.APIConfig.get_instance()

def get_session(account):
    response = httpx.get(f'https://51ssapi.187372.xyz/api/v2/getSession?acct={account}')
    session = response.json()["data"]["session"]
    return session
def auth(account):
    session = get_session(account)
    apiconfig.cookies = {"geli-session": session}