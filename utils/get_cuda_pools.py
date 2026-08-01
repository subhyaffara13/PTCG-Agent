
def get_cuda_pools():  # no type hint because it would make torch 2.4 crash
    """Returns a tuple of (mem_pool, graph_pool_id) for CUDA graphs. Since the MemPool object is only available in torch
    2.5+, we only return a graph_pool_id for older versions."""
    if is_torch_greater_or_equal("2.5.0"):
        mem_pool = torch.cuda.MemPool()
        graph_pool_id = mem_pool.id
        return mem_pool, graph_pool_id
    else:
        mem_pool = None
        graph_pool_id = torch.cuda.graph_pool_handle()
        return mem_pool, graph_pool_id

