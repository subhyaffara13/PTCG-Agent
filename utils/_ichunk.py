
def _ichunk(iterator, n):
    cache = deque()
    chunk = islice(iterator, n)

    def generator():
        with suppress(StopIteration):
            while True:
                if cache:
                    yield cache.popleft()
                else:
                    yield next(chunk)

    def materialize_next(n=1):
        # if n not specified materialize everything
        if n is None:
            cache.extend(chunk)
            return len(cache)

        to_cache = n - len(cache)

        # materialize up to n
        if to_cache > 0:
            cache.extend(islice(chunk, to_cache))

        # return number materialized up to n
        return min(n, len(cache))

    return (generator(), materialize_next)

