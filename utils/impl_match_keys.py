
def impl_MATCH_KEYS(obj: Mapping[T, U], keys: tuple[T, ...]) -> tuple[U, ...] | None:
    assert isinstance(obj, Mapping)
    if all(key in obj for key in keys):
        return tuple(obj[key] for key in keys)
    else:
        return None

