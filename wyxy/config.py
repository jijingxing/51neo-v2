# config.py
import os
from dataclasses import dataclass

@dataclass
class APIConfig:
    api_base: str = "https://iapis.51school.com/"
    cookies: str = ""
    timeout: int = 30
    
    @classmethod
    def from_env(cls):
        return cls(
            api_base=os.getenv("API_BASE", "https://iapis.51school.com/"),
            cookies=os.getenv("API_COOKIES", ""),
            timeout=int(os.getenv("API_TIMEOUT", "30"))
        )
