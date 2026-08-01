
def read_func_def(state: State, data: ReadBuffer) -> FuncDef:
    state.num_funcs += 1

    name = read_str(data)
    arguments, has_ann = read_parameters(state, data)

    if special_function_elide_names(name):
        for arg in arguments:
            arg.pos_only = True

    body = read_block(state, data)
    is_async = read_bool(data)

    # Type parameters (PEP 695)
    has_type_params = read_bool(data)
    if has_type_params:
        type_params = read_type_params(state, data)
    else:
        type_params = None

    has_return_type = read_bool(data)
    if has_return_type:
        return_type = read_type(state, data)
        has_ann = True
    else:
        return_type = None

    if has_ann:
        typ = CallableType(
            [
                arg.type_annotation if arg.type_annotation else AnyType(TypeOfAny.unannotated)
                for arg in arguments
            ],
            [arg.kind for arg in arguments],
            [None if arg.pos_only else arg.variable.name for arg in arguments],
            return_type if return_type else AnyType(TypeOfAny.unannotated),
            _dummy_fallback,
        )
    else:
        typ = None

    func_def = FuncDef(name, arguments, body, typ=typ, type_args=type_params)
    if is_async:
        func_def.is_coroutine = True
    read_loc(data, func_def)
    if type_params:
        state.check_min_version(
            "Improved type parameter syntax", (3, 12), func_def.line, func_def.column
        )
        check_type_param_defaults(state, type_params, func_def.line, func_def.column)
    if typ:
        typ.line = func_def.line
        typ.column = func_def.column
        typ.definition = func_def
        # TODO: This seems wasteful, can we avoid it?
        func_def.unanalyzed_type = typ.copy_modified()
    expect_end_tag(data)
    return func_def

