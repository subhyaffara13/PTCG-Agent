
def pairwise(iterable: Iterable[_T], /) -> Iterator[tuple[_T, _T]]:
    a = None
    first = True
    for b in iterable:
        if first:
            first = False
        else:
            yield a, b  # type: ignore[misc]
        a = b


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


def pairwise(iterable: Iterable[Any]) -> Iterator[tuple[Any, Any]]:
    """
    Return paired elements.

    For example:
        s -> (s0, s1), (s2, s3), (s4, s5), ...
    """
    iterable = iter(iterable)
    return zip_longest(iterable, iterable)


def pairwise(iterable, cyclic=False):
    """Return successive overlapping pairs taken from an input iterable.

    Parameters
    ----------
    iterable : iterable
        An iterable from which to generate pairs.

    cyclic : bool, optional (default=False)
        If `True`, a pair with the last and first items is included at the end.

    Returns
    -------
    iterator
        An iterator over successive overlapping pairs from the `iterable`.

    See Also
    --------
    itertools.pairwise

    Examples
    --------
    >>> list(nx.utils.pairwise([1, 2, 3, 4]))
    [(1, 2), (2, 3), (3, 4)]

    >>> list(nx.utils.pairwise([1, 2, 3, 4], cyclic=True))
    [(1, 2), (2, 3), (3, 4), (4, 1)]
    """
    if not cyclic:
        return itertools.pairwise(iterable)
    a, b = tee(iterable)
    first = next(b, None)
    return zip(a, chain(b, (first,)))


def pairwise(iterable):
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def pairwise(iterable, reverse=False):
    """Iterate over current and next items in iterable.

    Args:
        iterable: An iterable
        reverse: If true, iterate in reverse order.

    Returns:
        A iterable yielding two elements per iteration.

    Example:

        >>> tuple(pairwise([]))
        ()
        >>> tuple(pairwise([], reverse=True))
        ()
        >>> tuple(pairwise([0]))
        ((0, 0),)
        >>> tuple(pairwise([0], reverse=True))
        ((0, 0),)
        >>> tuple(pairwise([0, 1]))
        ((0, 1), (1, 0))
        >>> tuple(pairwise([0, 1], reverse=True))
        ((1, 0), (0, 1))
        >>> tuple(pairwise([0, 1, 2]))
        ((0, 1), (1, 2), (2, 0))
        >>> tuple(pairwise([0, 1, 2], reverse=True))
        ((2, 1), (1, 0), (0, 2))
        >>> tuple(pairwise(['a', 'b', 'c', 'd']))
        (('a', 'b'), ('b', 'c'), ('c', 'd'), ('d', 'a'))
        >>> tuple(pairwise(['a', 'b', 'c', 'd'], reverse=True))
        (('d', 'c'), ('c', 'b'), ('b', 'a'), ('a', 'd'))
    """
    if not iterable:
        return
    if reverse:
        it = reversed(iterable)
    else:
        it = iter(iterable)
    first = next(it, None)
    a = first
    for b in it:
        yield (a, b)
        a = b
    yield (a, first)

