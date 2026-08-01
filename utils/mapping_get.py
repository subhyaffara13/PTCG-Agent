
def mapping_get(obj: Mapping[T, U], key: T, value: U | None = None, /) -> U | None:
    try:
        return obj.__getitem__(key)
    except KeyError:
        return value

