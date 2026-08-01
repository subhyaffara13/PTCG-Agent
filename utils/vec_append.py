
def vec_append(builder: LowLevelIRBuilder, vec: Value, item: Value, line: int) -> Value:
    vec_type = vec.type
    assert isinstance(vec_type, RVec)
    item_type = vec_type.item_type
    coerced_item = builder.coerce(item, item_type, line)
    item_type_arg = []
    api_name = vec_api_by_item_type.get(item_type)
    if api_name is not None:
        name = f"{api_name}.append"
    elif vec_type.depth() == 0:
        name = "VecTApi.append"
        item_type_arg = [vec_item_type(builder, item_type, line)]
    else:
        coerced_item = convert_to_t_ext_item(builder, coerced_item)
        name = "VecNestedApi.append"
    call = builder.add(
        CallC(
            name,
            [vec, coerced_item] + item_type_arg,
            vec_type,
            steals=[True, False] + ([False] if item_type_arg else []),
            is_borrowed=False,
            error_kind=ERR_MAGIC,
            line=line,
        )
    )
    if vec_type.depth() > 0:
        builder.keep_alive([item], line)
    return call

