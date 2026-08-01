
def skipCUDANonDefaultStreamIf(condition):
    def dec(fn):
        if getattr(fn, '_do_cuda_non_default_stream', True):  # if current True
            fn._do_cuda_non_default_stream = not condition
        return fn
    return dec

