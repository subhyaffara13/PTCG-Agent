
def caching_allocator_disabled():
    r"""Context manager that temporarily disables the CUDA caching allocator."""
    prev = torch._C._cuda_cudaCachingAllocator_is_enabled()
    caching_allocator_enable(False)
    try:
        yield
    finally:
        caching_allocator_enable(prev)

