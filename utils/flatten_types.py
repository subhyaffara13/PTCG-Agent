
def flatten_types(types: Iterable[Type]) -> Iterable[Type]:
    for t in types:
        tp = get_proper_type(t)
        if isinstance(tp, UnionType):
            yield from flatten_types(tp.items)
        else:
            yield t

