
def replace_function_sig_callback(ctx: FunctionSigContext) -> CallableType:
    """
    Returns a signature for the 'dataclasses.replace' function that's dependent on the type
    of the first positional argument.
    """
    if len(ctx.args) != 2:
        # Ideally the name and context should be callee's, but we don't have it in FunctionSigContext.
        ctx.api.fail(f'"{ctx.default_signature.name}" has unexpected type annotation', ctx.context)
        return ctx.default_signature

    if len(ctx.args[0]) != 1:
        return ctx.default_signature  # leave it to the type checker to complain

    obj_arg = ctx.args[0][0]
    obj_type = get_proper_type(ctx.api.get_expression_type(obj_arg))
    inst_type_str = format_type_bare(obj_type, ctx.api.options)

    replace_sigs = _get_expanded_dataclasses_fields(ctx, obj_type, obj_type, obj_type)
    if replace_sigs is None:
        return ctx.default_signature
    replace_sig = _meet_replace_sigs(replace_sigs)

    return replace_sig.copy_modified(
        arg_names=[None, *replace_sig.arg_names],
        arg_kinds=[ARG_POS, *replace_sig.arg_kinds],
        arg_types=[obj_type, *replace_sig.arg_types],
        ret_type=obj_type,
        fallback=ctx.default_signature.fallback,
        name=f"{ctx.default_signature.name} of {inst_type_str}",
    )

