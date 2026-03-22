# config.py
from dataclasses import dataclass, field
from typing import Dict, Union
import os

@dataclass
class APIConfig:
    api_base: str = "https://iapis.51school.com/"
    cookies: Dict[str, str] = field(default_factory=dict)  # 改为字典
    timeout: int = 30
    
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, api_base=None, cookies=None, timeout=None):
        # 只在第一次初始化时设置值
        if not hasattr(self, '_initialized'):
            if api_base is not None:
                self.api_base = api_base
            if cookies is not None:
                self.cookies = cookies
            if timeout is not None:
                self.timeout = timeout
            self._initialized = True
    
    @classmethod
    def from_env(cls):
        """从环境变量创建或更新配置实例"""
        instance = cls()
        instance.api_base = os.getenv("API_BASE", "https://iapis.51school.com/")
        instance.cookies = os.getenv("API_COOKIES", "")
        instance.timeout = int(os.getenv("API_TIMEOUT", "30"))
        return instance
    
    @classmethod
    def get_instance(cls):
        """获取单例实例"""
        if cls._instance is None:
            cls.from_env()
        return cls._instance
    
    def reset(self):
        """重置配置为默认值"""
        self.api_base = "https://iapis.51school.com/"
        self.cookies = ""
        self.timeout = 30