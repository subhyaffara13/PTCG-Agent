
def zip_longest(
    iter1: Iterable[_T1],
    /,
    *,
    fillvalue: _U = ...,
) -> Iterator[tuple[_T1]]: ...


def zip_longest(
    iter1: Iterable[_T1],
    iter2: Iterable[_T2],
    /,
) -> Iterator[tuple[_T1 | None, _T2 | None]]: ...


def zip_longest(
    iter1: Iterable[_T1],
    iter2: Iterable[_T2],
    /,
    *,
    fillvalue: _U = ...,
) -> Iterator[tuple[_T1 | _U, _T2 | _U]]: ...


def zip_longest(
    iter1: Iterable[_T],
    iter2: Iterable[_T],
    iter3: Iterable[_T],
    /,
    *iterables: Iterable[_T],
) -> Iterator[tuple[_T | None, ...]]: ...


def zip_longest(
    iter1: Iterable[_T],
    iter2: Iterable[_T],
    iter3: Iterable[_T],
    /,
    *iterables: Iterable[_T],
    fillvalue: _U = ...,
) -> Iterator[tuple[_T | _U, ...]]: ...


def zip_longest(
    *iterables: Iterable[_T],
    fillvalue: _U = None,  # type: ignore[assignment]
) -> Iterator[tuple[_T | _U, ...]]:
    # zip_longest('ABCD', 'xy', fillvalue='-') -> Ax By C- D-

    iterators = list(map(iter, iterables))
    num_active = len(iterators)
    if not num_active:
        return

    while True:
        values = []
        for i, iterator in enumerate(iterators):
            try:
                value = next(iterator)
            except StopIteration:
                num_active -= 1
                if not num_active:
                    return
                iterators[i] = itertools.repeat(fillvalue)  # type: ignore[arg-type]
                value = fillvalue  # type: ignore[assignment]
            values.append(value)
        yield tuple(values)

