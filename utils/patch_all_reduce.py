from typing import Callable

def patch_all_reduce(new_all_reduce: Callable):
    orig_all_reduce = dist.all_reduce
    dist.barrier()
    dist.all_reduce = new_all_reduce
    try:
        yield
    finally:
        dist.barrier()
        dist.all_reduce = orig_all_reduce

