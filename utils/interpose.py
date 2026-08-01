
def interpose(el, seq):
    """ Introduce element between each pair of elements in seq

    >>> list(interpose("a", [1, 2, 3]))
    [1, 'a', 2, 'a', 3]
    """
    inposed = concat(zip(itertools.repeat(el), seq))
    next(inposed)
    return inposed

