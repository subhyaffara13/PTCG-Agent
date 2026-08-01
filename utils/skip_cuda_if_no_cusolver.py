
def skipCUDAIfNoCusolver(fn):
    return skipCUDAIf(
        not has_cusolver() and not has_hipsolver(), "cuSOLVER not available"
    )(fn)

