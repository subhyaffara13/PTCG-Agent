
def skipCUDAIfNoHipsparseGeneric(fn):
    return skipCUDAIf(
        not TEST_HIPSPARSE_GENERIC, "hipSparse Generic API not available"
    )(fn)

