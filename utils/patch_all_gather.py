
def patch_all_gather(new_all_gather_into_tensor: Callable):
    orig_all_gather = dist.all_gather_into_tensor
    dist.barrier()
    dist.all_gather_into_tensor = new_all_gather_into_tensor
    try:
        yield
    finally:
        dist.barrier()
        dist.all_gather_into_tensor = orig_all_gather

