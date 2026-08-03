from typing import Callable

def patch_post_backward(new_post_backward: Callable):
    orig_post_backward = FSDPParamGroup.post_backward
    dist.barrier()
    FSDPParamGroup.post_backward = new_post_backward
    try:
        yield
    finally:
        dist.barrier()
        FSDPParamGroup.post_backward = orig_post_backward

