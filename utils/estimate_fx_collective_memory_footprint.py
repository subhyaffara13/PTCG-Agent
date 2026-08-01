
def estimate_fx_collective_memory_footprint(fx_node: torch.fx.Node) -> int:
    """Estimate the memory footprint of a collective operation in bytes.

    This returns the total bytes that need to be live concurrently in memory.
    For all_reduce, we divide by 2 since it can be done in-place.
    """
    from torch._inductor.fx_passes.bucketing import (
        is_all_reduce_tensor as is_all_reduce,
    )

    size = estimate_fx_collective_size(fx_node)
    return size if not is_all_reduce(fx_node) else size // 2

