
def get_str_query_from_sequence_iterable(
    items: Iterable[tuple[str | istr, QueryVariable]],
) -> str:
    """Return a query string from a sequence of (key, value) pairs.

    value is a single value or a sequence of values for the key

    The sequence of values must be a list or tuple.
    """
    quoter = QUERY_PART_QUOTER
    pairs = [
        f"{quoter(k)}={quoter(v if type(v) is str else query_var(v))}"
        for k, val in items
        for v in (
            val if type(val) is not str and isinstance(val, (list, tuple)) else (val,)
        )
    ]
    return "&".join(pairs)

