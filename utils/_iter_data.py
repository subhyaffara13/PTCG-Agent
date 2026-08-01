
def _iter_data(data: t.Mapping[str, t.Any]) -> t.Iterator[tuple[str, t.Any]]:
    """Iterate over a mapping that might have a list of values, yielding
    all key, value pairs. Almost like iter_multi_items but only allows
    lists, not tuples, of values so tuples can be used for files.
    """
    if isinstance(data, MultiDict):
        yield from data.items(multi=True)
    else:
        for key, value in data.items():
            if isinstance(value, list):
                for v in value:
                    yield key, v
            else:
                yield key, value

