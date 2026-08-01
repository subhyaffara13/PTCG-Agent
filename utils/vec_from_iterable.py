
def vec_from_iterable(
    builder: IRBuilder,
    vec_type: RVec,
    iterable: Expression,
    line: int,
    *,
    capacity: Value | None = None,
) -> Value:
    """Construct a vec from an arbitrary iterable."""
    item_type = vec_type.item_type
    api_name = vec_api_by_item_type.get(item_type)
    iterable_rtype = builder.node_type(iterable)
    use_c_from_iterable = (
        is_object_rprimitive(iterable_rtype)
        or is_list_rprimitive(iterable_rtype)
        or is_tuple_rprimitive(iterable_rtype)
    )
    if api_name is not None and (
        use_c_from_iterable
        or is_bytes_rprimitive(iterable_rtype)
        or is_bytearray_rprimitive(iterable_rtype)
    ):
        # For generic iterables (typed as object) and bytes/bytearray
        # (which support the buffer protocol for fast memcpy), call the
        # C-level from_iterable. For concrete types like range, list,
        # vec, etc., the for-loop desugaring below produces better IR.
        name = f"{api_name}.from_iterable"
        extra_args: list[Value] = []
    elif api_name is None and vec_type.depth() == 0 and use_c_from_iterable:
        name = "VecTApi.from_iterable"
        extra_args = [vec_item_type(builder.builder, item_type, line)]
    else:
        name = None
    if name is not None:
        iterable_val = builder.accept(iterable)
        cap = (
            as_platform_int(builder.builder, capacity, line)
            if capacity is not None
            else Integer(0, int64_rprimitive)
        )
        args = extra_args + [iterable_val, cap]
        call = CallC(
            name,
            args,
            vec_type,
            steals=[False] * len(args),
            is_borrowed=False,
            error_kind=ERR_MAGIC,
            line=line,
        )
        return builder.add(call)

    # Use a for loop with vec_append. The comprehension helper
    # special-cases range, list, vec, etc. for efficient iteration.
    vec = Register(vec_type)
    builder.assign(vec, vec_create(builder.builder, vec_type, 0, line, capacity=capacity), line)
    name = f"___tmp_{line}"
    var = Var(name)
    reg = builder.add_local(var, vec_type.item_type)
    index = NameExpr(name)
    index.kind = LDEF
    index.node = var
    loop_params: list[tuple[Expression, Expression, list[Expression], bool]] = [
        (index, iterable, [], False)
    ]

    def gen_inner_stmts() -> None:
        builder.assign(vec, vec_append(builder.builder, vec, reg, line), line)

    comprehension_helper(builder, loop_params, gen_inner_stmts, line)
    return vec

