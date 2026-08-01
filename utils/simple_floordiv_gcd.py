
def simple_floordiv_gcd(p: sympy.Basic, q: sympy.Basic) -> sympy.Basic:
    """
    Fast path for sympy.gcd, using a simple factoring strategy.

    We try to rewrite p and q in the form n*e*p1 + n*e*p2 and n*e*q0,
    where n is the greatest common integer factor and e is the largest
    syntactic common factor (i.e., common sub-expression) in p and q.
    Then the gcd returned is n*e, cancelling which we would be left with
    p1 + p2 and q0.

    Note that further factoring of p1 + p2 and q0 might be possible with
    sympy.factor (which uses domain-specific theories). E.g., we are unable
    to find that x*y + x + y + 1 is divisible by x + 1. More generally,
    when q is of the form q1 + q2 (instead of being already factored) it
    might be necessary to fall back on sympy.gcd.
    """

    def integer_coefficient(x: sympy.Basic) -> int:
        integer_coefficients: list[int] = [
            abs(int(arg))
            for arg in sympy.Mul.make_args(x)
            if isinstance(arg, (int, sympy.Integer))
        ]
        return math.prod(integer_coefficients)

    def integer_factor(expr: sympy.Basic) -> int:
        integer_factors: Iterable[int] = map(
            integer_coefficient, sympy.Add.make_args(expr)
        )
        return functools.reduce(math.gcd, integer_factors)

    gcd: int = math.gcd(integer_factor(p), integer_factor(q))
    p, q = p / gcd, q / gcd  # type: ignore[operator, assignment]  # remove in py3.12

    base_splits: list[tuple[sympy.Basic, ...]] = list(
        map(sympy.Mul.make_args, sympy.Add.make_args(p))
    )
    divisor_split: tuple[sympy.Basic, ...] = sympy.Mul.make_args(q)
    for x in divisor_split:
        if all(x in base_split for base_split in base_splits):
            gcd = gcd * x  # type: ignore[operator]  # remove in py3.12
    return gcd  # type: ignore[return-value]  # remove in py3.12

