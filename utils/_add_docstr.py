
def _add_docstr(*args: str) -> Callable[[_T], _T]:
    r"""Adds docstrings to a given decorated function.

    Specially useful when then docstrings needs string interpolation, e.g., with
    str.format().
    REMARK: Do not use this function if the docstring doesn't need string
    interpolation, just write a conventional docstring.

    Args:
        args (str):
    """

    def decorator(o: _T) -> _T:
        o.__doc__ = "".join(args)
        return o

    return decorator

