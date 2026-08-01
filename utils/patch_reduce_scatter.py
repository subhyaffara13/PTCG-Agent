
def patch_reduce_scatter(new_reduce_scatter_tensor: Callable):
    orig_reduce_scatter = dist.reduce_scatter_tensor
    dist.barrier()
    dist.reduce_scatter_tensor = new_reduce_scatter_tensor
    try:
        yield
    finally:
        dist.barrier()
        dist.reduce_scatter_tensor = orig_reduce_scatter

