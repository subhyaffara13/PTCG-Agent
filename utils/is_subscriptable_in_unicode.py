
def is_subscriptable_in_unicode(subscript):
    """
    Checks whether a string is subscriptable in unicode or not.

    Parameters
    ==========

    subscript: the string which needs to be checked

    Examples
    ========

    >>> from sympy.printing.pretty.pretty_symbology import is_subscriptable_in_unicode
    >>> is_subscriptable_in_unicode('abc')
    False
    >>> is_subscriptable_in_unicode('123')
    True

    """
    return all(character in sub for character in subscript)

