
def takewhile(predicate: _Predicate[_T], iterable: Iterable[_T], /) -> Iterator[_T]:
    # takewhile(lambda x: x<5, [1,4,6,3,8]) → 1 4
    if not callable(predicate):
        raise TypeError(f"'{type(predicate).__name__}' object is not callable")

    for x in iterable:
        if not predicate(x):
            break
        yield x

