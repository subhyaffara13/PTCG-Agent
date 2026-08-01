
def read_parameters(state: State, data: ReadBuffer) -> tuple[list[Argument], bool]:
    """Read function/lambda parameters.

    Return (parameters, has_annotations).
    """
    expect_tag(data, LIST_GEN)
    n_args = read_int_bare(data)
    arguments = []
    has_ann = False
    for _ in range(n_args):
        arg_name = read_str(data)
        arg_kind_int = read_int(data)
        arg_kind = ARG_KINDS[arg_kind_int]
        has_type = read_bool(data)
        if has_type:
            ann = read_type(state, data)
            has_ann = True
        else:
            ann = None
        has_default = read_bool(data)
        if has_default:
            default = read_expression(state, data)
        else:
            default = None
        pos_only = read_bool(data)

        if state.options.implicit_optional and ann is not None:
            optional = isinstance(default, NameExpr) and default.name == "None"
            if isinstance(ann, UnboundType):
                ann.optional = optional

        var = Var(arg_name, ann)
        var.is_inferred = False
        var.is_argument = True
        arg = Argument(var, ann, default, arg_kind, pos_only)
        read_loc(data, arg)
        set_line_column_range(var, arg)
        arguments.append(arg)

    return arguments, has_ann

