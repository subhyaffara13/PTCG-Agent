
def ordered(request):
    """
    Boolean 'ordered' parameter for Categorical.
    """
    return request.param


def ordered(seq, keys=None, default=True, warn=False):
    """Return an iterator of the seq where keys are used to break ties
    in a conservative fashion: if, after applying a key, there are no
    ties then no other keys will be computed.

    Two default keys will be applied if 1) keys are not provided or
    2) the given keys do not resolve all ties (but only if ``default``
    is True). The two keys are ``_nodes`` (which places smaller
    expressions before large) and ``default_sort_key`` which (if the
    ``sort_key`` for an object is defined properly) should resolve
    any ties. This strategy is similar to sorting done by
    ``Basic.compare``, but differs in that ``ordered`` never makes a
    decision based on an objects name.

    If ``warn`` is True then an error will be raised if there were no
    keys remaining to break ties. This can be used if it was expected that
    there should be no ties between items that are not identical.

    Examples
    ========

    >>> from sympy import ordered, count_ops
    >>> from sympy.abc import x, y

    The count_ops is not sufficient to break ties in this list and the first
    two items appear in their original order (i.e. the sorting is stable):

    >>> list(ordered([y + 2, x + 2, x**2 + y + 3],
    ...    count_ops, default=False, warn=False))
    ...
    [y + 2, x + 2, x**2 + y + 3]

    The default_sort_key allows the tie to be broken:

    >>> list(ordered([y + 2, x + 2, x**2 + y + 3]))
    ...
    [x + 2, y + 2, x**2 + y + 3]

    Here, sequences are sorted by length, then sum:

    >>> seq, keys = [[[1, 2, 1], [0, 3, 1], [1, 1, 3], [2], [1]], [
    ...    lambda x: len(x),
    ...    lambda x: sum(x)]]
    ...
    >>> list(ordered(seq, keys, default=False, warn=False))
    [[1], [2], [1, 2, 1], [0, 3, 1], [1, 1, 3]]

    If ``warn`` is True, an error will be raised if there were not
    enough keys to break ties:

    >>> list(ordered(seq, keys, default=False, warn=True))
    Traceback (most recent call last):
    ...
    ValueError: not enough keys to break ties


    Notes
    =====

    The decorated sort is one of the fastest ways to sort a sequence for
    which special item comparison is desired: the sequence is decorated,
    sorted on the basis of the decoration (e.g. making all letters lower
    case) and then undecorated. If one wants to break ties for items that
    have the same decorated value, a second key can be used. But if the
    second key is expensive to compute then it is inefficient to decorate
    all items with both keys: only those items having identical first key
    values need to be decorated. This function applies keys successively
    only when needed to break ties. By yielding an iterator, use of the
    tie-breaker is delayed as long as possible.

    This function is best used in cases when use of the first key is
    expected to be a good hashing function; if there are no unique hashes
    from application of a key, then that key should not have been used. The
    exception, however, is that even if there are many collisions, if the
    first group is small and one does not need to process all items in the
    list then time will not be wasted sorting what one was not interested
    in. For example, if one were looking for the minimum in a list and
    there were several criteria used to define the sort order, then this
    function would be good at returning that quickly if the first group
    of candidates is small relative to the number of items being processed.

    """

    d = defaultdict(list)
    if keys:
        if isinstance(keys, (list, tuple)):
            keys = list(keys)
            f = keys.pop(0)
        else:
            f = keys
            keys = []
        for a in seq:
            d[f(a)].append(a)
    else:
        if not default:
            raise ValueError('if default=False then keys must be provided')
        d[None].extend(seq)

    for k, value in sorted(d.items()):
        if len(value) > 1:
            if keys:
                value = ordered(value, keys, default, warn)
            elif default:
                value = ordered(value, (_nodes, default_sort_key,),
                               default=False, warn=warn)
            elif warn:
                u = list(uniq(value))
                if len(u) > 1:
                    raise ValueError(
                        'not enough keys to break ties: %s' % u)
        yield from value


def ordered(*args, **kwargs):
    from sympy import ordered as _ordered
    return _ordered(*args, **kwargs)


def ordered(x: VectorClock, y: VectorClock) -> bool:
  return lt(x, y) | lt(y, x)

