
def _use_cuda_memory_pool_manager(
    device: int, mem_pool: tuple[int, int], stream: torch.cuda.Stream
) -> Generator[None, None, None]:
    """
    Context manager to use cuda graph pool for new allocations. If you use this manager
    all cudagraph tensors in use should be reflected in the allocator or they will be overwritten.
    existing_graph should already have been used in a capture, and the mem_pool must already exist,
    because this manager will not preserve a reference to the pool which keeps it alive.
    """
    torch.cuda.synchronize()
    stream.wait_stream(torch.cuda.current_stream())

    with torch.cuda.stream(stream), torch.device(device):
        # Begin allocate to mem pool for all memory allocation on the current thread.
        # This is thread safe since a thread can only warmup or record 1 cudagraph
        # at the same time.
        torch._C._cuda_beginAllocateCurrentThreadToPool(device, mem_pool)
        try:
            yield
        finally:
            torch._C._cuda_endAllocateToPool(device, mem_pool)
            torch._C._cuda_releasePool(device, mem_pool)

    torch.cuda.current_stream().wait_stream(stream)

