import functools
import time
from typing import Callable, Any

class ResilientClientError(Exception):
    pass

class MaxRetriesExceededError(ResilientClientError):
    def __init__(self, message: str, attempts: int):
        super().__init__(message)
        self.attempts = attempts

def log_execution(func: Callable[..., Any]) -> Callable[..., Any]:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        print(f"🚀 Executing {func.__name__} with args: {args} and kwargs: {kwargs}")
        try:
            result = func(*args, **kwargs)
            print(f"✅ {func.__name__} returned: {result}")
            return result
        except Exception as e:
            print(f"❌ Error in {func.__name__}: {e}")
            raise
    return wrapper

def retry(max_attempts: int, delay: float, exceptions: tuple):
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            attempt = 0
            current_delay = delay
            last_exception = None
            while attempt < max_attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:   
                    last_exception = e                 
                    attempt += 1
                    print(f"⚠️ Transient error: {e}. Retrying in {current_delay}s ({attempt}/{max_attempts})")
                    current_delay *= 2
                    time.sleep(current_delay)
            raise MaxRetriesExceededError(f"Max retries exceeded for {func.__name__}", max_attempts) from last_exception
        return wrapper
    return decorator