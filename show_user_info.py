from school_api_lib import (
    get_user_info,
    lookup_card_id_by_account,
)  # 导入51校园API 逆向 BY:景
import auth

auth.auth()  # 完成认证
user_info = get_user_info(  # 通过卡ID获取用户信息
    lookup_card_id_by_account(input("请输入通讯密码："))  # 从账户ID（通讯码）中检索卡ID
)

print(user_info)

# 输出获取到的信息
print(
    "================================================================================"
)
print("姓名：", user_info["name"])
print("年级：", user_info["yearClass"])
print("班级：", user_info["classes"])
print("内外宿：", user_info["tacticsType"])
print("考勤分组：", user_info["board"])
print("账户ID（通讯码）：", user_info["id"])
print("大头链接：", "https://iapis.51school.com" + user_info["picUrl"])
print(
    "================================================================================"
)
