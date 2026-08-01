
def skipCPUIfNoMkldnn(fn):
    return skipCPUIf(
        not torch.backends.mkldnn.is_available(),
        "PyTorch is built without mkldnn support",
    )(fn)

