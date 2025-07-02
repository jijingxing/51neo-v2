import os
from modules import school_api_lib
from dotenv import load_dotenv

env_file = ".env"


def create_env():
    with open(env_file, "w") as f:
        mac = input("请输入51校园Mac地址: ")

        f.write(f"MCX={mac}\n")


def auth():
    # 优先从系统环境变量中读取 mac
    mac = os.getenv("MAC")

    if mac is None:
        if os.path.exists(env_file):
            load_dotenv(env_file)
            mac = os.getenv("MAC")

    if mac is None:
        print("")
        create_env()
        mac = os.getenv("MAC")  # 再次尝试读取
    school_api_lib.fake_mac_address = mac
