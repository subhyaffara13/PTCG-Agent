from typing import Any, Union

def get_str_query(*args: Any, **kwargs: Any) -> str | None:
    """Return a query string from supported args."""
    query: (
        str
        | Mapping[str, QueryVariable]
        | Sequence[tuple[str | istr, SimpleQuery]]
        | None
    )
    if kwargs:
        if args:
            msg = "Either kwargs or single query parameter must be present"
            raise ValueError(msg)
        query = kwargs
    elif len(args) == 1:
        query = args[0]
    else:
        raise ValueError("Either kwargs or single query parameter must be present")

    if query is None:
        return None
    if not query:
        return ""
    if type(query) is dict:
        return get_str_query_from_sequence_iterable(query.items())
    if type(query) is str or isinstance(query, str):
        return QUERY_QUOTER(query)
    if isinstance(query, Mapping):
        return get_str_query_from_sequence_iterable(query.items())
    if isinstance(query, (bytes, bytearray, memoryview)):
        msg = "Invalid query type: bytes, bytearray and memoryview are forbidden"
        raise TypeError(msg)
    if isinstance(query, Sequence):
        # We don't expect sequence values if we're given a list of pairs
        # already; only mappings like builtin `dict` which can't have the
        # same key pointing to multiple values are allowed to use
        # `_query_seq_pairs`.
        if TYPE_CHECKING:
            query = cast(Sequence[tuple[Union[str, istr], SimpleQuery]], query)
        return get_str_query_from_iterable(query)
    raise TypeError(
        "Invalid query type: only str, mapping or "
        "sequence of (key, value) pairs is allowed"
    )

