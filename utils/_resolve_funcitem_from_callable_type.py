
def _resolve_funcitem_from_callable_type(
    dec: nodes.Decorator, typ: mypy.types.CallableType
) -> nodes.FuncDef | None:
    if (
        typ.arg_kinds == [nodes.ARG_STAR, nodes.ARG_STAR2]
        and (var_arg := typ.var_arg()) is not None
        and isinstance(mypy.types.get_proper_type(var_arg.typ), mypy.types.AnyType)
        and (var_kwarg := typ.kw_arg()) is not None
        and isinstance(mypy.types.get_proper_type(var_kwarg.typ), mypy.types.AnyType)
    ):
        # There isn't a FuncDef we can invent corresponding to a Callable[..., T]
        return None

    args: list[nodes.Argument] = []
    for i, (arg_type, arg_kind, arg_name) in enumerate(
        zip(typ.arg_types, typ.arg_kinds, typ.arg_names, strict=True)
    ):
        var_name = arg_name if arg_name is not None else f"__arg{i}"
        var = nodes.Var(var_name, arg_type)
        pos_only = arg_name is None and arg_kind == nodes.ARG_POS
        args.append(
            nodes.Argument(
                variable=var,
                type_annotation=arg_type,
                initializer=None,  # CallableType doesn't store the values of defaults
                kind=arg_kind,
                pos_only=pos_only,
            )
        )

    if dec.func.is_class:
        if not args:
            return None
        # Munge classmethods, similar to logic in _resolve_funcitem_from_decorator
        if args[0].variable.name not in ("_cls", "cls", "mcs", "metacls"):
            return None
        args.pop(0)

    ret = nodes.FuncDef(name=typ.name or "", arguments=args, body=nodes.Block([]), typ=typ)
    ret.is_class = dec.func.is_class
    return ret

