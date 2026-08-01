
def functools_total_ordering_maker_callback(
    ctx: mypy.plugin.ClassDefContext, auto_attribs_default: bool = False
) -> bool:
    """Add dunder methods to classes decorated with functools.total_ordering."""
    comparison_methods = _analyze_class(ctx)
    if not comparison_methods:
        ctx.api.fail(
            'No ordering operation defined when using "functools.total_ordering": < > <= >=',
            ctx.reason,
        )
        return True

    # prefer __lt__ to __le__ to __gt__ to __ge__
    root = max(comparison_methods, key=lambda k: (comparison_methods[k] is None, k))
    root_method = comparison_methods[root]
    if not root_method:
        # None of the defined comparison methods can be analysed
        return True

    other_type = _find_other_type(root_method)
    bool_type = ctx.api.named_type("builtins.bool")
    ret_type: Type = bool_type
    if root_method.type.ret_type != ctx.api.named_type("builtins.bool"):
        proper_ret_type = get_proper_type(root_method.type.ret_type)
        if not (
            isinstance(proper_ret_type, UnboundType)
            and proper_ret_type.name.split(".")[-1] == "bool"
        ):
            ret_type = AnyType(TypeOfAny.implementation_artifact)
    for additional_op in _ORDERING_METHODS:
        # Either the method is not implemented
        # or has an unknown signature that we can now extrapolate.
        if not comparison_methods.get(additional_op):
            args = [Argument(Var("other", other_type), other_type, None, ARG_POS)]
            add_method_to_class(ctx.api, ctx.cls, additional_op, args, ret_type)

    return True

