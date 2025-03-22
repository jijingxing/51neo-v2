import os
import school_api_lib
from dotenv import load_dotenv
env_file = ".env"

def create_env():
    with open(env_file, "w") as f:
        mac = input("请输入51校园Mac地址: ")

        f.write(f"mac={mac}\n")

def auth():
    # 检查 .env 文件是否存在
    if not os.path.exists(env_file):                                       create_env()

    # 加载环境变量
    load_dotenv(env_file)
    school_api_lib.fake_mac_address = os.getenv("mac")
