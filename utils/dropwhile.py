
def dropwhile(predicate: _Predicate[_T], iterable: Iterable[_T], /) -> Iterator[_T]:
    # dropwhile(lambda x: x < 5, [1, 4, 6, 3, 8]) -> 6 3 8
    if not callable(predicate):
        raise TypeError(f"'{type(predicate).__name__}' object is not callable")

    iterator = iter(iterable)
    for x in iterator:
        if not predicate(x):
            yield x
            break

    yield from iterator

