
def _izip_fields_flat(iterable):
    """
    Returns an iterator of concatenated fields from a sequence of arrays,
    collapsing any nested structure.

    """
    for element in iterable:
        if isinstance(element, np.void):
            yield from _izip_fields_flat(tuple(element))
        else:
            yield element

