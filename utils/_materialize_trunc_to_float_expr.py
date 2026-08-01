
def _materialize_trunc_to_float_expr(
    expr: sympy.Expr, dtype: torch.dtype
) -> sympy.Expr:
    if not dtype.is_floating_point or not expr.has(TruncToInt):
        return expr

    # Preserve float truncation semantics when materializing symbolic scalars
    # into floating tensors. Casting to the kernel index dtype first can
    # overflow before the requested floating-point conversion happens. Only
    # rewrite truncations that are already participating in floating-point
    # computation; integer subexpressions and predicates must keep exact
    # integer semantics until the final materialization cast.
    if expr.func is TruncToInt:
        return TruncToFloat(*expr.args)

    def is_predicate_expr(node: sympy.Basic) -> bool:
        return bool(
            getattr(node, "is_Boolean", False) or getattr(node, "is_Relational", False)
        )

    def rewrite_float_subexpr(node: sympy.Expr) -> sympy.Expr:
        if not node.has(TruncToInt):
            return node
        if node.func is TruncToInt:
            return TruncToFloat(*node.args)
        if is_predicate_expr(node) or node.is_integer:
            return node

        new_args = tuple(
            rewrite_float_subexpr(arg)
            if isinstance(arg, sympy.Expr) and not is_predicate_expr(arg)
            else arg
            for arg in node.args
        )
        if new_args == node.args:
            return node
        return node.func(*new_args)

    return rewrite_float_subexpr(expr)

