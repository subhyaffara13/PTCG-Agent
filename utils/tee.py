
def tee(
    iterable: Iterable[T] | AsyncIterable[T], n: int = 2
) -> tuple[AsyncIterator[T], ...]:
    n = operator.index(cast(Any, n))
    if n < 0:
        raise ValueError("n must be >= 0")
    if n == 0:
        return ()

    iterator = _TeeAsyncIterator(iterable)
    iterators: list[AsyncIterator[T]] = [iterator]
    iterators.extend(_TeeAsyncIterator(iterator) for _ in range(n - 1))
    return tuple(iterators)


def tee(iterable: Iterable[_T], n: int = 2, /) -> tuple[Iterator[_T], ...]:
    iterator = iter(iterable)
    shared_link = [None, None]

    def _tee(link) -> Iterator[_T]:  # type: ignore[no-untyped-def]
        try:
            while True:
                if link[1] is None:
                    link[0] = next(iterator)
                    link[1] = [None, None]
                value, link = link
                yield value
        except StopIteration:
            return

    return tuple(_tee(shared_link) for _ in range(n))

