import psutil
import os
from time import time
from functools import wraps
from typing import Callable, Optional


def process_memory():
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.rss


def _human_bytes(n: int) -> str:
    units = ["B", "KB", "MB", "GB", "TB", "PB", "EB"]
    v = float(abs(n))
    i = 0
    while v >= 1024.0 and i < len(units) - 1:
        v /= 1024.0
        i += 1
    return f"{v:.2f} {units[i]}"


def _fmt_bytes(n: int) -> str:
    # 12,345 B (12.06 KB)
    return f"{n:,} B ({_human_bytes(n)})"


def _fmt_diff(n: int) -> str:
    # +4,096 B (+4.00 KB) or -4,096 B (-4.00 KB)
    sign = "+" if n >= 0 else "-"
    a = abs(n)
    return f"{sign}{a:,} B ({sign}{_human_bytes(a)})"


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

        if os.getenv('ENV') == 'test':
            return result

        if callback:
            try:
                callback(func.__name, mem_before, mem_after, mem_diff,
                         elapsed_ms, result, args, kwargs)
            except:
                pass
        else:
            print(
                f"{used_msg}: memory {_fmt_bytes(mem_after)}, diff {_fmt_diff(mem_diff)}")
            print(f"{used_msg}: {elapsed_ms:.2f} ms")

        return result
    return wrapper
