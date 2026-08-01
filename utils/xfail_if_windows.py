
def xfailIfWindows(func):
    return unittest.expectedFailure(func) if IS_WINDOWS else func

