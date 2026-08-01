
def xfailIfROCm(func):
    return unittest.expectedFailure(func) if torch.version.hip is not None else func

