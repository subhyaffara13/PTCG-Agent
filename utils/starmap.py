
def starmap(
    function: Callable[[], _U],
    iterable: Iterable[tuple[()]],
    /,
) -> itertools.starmap[_U]: ...


def starmap(
    function: Callable[[_T], _U],
    iterable: Iterable[tuple[_T]],
    /,
) -> itertools.starmap[_U]: ...


def starmap(
    function: Callable[[_T, _T1], _U],
    iterable: Iterable[tuple[_T, _T1]],
    /,
) -> itertools.starmap[_U]: ...


def starmap(
    function: Callable[[_T, _T1, _T2], _U],
    iterable: Iterable[tuple[_T, _T1, _T2]],
    /,
) -> itertools.starmap[_U]: ...


def starmap(function: Callable[..., _T], iterable: Iterable, /) -> Iterable[_T]:
    # starmap(pow, [(2,5), (3,2), (10,3)]) → 32 9 1000
    if not callable(function):
        raise TypeError(f"'{type(function).__name__}' object is not callable")

    for args in iterable:
        yield function(*args)

