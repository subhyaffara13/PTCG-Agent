
def duplicates_everseen(iterable, key=None):
    """Yield duplicate elements after their first appearance.

    >>> list(duplicates_everseen('mississippi'))
    ['s', 'i', 's', 's', 'i', 'p', 'i']
    >>> list(duplicates_everseen('AaaBbbCccAaa', str.lower))
    ['a', 'a', 'b', 'b', 'c', 'c', 'A', 'a', 'a']

    This function is analogous to :func:`unique_everseen` and is subject to
    the same performance considerations.

    """
    seen_set = set()
    seen_list = []
    use_key = key is not None

    for element in iterable:
        k = key(element) if use_key else element
        try:
            if k not in seen_set:
                seen_set.add(k)
            else:
                yield element
        except TypeError:
            if k not in seen_list:
                seen_list.append(k)
            else:
                yield element

