# get_db.py
import sqlite3
import threading
from contextlib import contextmanager
from typing import Generator

# 集中配置数据库名称
DATABASE_NAME = "application.db"

# 线程局部存储确保连接隔离
_thread_local = threading.local()

def _get_connection() -> sqlite3.Connection:
    """获取线程独立的数据库连接（内部方法）"""
    if not hasattr(_thread_local, "conn"):
        # 创建新连接并应用优化设置
        _thread_local.conn = sqlite3.connect(
            DATABASE_NAME,
            check_same_thread=False,
            timeout=15,  # 延长超时时间
            isolation_level=None  # 自动提交模式
        )
        # 性能优化设置
        _thread_local.conn.execute("PRAGMA journal_mode = WAL")
        _thread_local.conn.execute("PRAGMA busy_timeout = 5000")
        _thread_local.conn.execute("PRAGMA synchronous = NORMAL")
    return _thread_local.conn

@contextmanager
def database_session() -> Generator[sqlite3.Cursor, None, None]:
    """
    线程安全的数据库会话上下文管理器
    使用示例：
    with database_session() as cursor:
        cursor.execute("INSERT ...")
    """
    conn = _get_connection()
    cursor = conn.cursor()
    try:
        yield cursor
        conn.commit()  # 成功时提交事务
    except sqlite3.Error as e:
        conn.rollback()  # 失败时回滚事务
        raise RuntimeError(f"Database error: {str(e)}") from e
    finally:
        cursor.close()

# 多线程安全访问示例
if __name__ == "__main__":
    # 初始化表结构（仅需运行一次）
    with database_session() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS task_queue (
                id INTEGER PRIMARY KEY,
                task_data TEXT NOT NULL,
                status TEXT DEFAULT 'pending'
            )
        """)
    
    # 定义多线程写入任务
    def worker_thread(thread_id: int):
        with database_session() as cursor:
            for i in range(3):
                cursor.execute(
                    "INSERT INTO task_queue (task_data) VALUES (?)",
                    (f"Thread-{thread_id} task-{i}",)
                )
            print(f"Thread {thread_id} inserted 3 tasks")

    # 启动5个工作线程
    threads = []
    for i in range(5):
        t = threading.Thread(target=worker_thread, args=(i,))
        threads.append(t)
        t.start()

    # 等待所有线程完成
    for t in threads:
        t.join()

    # 验证结果
    with database_session() as cursor:
        cursor.execute("SELECT COUNT(*) FROM task_queue")
        total = cursor.fetchone()[0]
        print(f"Total tasks in database: {total}")

