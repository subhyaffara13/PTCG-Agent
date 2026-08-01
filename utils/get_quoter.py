
def get_quoter(encode: bool = True) -> Callable[[AnyStr], str]: ...


def get_quoter(encode: None) -> Callable[[str], str]: ...


def get_quoter(encode: bool | None = True) -> Callable[[AnyStr], str] | Callable[[str], str]:
    """
    Return quoting callable given an `encode` tri-boolean (True, False or None)
    """
    if encode is True:
        return quote
    elif encode is False:
        return unquote
    elif encode is None:
        return lambda x: x

