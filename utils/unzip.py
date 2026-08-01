
def unzip(infile, mode="rb", filename=None, **kwargs):
    if "r" not in mode:
        filename = filename or "file"
        z = ZipFile(infile, mode="w", **kwargs)
        fo = z.open(filename, mode="w")
        fo.close = lambda closer=fo.close: closer() or z.close()
        return fo
    z = ZipFile(infile)
    if filename is None:
        filename = z.namelist()[0]
    return z.open(filename, mode="r", **kwargs)


def unzip(seq):
    """Inverse of ``zip``

    >>> a, b = unzip([('a', 1), ('b', 2)])
    >>> list(a)
    ['a', 'b']
    >>> list(b)
    [1, 2]

    Unlike the naive implementation ``def unzip(seq): zip(*seq)`` this
    implementation can handle an infinite sequence ``seq``.

    Caveats:

    * The implementation uses ``tee``, and so can use a significant amount
      of auxiliary storage if the resulting iterators are consumed at
      different times.

    * The inner sequence cannot be infinite. In Python 3 ``zip(*seq)`` can be
      used if ``seq`` is a finite sequence of infinite sequences.

    """

    seq = iter(seq)

    # Check how many iterators we need
    try:
        first = tuple(next(seq))
    except StopIteration:
        return tuple()

    # and create them
    niters = len(first)
    seqs = tee(cons(first, seq), niters)

    return tuple(starmap(pluck, enumerate(seqs)))


def unzip(iterable):
    """The inverse of :func:`zip`, this function disaggregates the elements
    of the zipped *iterable*.

    The ``i``-th iterable contains the ``i``-th element from each element
    of the zipped iterable. The first element is used to determine the
    length of the remaining elements.

        >>> iterable = [('a', 1), ('b', 2), ('c', 3), ('d', 4)]
        >>> letters, numbers = unzip(iterable)
        >>> list(letters)
        ['a', 'b', 'c', 'd']
        >>> list(numbers)
        [1, 2, 3, 4]

    This is similar to using ``zip(*iterable)``, but it avoids reading
    *iterable* into memory. Note, however, that this function uses
    :func:`itertools.tee` and thus may require significant storage.

    """
    head, iterable = spy(iterable)
    if not head:
        # empty iterable, e.g. zip([], [], [])
        return ()
    # spy returns a one-length iterable as head
    head = head[0]
    iterables = tee(iterable, len(head))

    # If we have an iterable like iter([(1, 2, 3), (4, 5), (6,)]),
    # the second unzipped iterable fails at the third tuple since
    # it tries to access (6,)[1].
    # Same with the third unzipped iterable and the second tuple.
    # To support these "improperly zipped" iterables, we suppress
    # the IndexError, which just stops the unzipped iterables at
    # first length mismatch.
    return tuple(
        iter_suppress(map(itemgetter(i), it), IndexError)
        for i, it in enumerate(iterables)
    )

