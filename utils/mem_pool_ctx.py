
def mem_pool_ctx(mem_pool):
    """A context manager to use a CUDA mem pool. If the mem pool is None, it is a no-op. No type hint because it would
    make torch 2.4 or below crash."""
    if mem_pool is not None:
        with torch.cuda.use_mem_pool(mem_pool):
            yield
    else:
        yield

