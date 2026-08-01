
def vec_extend(builder: LowLevelIRBuilder, vec: Value, iterable: Value, line: int) -> Value:
    vec_type = vec.type
    assert isinstance(vec_type, RVec)
    item_type = vec_type.item_type
    if isinstance(iterable.type, RVec) and iterable.type == vec_type:
        suffix = "_vec"
        src = iterable
    else:
        suffix = ""
        src = builder.coerce(iterable, object_rprimitive, line)
    item_type_arg: list[Value] = []
    api_name = vec_api_by_item_type.get(item_type)
    if api_name is not None:
        name = f"{api_name}.extend{suffix}"
    elif vec_type.depth() == 0:
        name = f"VecTApi.extend{suffix}"
        item_type_arg = [vec_item_type(builder, item_type, line)]
    else:
        name = f"VecNestedApi.extend{suffix}"
    return builder.add(
        CallC(
            name,
            [vec, src] + item_type_arg,
            vec_type,
            steals=[True, False] + ([False] if item_type_arg else []),
            is_borrowed=False,
            error_kind=ERR_MAGIC,
            line=line,
        )
    )

