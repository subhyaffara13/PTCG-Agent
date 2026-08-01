
def skipCUDAIfNoCusparseGeneric(fn):
    return skipCUDAIf(not TEST_CUSPARSE_GENERIC, "cuSparse Generic API not available")(
        fn
    )

