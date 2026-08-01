
def collapse_variadic_union(typ: UnionType) -> Type:
    """Simplify a union involving variadic tuple if possible.

    This will collapse a type like e.g.
        tuple[X, Z] | tuple[X, Y, Z] | tuple[X, Y, Y, *tuple[Y, ...], Z]
    back to
        tuple[X, *tuple[Y, ...], Z]
    which is equivalent, but much simpler form of the same type.
    """
    tuple_items = []
    other_items = []
    for t in typ.items:
        p_t = get_proper_type(t)
        if isinstance(p_t, TupleType):
            tuple_items.append(p_t)
        else:
            other_items.append(t)
    if len(tuple_items) <= 1:
        # This type cannot be simplified further.
        return typ
    tuple_items = sorted(tuple_items, key=lambda t: len(t.items))
    first = tuple_items[0]
    last = tuple_items[-1]
    unpack_index = find_unpack_in_list(last.items)
    if unpack_index is None:
        return typ
    unpack = last.items[unpack_index]
    assert isinstance(unpack, UnpackType)
    unpacked = get_proper_type(unpack.type)
    if not isinstance(unpacked, Instance):
        return typ
    assert unpacked.type.fullname == "builtins.tuple"
    suffix = last.items[unpack_index + 1 :]

    # Check that first item matches the expected pattern and infer prefix.
    if len(first.items) < len(suffix):
        return typ
    if suffix and first.items[-len(suffix) :] != suffix:
        return typ
    if suffix:
        prefix = first.items[: -len(suffix)]
    else:
        prefix = first.items

    # Check that all middle types match the expected pattern as well.
    arg = unpacked.args[0]
    for i, it in enumerate(tuple_items[1:-1]):
        if it.items != prefix + [arg] * (i + 1) + suffix:
            return typ

    # Check the last item (the one with unpack), and choose an appropriate simplified type.
    if last.items != prefix + [arg] * (len(typ.items) - 1) + [unpack] + suffix:
        return typ
    if len(first.items) == 0:
        simplified: Type = unpacked.copy_modified()
    else:
        simplified = TupleType(prefix + [unpack] + suffix, fallback=last.partial_fallback)
    return UnionType.make_union([simplified] + other_items)

