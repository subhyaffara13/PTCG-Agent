
def all_unique(iterable, key=None):
    """
    Returns ``True`` if all the elements of *iterable* are unique (no two
    elements are equal).

        >>> all_unique('ABCB')
        False

    If a *key* function is specified, it will be used to make comparisons.

        >>> all_unique('ABCb')
        True
        >>> all_unique('ABCb', str.lower)
        False

    The function returns as soon as the first non-unique element is
    encountered. Iterables with a mix of hashable and unhashable items can
    be used, but the function will be slower for unhashable items.
    """
    seenset = set()
    seenset_add = seenset.add
    seenlist = []
    seenlist_add = seenlist.append
    for element in map(key, iterable) if key else iterable:
        try:
            if element in seenset:
                return False
            seenset_add(element)
        except TypeError:
            if element in seenlist:
                return False
            seenlist_add(element)
    return True

