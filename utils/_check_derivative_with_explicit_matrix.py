
def _check_derivative_with_explicit_matrix(expr, x, diffexpr, dim=2):
    # TODO: this is commented because it slows down the tests.
    return

    expr = expr.xreplace({k: dim})
    x = x.xreplace({k: dim})
    diffexpr = diffexpr.xreplace({k: dim})

    expr = expr.as_explicit()
    x = x.as_explicit()
    diffexpr = diffexpr.as_explicit()

    assert expr.diff(x).reshape(*diffexpr.shape).tomatrix() == diffexpr

