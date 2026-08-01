
def xfailIfPy312Plus(func):
    return unittest.expectedFailure(func) if sys.version_info >= (3, 12) else func

