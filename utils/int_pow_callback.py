
def int_pow_callback(ctx: MethodContext) -> Type:
    """Infer a more precise return type for int.__pow__."""
    # int.__pow__ has an optional modulo argument,
    # so we expect 2 argument positions
    if len(ctx.arg_types) == 2 and len(ctx.arg_types[0]) == 1 and len(ctx.arg_types[1]) == 0:
        arg = ctx.args[0][0]
        if isinstance(arg, IntExpr):
            exponent = arg.value
        elif isinstance(arg, UnaryExpr) and arg.op == "-" and isinstance(arg.expr, IntExpr):
            exponent = -arg.expr.value
        else:
            # Right operand not an int literal or a negated literal -- give up.
            return ctx.default_return_type
        if exponent >= 0:
            return ctx.api.named_generic_type("builtins.int", [])
        else:
            return ctx.api.named_generic_type("builtins.float", [])
    return ctx.default_return_type

