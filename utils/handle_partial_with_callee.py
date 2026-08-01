
def handle_partial_with_callee(ctx: mypy.plugin.FunctionContext, callee: Type) -> Type:
    if not isinstance(ctx.api, mypy.checker.TypeChecker):  # use internals
        return ctx.default_return_type

    if isinstance(callee_proper := get_proper_type(callee), UnionType):
        return UnionType.make_union(
            [handle_partial_with_callee(ctx, item) for item in callee_proper.items]
        )

    fn_type = ctx.api.extract_callable_type(callee, ctx=ctx.default_return_type)
    if fn_type is None:
        return ctx.default_return_type

    # We must normalize from the start to have coherent view together with TypeChecker.
    fn_type = fn_type.with_unpacked_kwargs().with_normalized_var_args()

    last_context = ctx.api.type_context[-1]
    if not fn_type.is_type_obj():
        # We wrap the return type to get use of a possible type context provided by caller.
        # We cannot do this in case of class objects, since otherwise the plugin may get
        # falsely triggered when evaluating the constructed call itself.
        ret_type: Type = ctx.api.named_generic_type(PARTIAL, [fn_type.ret_type])
        wrapped_return = True
    else:
        ret_type = fn_type.ret_type
        # Instead, for class objects we ignore any type context to avoid spurious errors,
        # since the type context will be partial[X] etc., not X.
        ctx.api.type_context[-1] = None
        wrapped_return = False

    # Flatten actual to formal mapping, since this is what check_call() expects.
    actual_args = []
    actual_arg_kinds = []
    actual_arg_names = []
    actual_types = []
    seen_args = set()
    for i, param in enumerate(ctx.args[1:], start=1):
        for j, a in enumerate(param):
            if a in seen_args:
                # Same actual arg can map to multiple formals, but we need to include
                # each one only once.
                continue
            # Here we rely on the fact that expressions are essentially immutable, so
            # they can be compared by identity.
            seen_args.add(a)
            actual_args.append(a)
            actual_arg_kinds.append(ctx.arg_kinds[i][j])
            actual_arg_names.append(ctx.arg_names[i][j])
            actual_types.append(ctx.arg_types[i][j])

    formal_to_actual = map_actuals_to_formals(
        actual_kinds=actual_arg_kinds,
        actual_names=actual_arg_names,
        formal_kinds=fn_type.arg_kinds,
        formal_names=fn_type.arg_names,
        actual_arg_type=lambda i: actual_types[i],
    )

    # We need to remove any type variables that appear only in formals that have
    # no actuals, to avoid eagerly binding them in check_call() below.
    can_infer_ids = set()
    for i, arg_type in enumerate(fn_type.arg_types):
        if not formal_to_actual[i]:
            continue
        can_infer_ids.update({tv.id for tv in get_all_type_vars(arg_type)})

    # special_sig="partial" allows omission of args/kwargs typed with ParamSpec
    defaulted = fn_type.copy_modified(
        arg_kinds=[
            (
                ArgKind.ARG_OPT
                if k == ArgKind.ARG_POS
                else (ArgKind.ARG_NAMED_OPT if k == ArgKind.ARG_NAMED else k)
            )
            for k in fn_type.arg_kinds
        ],
        ret_type=ret_type,
        variables=[
            tv
            for tv in fn_type.variables
            # Keep TypeVarTuple/ParamSpec to avoid spurious errors on empty args.
            if tv.id in can_infer_ids or not isinstance(tv, TypeVarType)
        ],
        special_sig="partial",
    )
    if defaulted.line < 0:
        # Make up a line number if we don't have one
        defaulted.set_line(ctx.default_return_type)

    # Create a valid context for various ad-hoc inspections in check_call().
    call_expr = CallExpr(
        callee=ctx.args[0][0],
        args=actual_args,
        arg_kinds=actual_arg_kinds,
        arg_names=actual_arg_names,
        analyzed=ctx.context.analyzed if isinstance(ctx.context, CallExpr) else None,
    )
    call_expr.set_line(ctx.context)

    _, bound = ctx.api.expr_checker.check_call(
        callee=defaulted,
        args=actual_args,
        arg_kinds=actual_arg_kinds,
        arg_names=actual_arg_names,
        context=call_expr,
    )
    if not wrapped_return:
        # Restore previously ignored context.
        ctx.api.type_context[-1] = last_context

    bound = get_proper_type(bound)
    if not isinstance(bound, CallableType):
        return ctx.default_return_type

    if wrapped_return:
        # Reverse the wrapping we did above.
        ret_type = get_proper_type(bound.ret_type)
        if not isinstance(ret_type, Instance) or ret_type.type.fullname != PARTIAL:
            return ctx.default_return_type
        bound = bound.copy_modified(ret_type=ret_type.args[0])

    partial_kinds = []
    partial_types = []
    partial_names = []
    # We need to fully apply any positional arguments (they cannot be respecified)
    # However, keyword arguments can be respecified, so just give them a default
    for i, actuals in enumerate(formal_to_actual):
        if len(bound.arg_types) == len(fn_type.arg_types):
            arg_type = bound.arg_types[i]
            if not mypy.checker.is_valid_inferred_type(arg_type, ctx.api.options):
                arg_type = fn_type.arg_types[i]  # bit of a hack
        else:
            # TODO: I assume that bound and fn_type have the same arguments. It appears this isn't
            # true when PEP 646 things are happening. See testFunctoolsPartialTypeVarTuple
            arg_type = fn_type.arg_types[i]

        if not actuals or fn_type.arg_kinds[i] in (ArgKind.ARG_STAR, ArgKind.ARG_STAR2):
            partial_kinds.append(fn_type.arg_kinds[i])
            partial_types.append(arg_type)
            partial_names.append(fn_type.arg_names[i])
        else:
            assert actuals
            if any(actual_arg_kinds[j] in (ArgKind.ARG_POS, ArgKind.ARG_STAR) for j in actuals):
                # Don't add params for arguments passed positionally
                continue
            # Add defaulted params for arguments passed via keyword
            kind = actual_arg_kinds[actuals[0]]
            if kind == ArgKind.ARG_NAMED or kind == ArgKind.ARG_STAR2:
                kind = ArgKind.ARG_NAMED_OPT
            partial_kinds.append(kind)
            partial_types.append(arg_type)
            partial_names.append(fn_type.arg_names[i])

    ret_type = bound.ret_type
    if not mypy.checker.is_valid_inferred_type(ret_type, ctx.api.options):
        ret_type = fn_type.ret_type  # same kind of hack as above

    # Technically, we should set definition to None here, since it will not be recovered
    # on warm cache runs in fixup.py. This however may hide some helpful info in error
    # messages, so we are keeping it for now. See also issue #20640.
    partially_applied = fn_type.copy_modified(
        arg_types=partial_types,
        arg_kinds=partial_kinds,
        arg_names=partial_names,
        ret_type=ret_type,
        special_sig="partial",
    )

    # Do not leak typevars from generic functions - they cannot be usable.
    # Keep them in the wrapped callable, but avoid `partial[SomeStrayTypeVar]`
    erased_ret_type = erase_typevars(ret_type, [tv.id for tv in fn_type.variables])

    ret = ctx.api.named_generic_type(PARTIAL, [erased_ret_type])
    ret = ret.copy_with_extra_attr("__mypy_partial", partially_applied)
    if partially_applied.param_spec():
        assert ret.extra_attrs is not None  # copy_with_extra_attr above ensures this
        attrs = ret.extra_attrs.copy()
        if ArgKind.ARG_STAR in actual_arg_kinds:
            attrs.immutable.add("__mypy_partial_paramspec_args_bound")
        if ArgKind.ARG_STAR2 in actual_arg_kinds:
            attrs.immutable.add("__mypy_partial_paramspec_kwargs_bound")
        ret.extra_attrs = attrs
    return ret

