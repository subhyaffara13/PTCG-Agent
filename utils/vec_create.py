
def vec_create(
    builder: LowLevelIRBuilder,
    vtype: RVec,
    length: int | Value,
    line: int,
    *,
    capacity: Value | None = None,
) -> Value:
    if isinstance(length, int):
        length = Integer(length, c_pyssize_t_rprimitive)
    length = as_platform_int(builder, length, line)
    if capacity is not None:
        capacity = as_platform_int(builder, capacity, line)
    else:
        capacity = length

    item_type = vtype.item_type
    api_name = vec_api_by_item_type.get(item_type)
    if api_name is not None:
        call = CallC(
            f"{api_name}.alloc",
            [length, capacity],
            vtype,
            False,
            False,
            error_kind=ERR_MAGIC,
            line=line,
        )
        return builder.add(call)

    typeobj, optional, depth = vec_item_type_info(builder, item_type, line)
    if typeobj is not None:
        typeval: Value
        if isinstance(typeobj, Integer):
            typeval = typeobj
        else:
            # Create an integer which will hold the type object * as an integral value.
            # Assign implicitly coerces between pointer/integer types.
            typeval = Register(pointer_rprimitive)
            builder.add(Assign(typeval, typeobj))
            if optional:
                typeval = builder.add(
                    IntOp(pointer_rprimitive, typeval, Integer(1, pointer_rprimitive), IntOp.OR)
                )
        if depth == 0:
            call = CallC(
                "VecTApi.alloc",
                [length, capacity, typeval],
                vtype,
                False,
                False,
                error_kind=ERR_MAGIC,
                line=line,
            )
            return builder.add(call)
        else:
            call = CallC(
                "VecNestedApi.alloc",
                [length, capacity, typeval, Integer(depth, int32_rprimitive)],
                vtype,
                False,
                False,
                error_kind=ERR_MAGIC,
                line=line,
            )
            return builder.add(call)

    assert False, "unsupported: %s" % vtype

