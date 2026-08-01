
def _first_order_type5_6_subs(A, t, b=None):
    match = {}

    factor_terms = _factor_matrix(A, t)
    is_homogeneous = b is None or b.is_zero_matrix

    if factor_terms is not None:
        t_ = Symbol("{}_".format(t))
        F_t = integrate(factor_terms[0], t)
        inverse = solveset(Eq(t_, F_t), t)

        # Note: A simple way to check if a function is invertible
        # or not.
        if isinstance(inverse, FiniteSet) and not inverse.has(Piecewise)\
            and len(inverse) == 1:

            A = factor_terms[1]
            if not is_homogeneous:
                b = b / factor_terms[0]
                b = b.subs(t, list(inverse)[0])
            type = "type{}".format(5 + (not is_homogeneous))
            match.update({'func_coeff': A, 'tau': F_t,
                          't_': t_, 'type_of_equation': type, 'rhs': b})

    return match

