
def make_generic_base_class(
    builder: IRBuilder, fullname: str, type_args: list[TypeParam], line: int
) -> Value:
    """Construct Generic[...] base class object for a new-style generic class (Python 3.12)."""
    mod = builder.call_c(import_op, [builder.load_str("_typing")], line)
    tvs = create_type_params(builder, mod, type_args, line)
    args = []
    for tv, type_param in zip(tvs, type_args):
        if type_param.kind == TYPE_VAR_TUPLE_KIND:
            # Evaluate *Ts for a TypeVarTuple
            it = builder.primitive_op(iter_op, [tv], line)
            tv = builder.call_c(next_op, [it], line)
        args.append(tv)

    gent = builder.py_get_attr(mod, "Generic", line)
    if len(args) == 1:
        arg = args[0]
    else:
        arg = builder.new_tuple(args, line)

    base = builder.primitive_op(py_get_item_op, [gent, arg], line)
    return base

