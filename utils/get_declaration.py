
def get_declaration(expr: BindableExpression) -> Type | None:
    """Get the declared or inferred type of a RefExpr expression.

    Return None if there is no type or the expression is not a RefExpr.
    This can return None if the type hasn't been inferred yet.
    """
    if isinstance(expr, RefExpr):
        if isinstance(expr.node, Var):
            type = expr.node.type
            if not isinstance(get_proper_type(type), PartialType):
                return type
        elif isinstance(expr.node, TypeInfo):
            return TypeType(fill_typevars_with_any(expr.node))
    return None

