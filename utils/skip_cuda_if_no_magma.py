
def skipCUDAIfNoMagma(fn):
    return skipCUDAIf("no_magma", "no MAGMA library detected")(
        skipCUDANonDefaultStreamIf(True)(fn)
    )

