
def skipCUDAIfNoCusolverROCMIfNoMagma(fn):
    if TEST_WITH_ROCM:
        return skipCUDAIfNoMagma(fn)
    else:
        return skipCUDAIfNoCusolver(fn)

