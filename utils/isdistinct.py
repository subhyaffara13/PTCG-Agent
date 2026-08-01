
def isdistinct(seq):
    """ All values in sequence are distinct

    >>> isdistinct([1, 2, 3])
    True
    >>> isdistinct([1, 2, 1])
    False

    >>> isdistinct("Hello")
    False
    >>> isdistinct("World")
    True
    """
    if iter(seq) is seq:
        seen = set()
        seen_add = seen.add
        for item in seq:
            if item in seen:
                return False
            seen_add(item)
        return True
    else:
        return len(seq) == len(set(seq))

