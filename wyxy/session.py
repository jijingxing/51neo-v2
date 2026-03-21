import httpx
def get_session(account):
    response = httpx.get(f'https://51ssapi.187372.xyz/api/v2/getSession?acct={account}')
    session = response.json()["data"]["session"]
    return session