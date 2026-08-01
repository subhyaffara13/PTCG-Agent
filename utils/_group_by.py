
def _group_by(values: Iterable[V], get_key: Callable[[V], K]) -> dict[K, set[V]]:
    """
    Groups elements with same key into sets.
    """
    key_to_values: defaultdict[K, set[V]] = defaultdict(set)
    for value in values:
        key = get_key(value)
        key_to_values[key].add(value)
    return key_to_values

