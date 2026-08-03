from typing import Any

def _factor_system_poly_from_expr(
        eqs: Sequence[Expr | complex], gens: Sequence[Expr], **kwargs: Any
) -> list[list[Poly]]:
    """
    Convert expressions to polynomials and factor the system.

    Takes a sequence of expressions, converts them to
    polynomials, and factors the resulting system. Handles both regular
    polynomial systems and purely numerical cases.
    """
    try:
        polys, opts = parallel_poly_from_expr(eqs, *gens, **kwargs)
        only_numbers = False
    except (GeneratorsNeeded, PolificationFailed):
        _u = Dummy('u')
        polys, opts = parallel_poly_from_expr(eqs, [_u], **kwargs)
        assert opts['domain'].is_Numerical
        only_numbers = True

    if only_numbers:
        return [[]] if all(p == 0 for p in polys) else []

    return factor_system_poly(polys)

