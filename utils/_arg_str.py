
def _arg_str(a: object) -> str:
    if isinstance(a, sympy.Expr):
        return sympy_str(a)
    return str(a)

