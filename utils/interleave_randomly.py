
def interleave_randomly(*iterables):
    """Repeatedly select one of the input *iterables* at random and yield the next
    item from it.

        >>> iterables = [1, 2, 3], 'abc', (True, False, None)
        >>> list(interleave_randomly(*iterables))  # doctest: +SKIP
        ['a', 'b', 1, 'c', True, False, None, 2, 3]

    The relative order of the items in each input iterable will preserved. Note the
    sequences of items with this property are not equally likely to be generated.

    """
    iterators = [iter(e) for e in iterables]
    while iterators:
        idx = randrange(len(iterators))
        try:
            yield next(iterators[idx])
        except StopIteration:
            # equivalent to `list.pop` but slightly faster
            iterators[idx] = iterators[-1]
            del iterators[-1]

