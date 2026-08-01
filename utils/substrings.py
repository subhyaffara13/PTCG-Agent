
def substrings(iterable):
    """Yield all of the substrings of *iterable*.

        >>> [''.join(s) for s in substrings('more')]
        ['m', 'o', 'r', 'e', 'mo', 'or', 're', 'mor', 'ore', 'more']

    Note that non-string iterables can also be subdivided.

        >>> list(substrings([0, 1, 2]))
        [(0,), (1,), (2,), (0, 1), (1, 2), (0, 1, 2)]

    """
    # The length-1 substrings
    seq = []
    for item in iterable:
        seq.append(item)
        yield (item,)
    seq = tuple(seq)
    item_count = len(seq)

    # And the rest
    for n in range(2, item_count + 1):
        for i in range(item_count - n + 1):
            yield seq[i : i + n]

