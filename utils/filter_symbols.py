
def filter_symbols(iterator, exclude):
    """
    Only yield elements from `iterator` that do not occur in `exclude`.

    Parameters
    ==========

    iterator : iterable
        iterator to take elements from

    exclude : iterable
        elements to exclude

    Returns
    =======

    iterator : iterator
        filtered iterator
    """
    exclude = set(exclude)
    for s in iterator:
        if s not in exclude:
            yield s

