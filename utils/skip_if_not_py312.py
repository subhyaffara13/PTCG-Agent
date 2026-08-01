
def skipIfNotPy312(fn: Callable[_P, _T]) -> Callable[_P, _T]:
    if sys.version_info >= (3, 12):
        return fn
    return unittest.skip("Requires Python 3.12+")(fn)

