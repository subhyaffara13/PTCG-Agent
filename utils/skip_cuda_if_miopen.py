
def skipCUDAIfMiopen(fn):
    return skipCUDAIf(torch.version.hip is not None, "Marked as skipped for MIOpen")(fn)

