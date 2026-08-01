
def xfailIfPy312(fn: Callable[_P, _T]) -> Callable[_P, _T]:
    if sys.version_info >= (3, 12):
        return unittest.expectedFailure(fn)
    return fn

