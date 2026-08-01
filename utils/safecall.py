
def safecall(func: t.Callable[P, R]) -> t.Callable[P, R | None]:
    """Wraps a function so that it swallows exceptions."""

    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R | None:
        try:
            return func(*args, **kwargs)
        except Exception:
            pass
        return None

    return update_wrapper(wrapper, func)


def safecall(f, name, *args, **kwargs):
    """Call a LAPACK routine, determining lwork automatically and handling
    error return values"""
    lwork = kwargs.get("lwork", None)
    if lwork in (None, -1):
        kwargs['lwork'] = -1
        ret = f(*args, **kwargs)
        kwargs['lwork'] = ret[-2][0].real.astype(np.int_)
    ret = f(*args, **kwargs)
    if ret[-1] < 0:
        raise ValueError(f"illegal value in {-ret[-1]}th argument of internal {name}")
    return ret[:-2]

