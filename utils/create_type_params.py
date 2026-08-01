
def create_type_params(
    builder: IRBuilder, typing_mod: Value, type_args: list[TypeParam], line: int
) -> list[Value]:
    """Create objects representing various kinds of Python 3.12 type parameters.

    The "typing_mod" argument is the "_typing" module object. The type objects
    are looked up from it.

    The returned list has one item for each "type_args" item, in the same order.
    Each item is either a TypeVar, TypeVarTuple or ParamSpec instance.
    """
    tvs = []
    type_var_imported: Value | None = None
    for type_param in type_args:
        if type_param.kind == TYPE_VAR_KIND:
            if type_var_imported:
                # Reuse previously imported value as a minor optimization
                tvt = type_var_imported
            else:
                tvt = builder.py_get_attr(typing_mod, "TypeVar", line)
                type_var_imported = tvt
        elif type_param.kind == TYPE_VAR_TUPLE_KIND:
            tvt = builder.py_get_attr(typing_mod, "TypeVarTuple", line)
        else:
            assert type_param.kind == PARAM_SPEC_KIND
            tvt = builder.py_get_attr(typing_mod, "ParamSpec", line)
        if type_param.kind != TYPE_VAR_TUPLE_KIND:
            # To match runtime semantics, pass infer_variance=True
            tv = builder.py_call(
                tvt,
                [builder.load_str(type_param.name, line), builder.true(line)],
                line,
                arg_kinds=[ARG_POS, ARG_NAMED],
                arg_names=[None, "infer_variance"],
            )
        else:
            tv = builder.py_call(tvt, [builder.load_str(type_param.name, line)], line)
        builder.init_type_var(tv, type_param.name, line)
        tvs.append(tv)
    return tvs

