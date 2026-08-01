
def longest_common_prefix(iterables):
    """Yield elements of the longest common prefix among given *iterables*.

    >>> ''.join(longest_common_prefix(['abcd', 'abc', 'abf']))
    'ab'

    """
    return (c[0] for c in takewhile(all_equal, zip(*iterables)))

