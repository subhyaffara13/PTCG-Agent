
def skipCPUIfNoMklSparse(fn):
    return skipCPUIf(
        IS_WINDOWS or not TEST_MKL, "PyTorch is built without MKL support"
    )(fn)

