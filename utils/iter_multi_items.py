
def iter_multi_items(
    mapping: (
        MultiDict[K, V]
        | cabc.Mapping[K, V | list[V] | tuple[V, ...] | set[V]]
        | cabc.Iterable[tuple[K, V]]
    ),
) -> cabc.Iterator[tuple[K, V]]:
    """Iterates over the items of a mapping yielding keys and values
    without dropping any from more complex structures.
    """
    if isinstance(mapping, MultiDict):
        yield from mapping.items(multi=True)
    elif isinstance(mapping, cabc.Mapping):
        for key, value in mapping.items():
            if isinstance(value, (list, tuple, set)):
                for v in value:
                    yield key, v
            else:
                yield key, value
    else:
        yield from mapping

