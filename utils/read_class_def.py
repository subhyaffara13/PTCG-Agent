
def read_class_def(state: State, data: ReadBuffer) -> ClassDef:
    name = read_str(data)
    body = read_block(state, data)
    base_type_exprs = read_expression_list(state, data)

    expect_tag(data, LIST_GEN)
    n_decorators = read_int_bare(data)
    decorators = [read_expression(state, data) for _ in range(n_decorators)]

    # Type parameters (PEP 695)
    has_type_params = read_bool(data)
    if has_type_params:
        type_params = read_type_params(state, data)
    else:
        type_params = None

    expect_tag(data, DICT_STR_GEN)
    n_keywords = read_int_bare(data)
    keywords = []
    for _ in range(n_keywords):
        key = read_str(data)
        value = read_expression(state, data)
        keywords.append((key, value))

    metaclass = dict(keywords).get("metaclass") if keywords else None

    class_def = ClassDef(
        name,
        body,
        base_type_exprs=base_type_exprs if base_type_exprs else None,
        metaclass=metaclass,
        # Note we keep metaclass in keywords as well, to match the old parser.
        keywords=keywords if keywords else None,
        type_args=type_params,
    )
    class_def.decorators = decorators
    read_loc(data, class_def)
    if type_params:
        state.check_min_version(
            "Improved type parameter syntax", (3, 12), class_def.line, class_def.column
        )
        check_type_param_defaults(state, type_params, class_def.line, class_def.column)
    expect_end_tag(data)
    return class_def

