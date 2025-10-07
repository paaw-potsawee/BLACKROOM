import psutil
import os
from time import time


def process_memory():
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.rss


# decorator function allow program to calculate space and time used
def profile(func):
    def wrapper(*args, **kwargs):

        mem_before = process_memory()
        start_time = time()
        result = func(*args, **kwargs)
        mem_after = process_memory()
        print("{}:consumed memory: {:,}".format(
            func.__name__,
            mem_before, mem_after, mem_after - mem_before))
        print(f"{func.__name__}:{(time() - start_time) * 1000} ms")

        return result
    return wrapper
