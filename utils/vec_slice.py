
def vec_slice(
    builder: LowLevelIRBuilder, vec: Value, begin: Value, end: Value, line: int
) -> Value:
    assert isinstance(vec.type, RVec)
    vec_type = vec.type
    item_type = vec_type.item_type
    begin = builder.coerce(begin, int64_rprimitive, line)
    end = builder.coerce(end, int64_rprimitive, line)
    api_name = vec_api_by_item_type.get(item_type)
    if api_name is not None:
        name = f"{api_name}.slice"
    elif vec_type.depth() == 0:
        name = "VecTApi.slice"
    else:
        name = "VecNestedApi.slice"
    call = CallC(
        name,
        [vec, begin, end],
        vec_type,
        steals=[False, False, False],
        is_borrowed=False,
        error_kind=ERR_MAGIC,
        line=line,
    )
    return builder.add(call)

