
def patch_register_post_backward_hook_backward(new_backward: Callable):
    orig_backward = RegisterPostBackwardFunction.backward
    dist.barrier()
    RegisterPostBackwardFunction.backward = new_backward
    try:
        yield
    finally:
        dist.barrier()
        RegisterPostBackwardFunction.backward = orig_backward

