
def skipCUDAIfNoSparseGeneric(fn):
    return skipCUDAIf(
        not (TEST_CUSPARSE_GENERIC or TEST_HIPSPARSE_GENERIC),
        "Sparse Generic API not available",
    )(fn)

