
def groupby_transform(iterable, keyfunc=None, valuefunc=None, reducefunc=None):
    """An extension of :func:`itertools.groupby` that can apply transformations
    to the grouped data.

    * *keyfunc* is a function computing a key value for each item in *iterable*
    * *valuefunc* is a function that transforms the individual items from
      *iterable* after grouping
    * *reducefunc* is a function that transforms each group of items

    >>> iterable = 'aAAbBBcCC'
    >>> keyfunc = lambda k: k.upper()
    >>> valuefunc = lambda v: v.lower()
    >>> reducefunc = lambda g: ''.join(g)
    >>> list(groupby_transform(iterable, keyfunc, valuefunc, reducefunc))
    [('A', 'aaa'), ('B', 'bbb'), ('C', 'ccc')]

    Each optional argument defaults to an identity function if not specified.

    :func:`groupby_transform` is useful when grouping elements of an iterable
    using a separate iterable as the key. To do this, :func:`zip` the iterables
    and pass a *keyfunc* that extracts the first element and a *valuefunc*
    that extracts the second element::

        >>> from operator import itemgetter
        >>> keys = [0, 0, 1, 1, 1, 2, 2, 2, 3]
        >>> values = 'abcdefghi'
        >>> iterable = zip(keys, values)
        >>> grouper = groupby_transform(iterable, itemgetter(0), itemgetter(1))
        >>> [(k, ''.join(g)) for k, g in grouper]
        [(0, 'ab'), (1, 'cde'), (2, 'fgh'), (3, 'i')]

    Note that the order of items in the iterable is significant.
    Only adjacent items are grouped together, so if you don't want any
    duplicate groups, you should sort the iterable by the key function.

    """
    ret = groupby(iterable, keyfunc)
    if valuefunc:
        ret = ((k, map(valuefunc, g)) for k, g in ret)
    if reducefunc:
        ret = ((k, reducefunc(g)) for k, g in ret)

    return ret

