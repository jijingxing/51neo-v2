import argparse
from libs import auth,school_api_lib,get_db

auth.auth()

#设置起始通讯码
index_uin = "2000000"

def make_cache(start_uin: str = None, count: int = 100):
    # 如果没有指定起始通讯码，使用默认值
    current_uin = start_uin if start_uin else index_uin
    
    # 使用数据库会话批量插入任务
    with get_db.database_session() as cursor:
        for i in range(count):
            try:
                # 获取用户信息
                card_id = school_api_lib.lookup_card_id_by_account(current_uin)
                user_info = school_api_lib.get_user_info(card_id)
                
                # 将用户信息转换为任务数据并存储
                task_data = f"用户信息 - 通讯码: {current_uin}, 姓名: {user_info['name']}, 班级: {user_info['classes']}"
                cursor.execute(
                    "INSERT INTO user_info_cache (uin, name, class_name, task_data) VALUES (?, ?, ?, ?)",
                    (current_uin, user_info['name'], user_info['classes'], task_data)
                )
                print(f"Added task for user: {user_info['name']} (通讯码: {current_uin})")
                
                # 递增通讯码
                current_uin = str(int(current_uin) + 1)
            except Exception as e:
                print(f"Error processing 通讯码 {current_uin}: {str(e)}")
                current_uin = str(int(current_uin) + 1)
                continue

if __name__ == "__main__":
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description='生成用户信息缓存')
    parser.add_argument('--start', type=str, default=index_uin,
                        help='起始通讯码 (默认: 2000000)')
    parser.add_argument('--count', type=int, default=100,
                        help='要缓存的用户数量 (默认: 100)')
    
    # 解析命令行参数
    args = parser.parse_args()
    
    # 使用命令行参数调用make_cache函数
    make_cache(start_uin=args.start, count=args.count)