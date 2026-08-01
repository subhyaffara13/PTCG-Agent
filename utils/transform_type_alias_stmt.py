
def transform_type_alias_stmt(builder: IRBuilder, s: TypeAliasStmt) -> None:
    line = s.line
    # Use "_typing" to avoid importing "typing", as the latter can be expensive.
    # "_typing" includes everything we need here.
    mod = builder.call_c(import_op, [builder.load_str("_typing")], line)
    type_params = create_type_params(builder, mod, s.type_args, s.line)

    type_alias_type = builder.py_get_attr(mod, "TypeAliasType", line)
    args = [builder.load_str(s.name.name), builder.none()]
    arg_names: list[str | None] = [None, None]
    arg_kinds = [ARG_POS, ARG_POS]
    if s.type_args:
        args.append(builder.new_tuple(type_params, line))
        arg_names.append("type_params")
        arg_kinds.append(ARG_NAMED)
    alias = builder.py_call(type_alias_type, args, line, arg_names=arg_names, arg_kinds=arg_kinds)

    # Use primitive to set function used to lazily compute type alias type value.
    # The value needs to be lazily computed to match Python runtime behavior, but
    # Python public APIs don't support this, so we use a C primitive.
    compute_fn = s.value.accept(builder.visitor)
    builder.builder.primitive_op(set_type_alias_compute_function_op, [alias, compute_fn], line)

    target = builder.get_assignment_target(s.name)
    builder.assign(target, alias, line)

