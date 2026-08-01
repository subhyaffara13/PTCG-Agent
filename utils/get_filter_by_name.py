
def get_filter_by_name(filtername, **options):
    """Return an instantiated filter.

    Options are passed to the filter initializer if wanted.
    Raise a ClassNotFound if not found.
    """
    cls = find_filter_class(filtername)
    if cls:
        return cls(**options)
    else:
        raise ClassNotFound(f'filter {filtername!r} not found')


def get_filter_by_name(filtername, **options):
    """Return an instantiated filter.

    Options are passed to the filter initializer if wanted.
    Raise a ClassNotFound if not found.
    """
    cls = find_filter_class(filtername)
    if cls:
        return cls(**options)
    else:
        raise ClassNotFound(f'filter {filtername!r} not found')

