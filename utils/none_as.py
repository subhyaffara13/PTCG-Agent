
def none_as(value, replacement=None):
    """
    >>> none_as(None, 'foo')
    'foo'
    >>> none_as('bar', 'foo')
    'bar'
    """
    return replacement if value is None else value


def none_as(value, replacement=None):
    """
    >>> none_as(None, 'foo')
    'foo'
    >>> none_as('bar', 'foo')
    'bar'
    """
    return replacement if value is None else value

