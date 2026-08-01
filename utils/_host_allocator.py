
def _host_allocator():
    _lazy_init()
    return torch._C._cuda_cudaHostAllocator()

