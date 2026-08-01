
def get_edge_candidates(o: object) -> Iterator[tuple[object, object]]:
    # use getattr because mypyc expects dict, not mappingproxy
    if "__getattribute__" in getattr(type(o), "__dict__"):  # noqa: B009
        return
    if type(o) not in COLLECTION_TYPE_BLACKLIST:
        for attr in dir(o):
            try:
                if attr not in ATTR_BLACKLIST and hasattr(o, attr) and not isproperty(o, attr):
                    e = getattr(o, attr)
                    if type(e) not in ATOMIC_TYPE_BLACKLIST:
                        yield attr, e
            except AssertionError:
                pass
    if isinstance(o, Mapping):
        yield from o.items()
    elif isinstance(o, Iterable) and not isinstance(o, str):
        for i, e in enumerate(o):
            yield i, e

