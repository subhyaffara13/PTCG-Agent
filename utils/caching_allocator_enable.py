
def caching_allocator_enable(value: bool = True) -> None:
    r"""Enable or disable the CUDA memory allocator. On by default."""
    if is_initialized():
        torch._C._cuda_cudaCachingAllocator_enable(value)

