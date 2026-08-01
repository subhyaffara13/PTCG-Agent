
def _splitstrip(string: str, sep: str = ",") -> list[str]:
    r"""Return a list of stripped string by splitting the string given as
    argument on `sep` (',' by default), empty strings are discarded.

    >>> _splitstrip('a, b, c   ,  4,,')
    ['a', 'b', 'c', '4']
    >>> _splitstrip('a')
    ['a']
    >>> _splitstrip('a,\nb,\nc,')
    ['a', 'b', 'c']

    :type string: str or unicode
    :param string: a csv line

    :type sep: str or unicode
    :param sep: field separator, default to the comma (',')

    :rtype: str or unicode
    :return: the unquoted string (or the input string if it wasn't quoted)
    """
    return [word.strip() for word in string.split(sep) if word.strip()]

