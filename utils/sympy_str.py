
def sympy_str(expr: sympy.Expr) -> str:
    """
    Normal sympy str is very slow, this is a lot faster.  The result are
    somewhat worse, as it doesn't do as much simplification.  So don't
    use this for final codegen.
    """

    def is_neg_lead(expr: sympy.Expr) -> bool:
        return (
            isinstance(expr, sympy.Mul) and len(expr.args) == 2 and expr.args[0] == -1
        )

    def sympy_str_add(expr: sympy.Expr) -> str:
        if isinstance(expr, sympy.Add):
            # Special case 'a - b'. Note that 'a - b - c' will still appear as
            # 'a + -1 * b + -1 * c'.
            if len(expr.args) == 2 and is_neg_lead(expr.args[1]):
                return f"{sympy_str_mul(expr.args[0])} - {sympy_str_mul(expr.args[1].args[1])}"
            else:
                return " + ".join(map(sympy_str_mul, expr.args))
        else:
            return sympy_str_mul(expr)

    def sympy_str_mul(expr: sympy.Expr) -> str:
        if isinstance(expr, sympy.Mul):
            if is_neg_lead(expr):
                # Special case '-a'. Note that 'a * -b' will still appear as
                # '-1 * a * b'.
                return f"-{sympy_str_atom(expr.args[1])}"
            else:
                return " * ".join(map(sympy_str_atom, expr.args))
        else:
            return sympy_str_atom(expr)

    def sympy_str_atom(expr: sympy.Expr) -> str:
        if isinstance(expr, sympy.Symbol):
            return expr.name
        elif isinstance(expr, (sympy.Add, sympy.Mul)):
            return f"({sympy_str_add(expr)})"
        elif isinstance(expr, (ModularIndexing, CleanDiv, FloorDiv, Identity)):
            return f"{expr.func.__name__}({', '.join(map(sympy_str, expr.args))})"
        else:
            return str(expr)

    return sympy_str_add(expr)

