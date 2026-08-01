
def is_borrow_friendly_expr(self: IRBuilder, expr: Expression) -> bool:
    """Can the result of the expression borrowed temporarily?

    Borrowing means keeping a reference without incrementing the reference count.
    """
    if isinstance(expr, (IntExpr, FloatExpr, StrExpr, BytesExpr)):
        # Literals are immortal and can always be borrowed
        return True
    if (
        isinstance(expr, (UnaryExpr, OpExpr, NameExpr, MemberExpr))
        and constant_fold_expr(self, expr) is not None
    ):
        # Literal expressions are similar to literals
        return True
    if isinstance(expr, NameExpr):
        if isinstance(expr.node, Var) and expr.kind == LDEF:
            # Local variable reference can be borrowed
            return True
    if isinstance(expr, MemberExpr) and self.is_native_attr_ref(expr):
        return True
    return False

