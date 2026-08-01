
def skipCUDAMemoryLeakCheckIf(condition):
    def dec(fn):
        if getattr(fn, '_do_cuda_memory_leak_check', True):  # if current True
            fn._do_cuda_memory_leak_check = not condition
        return fn
    return dec

