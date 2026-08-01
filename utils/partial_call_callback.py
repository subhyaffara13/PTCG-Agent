
def partial_call_callback(ctx: mypy.plugin.MethodContext) -> Type:
    """Infer a more precise return type for functools.partial.__call__."""
    if (
        not isinstance(ctx.api, mypy.checker.TypeChecker)  # use internals
        or not isinstance(ctx.type, Instance)
        or ctx.type.type.fullname != PARTIAL
        or not ctx.type.extra_attrs
        or "__mypy_partial" not in ctx.type.extra_attrs.attrs
    ):
        return ctx.default_return_type

    extra_attrs = ctx.type.extra_attrs
    partial_type = get_proper_type(extra_attrs.attrs["__mypy_partial"])
    if len(ctx.arg_types) != 2:  # *args, **kwargs
        return ctx.default_return_type

    # See comments for similar actual to formal code above
    actual_args = []
    actual_arg_kinds = []
    actual_arg_names = []
    seen_args = set()
    for i, param in enumerate(ctx.args):
        for j, a in enumerate(param):
            if a in seen_args:
                continue
            seen_args.add(a)
            actual_args.append(a)
            actual_arg_kinds.append(ctx.arg_kinds[i][j])
            actual_arg_names.append(ctx.arg_names[i][j])

    result, _ = ctx.api.expr_checker.check_call(
        callee=partial_type,
        args=actual_args,
        arg_kinds=actual_arg_kinds,
        arg_names=actual_arg_names,
        context=ctx.context,
    )
    if not isinstance(partial_type, CallableType) or partial_type.param_spec() is None:
        return result

    args_bound = "__mypy_partial_paramspec_args_bound" in extra_attrs.immutable
    kwargs_bound = "__mypy_partial_paramspec_kwargs_bound" in extra_attrs.immutable

    passed_paramspec_parts = [
        arg.node.type
        for arg in actual_args
        if isinstance(arg, NameExpr)
        and isinstance(arg.node, Var)
        and isinstance(arg.node.type, ParamSpecType)
    ]
    # ensure *args: P.args
    args_passed = any(part.flavor == ParamSpecFlavor.ARGS for part in passed_paramspec_parts)
    if not args_bound and not args_passed:
        ctx.api.expr_checker.msg.too_few_arguments(partial_type, ctx.context, actual_arg_names)
    elif args_bound and args_passed:
        ctx.api.expr_checker.msg.too_many_arguments(partial_type, ctx.context)

    # ensure **kwargs: P.kwargs
    kwargs_passed = any(part.flavor == ParamSpecFlavor.KWARGS for part in passed_paramspec_parts)
    if not kwargs_bound and not kwargs_passed:
        ctx.api.expr_checker.msg.too_few_arguments(partial_type, ctx.context, actual_arg_names)

    return result

