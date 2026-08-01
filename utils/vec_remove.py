
def vec_remove(builder: LowLevelIRBuilder, vec: Value, item: Value, line: int) -> Value:
    assert isinstance(vec.type, RVec)
    vec_type = vec.type
    item_type = vec_type.item_type
    coerced_item = builder.coerce(item, item_type, line)

    if item_type in vec_api_by_item_type:
        name = f"{vec_api_by_item_type[item_type]}.remove"
    elif vec_type.depth() == 0:
        name = "VecTApi.remove"
    else:
        coerced_item = convert_to_t_ext_item(builder, coerced_item)
        name = "VecNestedApi.remove"
    call = builder.add(
        CallC(
            name,
            [vec, coerced_item],
            vec_type,
            steals=[True, False],
            is_borrowed=False,
            error_kind=ERR_MAGIC,
            line=line,
        )
    )
    if vec_type.depth() > 0:
        builder.keep_alive([item], line)
    return call

