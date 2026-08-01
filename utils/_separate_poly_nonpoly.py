
def _separate_poly_nonpoly(system, symbols):
    polys = []
    polys_expr = []
    nonpolys = []
    # unrad_changed stores a list of expressions containing
    # radicals that were processed using unrad
    # this is useful if solutions need to be checked later.
    unrad_changed = []
    denominators = set()
    poly = None
    for eq in system:
        # Store denom expressions that contain symbols
        denominators.update(_simple_dens(eq, symbols))
        # Convert equality to expression
        if isinstance(eq, Eq):
            eq = eq.lhs - eq.rhs
        # try to remove sqrt and rational power
        without_radicals = unrad(simplify(eq), *symbols)
        if without_radicals:
            unrad_changed.append(eq)
            eq_unrad, cov = without_radicals
            if not cov:
                eq = eq_unrad
        if isinstance(eq, Expr):
            eq = eq.as_numer_denom()[0]
            poly = eq.as_poly(*symbols, extension=True)
        elif simplify(eq).is_number:
            continue
        if poly is not None:
            polys.append(poly)
            polys_expr.append(poly.as_expr())
        else:
            nonpolys.append(eq)
    return polys, polys_expr, nonpolys, denominators, unrad_changed

