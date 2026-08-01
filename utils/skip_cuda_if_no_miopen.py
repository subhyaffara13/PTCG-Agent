
def skipCUDAIfNoMiopen(fn):
    return skipCUDAIf(torch.version.hip is None, "MIOpen is not available")(
        skipCUDAIfNoCudnn(fn)
    )

