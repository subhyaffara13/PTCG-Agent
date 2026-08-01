
def tuple_fallback(typ: TupleType) -> Instance:
    """Return fallback type for a tuple."""
    info = typ.partial_fallback.type
    if info.fullname != "builtins.tuple":
        return typ.partial_fallback
    items = []
    for item in typ.items:
        if isinstance(item, UnpackType):
            unpacked_type = get_proper_type(item.type)
            if isinstance(unpacked_type, TypeVarTupleType):
                unpacked_type = get_proper_type(unpacked_type.upper_bound)
            if (
                isinstance(unpacked_type, Instance)
                and unpacked_type.type.fullname == "builtins.tuple"
            ):
                items.append(unpacked_type.args[0])
            else:
                raise NotImplementedError
        else:
            items.append(item)
    return Instance(
        info,
        # Note: flattening recursive unions is dangerous, since it can fool recursive
        # types optimization in subtypes.py and go into infinite recursion.
        [make_simplified_union(items, handle_recursive=False)],
        extra_attrs=typ.partial_fallback.extra_attrs,
    )

