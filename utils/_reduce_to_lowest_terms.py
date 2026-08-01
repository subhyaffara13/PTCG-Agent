
def _reduce_to_lowest_terms(expr: sympy.Expr) -> sympy.Expr:
    """
    Eliminates any integer factor from a given expression.
    E.g., 6x + 4y reduces to 3x + 2y.

    Useful when an expression is == or != to 0.
    """

    def integer_coefficient(x: sympy.Expr) -> int:
        if x.is_Integer:
            return abs(int(x))
        elif x.is_Mul:
            # If one of the args of a Mul is an Integer, it is the
            # first arg. eg: args(2*x*3*y) == (6, x, y)
            return abs(int(x.args[0])) if x.args[0].is_Integer else 1  # type: ignore[call-overload]
        else:
            return 1

    def div_by_factor(x: sympy.Expr, factor: int) -> sympy.Expr:
        if x.is_Integer:
            return x / factor
        elif x.is_Mul:
            if x.args[0] != factor:
                args = [x.args[0] / sympy.Integer(factor), *x.args[1:]]
            else:
                # Mul._from_args require a canonical list of args
                # so we remove the first arg (x.args[0] / factor) if it was 1
                args = list(x.args[1:])
            return _sympy_from_args(sympy.Mul, args, is_commutative=x.is_commutative)
        else:
            raise AssertionError(f"illegal arg to div_by_factor: {x}")

    if expr.is_Add:
        atoms = cast(Sequence[sympy.Expr], expr.args)
        factor = functools.reduce(math.gcd, map(integer_coefficient, atoms))
        if factor == 1:
            return expr
        # pyrefly: ignore [bad-argument-type]
        atoms = [div_by_factor(x, factor) for x in atoms]
        return _sympy_from_args(
            sympy.Add, atoms, sort=True, is_commutative=expr.is_commutative
        )
    elif expr.is_Integer:
        return S.One
    elif expr.is_Mul:
        return div_by_factor(expr, integer_coefficient(expr))
    return expr

