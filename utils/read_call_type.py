
def read_call_type(state: State, data: ReadBuffer) -> Type:
    """Read Call in type context (Arg/DefaultArg/VarArg/KwArg constructor)."""
    callee_type = read_type(state, data)

    # Read positional arguments
    expect_tag(data, LIST_GEN)
    n_args = read_int_bare(data)
    args = [read_type(state, data) for _ in range(n_args)]

    # Read keyword arguments
    expect_tag(data, LIST_GEN)
    n_kwargs = read_int_bare(data)
    kwargs = []
    for _ in range(n_kwargs):
        tag_kw = read_tag(data)
        if tag_kw == LITERAL_NONE:
            kw_name = None
        elif tag_kw == LITERAL_STR:
            kw_name = read_str_bare(data)
        else:
            assert False, f"Unexpected tag for keyword name: {tag_kw}"
        kw_value = read_type(state, data)
        kwargs.append((kw_name, kw_value))

    constructor = stringify_type_name(callee_type)

    invalid = AnyType(TypeOfAny.from_error)
    read_loc(data, invalid)
    expect_end_tag(data)

    if not constructor:
        state.add_error(
            message_registry.ARG_CONSTRUCTOR_NAME_EXPECTED.value,
            invalid.line,
            invalid.column,
            blocker=True,
            code="misc",
        )
        return invalid

    # Extract type and name from arguments
    name: str | None = None
    name_set_from_positional = False
    default_type = AnyType(TypeOfAny.special_form)
    typ: Type = default_type
    typ_set_from_positional = False

    # Process positional arguments
    for i, arg in enumerate(args):
        if i == 0:
            typ = arg
            typ_set_from_positional = True
        elif i == 1:
            name = extract_arg_name(arg)
            name_set_from_positional = True
        else:
            state.add_error(
                message_registry.ARG_CONSTRUCTOR_TOO_MANY_ARGS.value,
                invalid.line,
                invalid.column,
                blocker=True,
                code="misc",
            )

    # Process keyword arguments
    for kw_name, kw_value in kwargs:
        if kw_name == "name":
            if name is not None and name_set_from_positional:
                state.add_error(
                    message_registry.MULTIPLE_VALUES_FOR_NAME_KWARG.format(constructor).value,
                    invalid.line,
                    invalid.column,
                    blocker=True,
                    code="misc",
                )
            name = extract_arg_name(kw_value)
        elif kw_name == "type":
            if typ is not default_type and typ_set_from_positional:
                state.add_error(
                    message_registry.MULTIPLE_VALUES_FOR_TYPE_KWARG.format(constructor).value,
                    invalid.line,
                    invalid.column,
                    blocker=True,
                    code="misc",
                )
            typ = kw_value
        else:
            state.add_error(
                message_registry.ARG_CONSTRUCTOR_UNEXPECTED_ARG.format(kw_name).value,
                invalid.line,
                invalid.column,
                blocker=True,
                code="misc",
            )

    call_arg = CallableArgument(typ, name, constructor)
    set_line_column_range(call_arg, invalid)
    return call_arg

