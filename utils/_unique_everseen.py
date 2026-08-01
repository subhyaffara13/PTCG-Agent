
def _unique_everseen(iterable):
    # Adapted from https://docs.python.org/3/library/itertools.html examples
    "List unique elements, preserving order. Remember all elements ever seen."
    # unique_everseen('AAAABBBCCDAABBB') --> A B C D
    seen = set()
    seen_add = seen.add
    for element in _filterfalse(seen.__contains__, iterable):
        seen_add(element)
        yield element

