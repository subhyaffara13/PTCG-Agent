
def apply_dunder_specialization(
    builder: IRBuilder,
    base_expr: Expression,
    args: list[Expression],
    name: str,
    ctx_expr: Expression,
) -> Value | None:
    """Invoke the DunderSpecializer callback if one has been registered.

    Args:
        builder: The IR builder
        base_expr: The base expression (target object)
        args: List of argument expressions (positional arguments to the dunder)
        name: The dunder method name (e.g., "__getitem__")
        ctx_expr: The context expression for error reporting (e.g., IndexExpr)

    Returns:
        The specialized value, or None if no specialization was found.
    """
    base_type = builder.node_type(base_expr)

    # Check if there's a specializer for this dunder method and type
    if (name, base_type) in dunder_specializers:
        for specializer in dunder_specializers[name, base_type]:
            val = specializer(builder, base_expr, args, ctx_expr)
            if val is not None:
                return val
    return None

