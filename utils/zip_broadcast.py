
def zip_broadcast(*objects, scalar_types=(str, bytes), strict=False):
    """A version of :func:`zip` that "broadcasts" any scalar
    (i.e., non-iterable) items into output tuples.

    >>> iterable_1 = [1, 2, 3]
    >>> iterable_2 = ['a', 'b', 'c']
    >>> scalar = '_'
    >>> list(zip_broadcast(iterable_1, iterable_2, scalar))
    [(1, 'a', '_'), (2, 'b', '_'), (3, 'c', '_')]

    The *scalar_types* keyword argument determines what types are considered
    scalar. It is set to ``(str, bytes)`` by default. Set it to ``None`` to
    treat strings and byte strings as iterable:

    >>> list(zip_broadcast('abc', 0, 'xyz', scalar_types=None))
    [('a', 0, 'x'), ('b', 0, 'y'), ('c', 0, 'z')]

    If the *strict* keyword argument is ``True``, then
    ``UnequalIterablesError`` will be raised if any of the iterables have
    different lengths.
    """

    def is_scalar(obj):
        if scalar_types and isinstance(obj, scalar_types):
            return True
        try:
            iter(obj)
        except TypeError:
            return True
        else:
            return False

    size = len(objects)
    if not size:
        return

    new_item = [None] * size
    iterables, iterable_positions = [], []
    for i, obj in enumerate(objects):
        if is_scalar(obj):
            new_item[i] = obj
        else:
            iterables.append(iter(obj))
            iterable_positions.append(i)

    if not iterables:
        yield tuple(objects)
        return

    zipper = _zip_equal if strict else zip
    for item in zipper(*iterables):
        for i, new_item[i] in zip(iterable_positions, item):
            pass
        yield tuple(new_item)

