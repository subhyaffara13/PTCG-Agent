
def get_str_query_from_iterable(
    items: Iterable[tuple[str | istr, SimpleQuery]],
) -> str:
    """Return a query string from an iterable.

    The iterable must contain (key, value) pairs.

    The values are not allowed to be sequences, only single values are
    allowed. For sequences, use `_get_str_query_from_sequence_iterable`.
    """
    quoter = QUERY_PART_QUOTER
    # A listcomp is used since listcomps are inlined on CPython 3.12+ and
    # they are a bit faster than a generator expression.
    pairs = [
        f"{quoter(k)}={quoter(v if type(v) is str else query_var(v))}" for k, v in items
    ]
    return "&".join(pairs)

