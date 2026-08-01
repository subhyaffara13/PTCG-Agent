
def maybe_cprofile(func: Callable[_P, _T]) -> Callable[_P, _T]:
    if config.cprofile:
        return cprofile_wrapper(func)
    return func

