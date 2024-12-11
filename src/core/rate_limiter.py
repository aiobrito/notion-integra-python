# src/core/rate_limiter.py
from functools import wraps
from time import time
from typing import Callable

def rate_limit(calls: int, period: int):
    def decorator(func: Callable):
        timestamps = []
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time()
            timestamps[:] = [t for t in timestamps if now - t < period]
            
            if len(timestamps) >= calls:
                raise Exception(f"Rate limit: {calls} chamadas/{period}s")
                
            timestamps.append(now)
            return func(*args, **kwargs)
        return wrapper
    return decorator