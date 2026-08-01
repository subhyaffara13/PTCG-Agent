
def _izip_fields(iterable):
    """
    Returns an iterator of concatenated fields from a sequence of arrays.

    """
    for element in iterable:
        if (hasattr(element, '__iter__') and
                not isinstance(element, str)):
            yield from _izip_fields(element)
        elif isinstance(element, np.void) and len(tuple(element)) == 1:
            # this statement is the same from the previous expression
            yield from _izip_fields(element)
        else:
            yield element

