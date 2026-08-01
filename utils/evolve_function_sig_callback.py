
def evolve_function_sig_callback(ctx: mypy.plugin.FunctionSigContext) -> CallableType:
    """
    Generate a signature for the 'attr.evolve' function that's specific to the call site
    and dependent on the type of the first argument.
    """
    if len(ctx.args) != 2:
        # Ideally the name and context should be callee's, but we don't have it in FunctionSigContext.
        ctx.api.fail(f'"{ctx.default_signature.name}" has unexpected type annotation', ctx.context)
        return ctx.default_signature

    if len(ctx.args[0]) != 1:
        return ctx.default_signature  # leave it to the type checker to complain

    inst_arg = ctx.args[0][0]
    inst_type = get_proper_type(ctx.api.get_expression_type(inst_arg))
    inst_type_str = format_type_bare(inst_type, ctx.api.options)

    attr_types = _get_expanded_attr_types(ctx, inst_type, inst_type, inst_type)
    if attr_types is None:
        return ctx.default_signature
    fields = _meet_fields(attr_types)

    return CallableType(
        arg_names=["inst", *fields.keys()],
        arg_kinds=[ARG_POS] + [ARG_NAMED_OPT] * len(fields),
        arg_types=[inst_type, *fields.values()],
        ret_type=inst_type,
        fallback=ctx.default_signature.fallback,
        name=f"{ctx.default_signature.name} of {inst_type_str}",
    )

