
def vec_pop(builder: LowLevelIRBuilder, base: Value, index: Value, line: int) -> Value:
    assert isinstance(base.type, RVec)
    vec_type = base.type
    item_type = vec_type.item_type
    index = as_platform_int(builder, index, line)

    api_name = vec_api_by_item_type.get(item_type)
    if api_name is not None:
        name = f"{api_name}.pop"
    elif vec_type.depth() == 0:
        name = "VecTApi.pop"
    else:
        name = "VecNestedApi.pop"
        # Nested vecs return a generic vec struct.
        item_type = VecNestedBufItem
    result = builder.add(
        CallC(
            name,
            [base, index],
            RTuple([vec_type, item_type]),
            steals=[True, False],
            is_borrowed=False,
            error_kind=ERR_MAGIC,
            line=line,
        )
    )
    if vec_type.depth() > 0:
        orig = result
        x = builder.add(TupleGet(result, 0, borrow=True))
        x = builder.add(Unborrow(x))
        y = builder.add(TupleGet(result, 1, borrow=True))
        y = builder.add(Unborrow(y))
        assert isinstance(vec_type.item_type, RVec)
        z = convert_from_t_ext_item(builder, y, vec_type.item_type)
        result = builder.add(TupleSet([x, z], line))
        builder.keep_alive([orig], line, steal=True)
    return result

