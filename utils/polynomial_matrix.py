
def polynomial_matrix(x, powers, xp):
    return _pythran_polynomial_matrix(x, powers)


def polynomial_matrix(x, powers, xp):
    """Evaluate monomials, with exponents from `powers`, at `x`."""
    return xp.prod(x[:, None, :] ** powers, axis=-1)

