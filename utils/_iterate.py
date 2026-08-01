
def _iterate(iterable: Iterable[T] | AsyncIterable[T]) -> AsyncIterator[T]:
    if isinstance(iterable, AsyncIterator):
        return iterable

    if isinstance(iterable, AsyncIterable):
        return iterable.__aiter__()

    return _IterableAsyncIterator(iter(iterable))

