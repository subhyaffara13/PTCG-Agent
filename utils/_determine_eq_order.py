
def _determine_eq_order(ctx: mypy.plugin.ClassDefContext) -> bool:
    """
    Validate the combination of *cmp*, *eq*, and *order*. Derive the effective
    value of order.
    """
    cmp = _get_decorator_optional_bool_argument(ctx, "cmp")
    eq = _get_decorator_optional_bool_argument(ctx, "eq")
    order = _get_decorator_optional_bool_argument(ctx, "order")

    if cmp is not None and any((eq is not None, order is not None)):
        ctx.api.fail('Don\'t mix "cmp" with "eq" and "order"', ctx.reason)

    # cmp takes precedence due to bw-compatibility.
    if cmp is not None:
        return cmp

    # If left None, equality is on and ordering mirrors equality.
    if eq is None:
        eq = True

    if order is None:
        order = eq

    if eq is False and order is True:
        ctx.api.fail("eq must be True if order is True", ctx.reason)

    return order

