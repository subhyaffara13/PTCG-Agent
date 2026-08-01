
def without_output_descs(f: Callable[_P, tuple[_T, _S]]) -> Callable[_P, _T]:
    @wraps(f)
    @simple_wraps(f)
    def inner(*args: _P.args, **kwargs: _P.kwargs) -> _T:
        return f(*args, **kwargs)[0]

    return inner

