
def _get_write_alias(x) -> str | None:
    alias_set = x.alias_set
    if not alias_set or not x.is_write:
        return None
    # torchscript allows for complicated alias sets, but our dispatcher ops only really involve simple aliasing
    if len(alias_set) != 1:
        raise AssertionError("Expected alias_set to contain exactly one element")
    # timeit says next(iter(alias_set)) is faster than list(alias_set)[0] even for
    # set of size 1 on Python 3.13.
    return next(iter(alias_set))

