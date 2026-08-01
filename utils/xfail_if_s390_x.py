
def xfailIfS390X(func):
    return unittest.expectedFailure(func) if IS_S390X else func

