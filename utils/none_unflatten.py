
def none_unflatten(_: None, children: Iterable[_T], /) -> None:
    if len(list(children)) != 0:
        raise ValueError("Expected no children.")
    return None

