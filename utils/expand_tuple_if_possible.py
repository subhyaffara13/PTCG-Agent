
def expand_tuple_if_possible(tup: TupleType, target: int) -> TupleType:
    if len(tup.items) > target + 1:
        return tup
    extra = target + 1 - len(tup.items)
    new_items = []
    for it in tup.items:
        if not isinstance(it, UnpackType):
            new_items.append(it)
            continue
        unpacked = get_proper_type(it.type)
        if isinstance(unpacked, TypeVarTupleType):
            instance = unpacked.tuple_fallback
        else:
            # Nested non-variadic tuples should be normalized at this point.
            assert isinstance(unpacked, Instance)
            instance = unpacked
        assert instance.type.fullname == "builtins.tuple"
        new_items.extend([instance.args[0]] * extra)
    return tup.copy_modified(items=new_items)

