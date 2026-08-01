
def accumulate(binop, seq, initial=no_default):
    """ Repeatedly apply binary function to a sequence, accumulating results

    >>> from operator import add, mul
    >>> list(accumulate(add, [1, 2, 3, 4, 5]))
    [1, 3, 6, 10, 15]
    >>> list(accumulate(mul, [1, 2, 3, 4, 5]))
    [1, 2, 6, 24, 120]

    Accumulate is similar to ``reduce`` and is good for making functions like
    cumulative sum:

    >>> from functools import partial, reduce
    >>> sum    = partial(reduce, add)
    >>> cumsum = partial(accumulate, add)

    Accumulate also takes an optional argument that will be used as the first
    value. This is similar to reduce.

    >>> list(accumulate(add, [1, 2, 3], -1))
    [-1, 0, 2, 5]
    >>> list(accumulate(add, [], 1))
    [1]

    See Also:
        itertools.accumulate :  In standard itertools for Python 3.2+
    """
    seq = iter(seq)
    if initial == no_default:
        try:
            result = next(seq)
        except StopIteration:
            return
    else:
        result = initial
    yield result
    for elem in seq:
        result = binop(result, elem)
        yield result


def accumulate(
    iterable: Iterable[_T],
    func: Callable[[_T, _T], _T] | None = None,
    *,
    initial: _T | None = None,
) -> Iterator[_T]:
    # call iter outside of the generator to match cypthon behavior
    iterator = iter(iterable)
    if func is None:
        func = operator.add

    def _accumulate(iterator: Iterator[_T]) -> Iterator[_T]:
        total = initial
        if total is None:
            try:
                total = next(iterator)
            except StopIteration:
                return

        yield total
        for element in iterator:
            total = func(total, element)
            yield total

    return _accumulate(iterator)

