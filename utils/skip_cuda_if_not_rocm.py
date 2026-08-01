
def skipCUDAIfNotRocm(fn):
    return skipCUDAIf(
        not TEST_WITH_ROCM, "test doesn't currently work on the CUDA stack"
    )(fn)

