
def simple_wraps(
    f: Callable[_P, _R],
) -> Callable[[Callable[_P2, _R2]], Callable[_P2, _R2]]:
    # NB: omit ('__module__', '__name__', '__qualname__') for ease of
    # debugging
    return wraps(f, assigned=("__doc__", "__annotations__", "__type_params__"))

