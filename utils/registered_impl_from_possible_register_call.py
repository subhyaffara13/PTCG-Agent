
def registered_impl_from_possible_register_call(
    expr: MemberExpr, dispatch_type: TypeInfo
) -> RegisteredImpl | None:
    if expr.name == "register" and isinstance(expr.expr, NameExpr):
        node = expr.expr.node
        if isinstance(node, Decorator):
            return RegisteredImpl(node.func, dispatch_type)
    return None

