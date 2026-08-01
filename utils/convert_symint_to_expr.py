
def convert_symint_to_expr(val: int | torch.SymInt) -> int | sympy.Expr:
    """
    Convert SymInt to sympy.Expr, leave int as is.

    Unlike sympy.sympify() which converts int to sympy.Integer,
    this function preserves int as int and only converts SymInt to Expr.
    """
    if isinstance(val, torch.SymInt):
        return val.node.expr
    return val

