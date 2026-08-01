
def _match_second_order_type(A1, A0, t, b=None):
    r"""
    Works only for second order system in its canonical form.

    Type 0: Constant coefficient matrix, can be simply solved by
            introducing dummy variables.
    Type 1: When the substitution: $U = t*X' - X$ works for reducing
            the second order system to first order system.
    Type 2: When the system is of the form: $poly * X'' = A*X$ where
            $poly$ is square of a quadratic polynomial with respect to
            *t* and $A$ is a constant coefficient matrix.

    """
    match = {"type_of_equation": "type0"}
    n = A1.shape[0]

    if _matrix_is_constant(A1, t) and _matrix_is_constant(A0, t):
        return match

    if (A1 + A0*t).applyfunc(expand_mul).is_zero_matrix:
        match.update({"type_of_equation": "type1", "A1": A1})

    elif A1.is_zero_matrix and (b is None or b.is_zero_matrix):
        is_type2, term = _is_second_order_type2(A0, t)
        if is_type2:
            a, b, c = _get_poly_coeffs(Poly(term, t), 2)
            A = (A0*(term**2).expand()).applyfunc(ratsimp) + (b**2/4 - a*c)*eye(n, n)
            tau = integrate(1/term, t)
            t_ = Symbol("{}_".format(t))
            match.update({"type_of_equation": "type2", "A0": A,
                          "g(t)": sqrt(term), "tau": tau, "is_transformed": True,
                          "t_": t_})

    return match

