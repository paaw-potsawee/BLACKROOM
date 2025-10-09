import psutil
import os
from time import time
from functools import wraps
from typing import Callable, Optional


def process_memory():
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.rss


# decorator function allow program to calculate space and time used
def profile(func, *, callback: Optional[Callable] = None, message: Optional[str] = None):

    @wraps(func)
    def wrapper(*args, **kwargs):
        runtime_msg = kwargs.pop('profile_msg', None)
        used_msg = runtime_msg or message or func.__name__

        mem_before = process_memory()
        start_time = time()
        result = func(*args, **kwargs)
        mem_after = process_memory()
        elapsed_ms = (time() - start_time) * 1000
        mem_diff = mem_after - mem_before

        if callback:
            try:
                callback(func.__name, mem_before, mem_after, mem_diff,
                         elapsed_ms, result, args, kwargs)
            except:
                pass
        else:
            print(
                f"{used_msg}: memory {mem_after/1024**2:.2f} MB (diff {mem_diff/1024**2:.2f} MB)")
            print(f"{used_msg}:{elapsed_ms} ms")

        return result
    return wrapper
