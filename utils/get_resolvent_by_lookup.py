
def get_resolvent_by_lookup(T, number):
    """
    Use the lookup table, to return a resolvent (as dup) for a given
    polynomial *T*.

    Parameters
    ==========

    T : Poly
        The polynomial whose resolvent is needed

    number : int
        For some degrees, there are multiple resolvents.
        Use this to indicate which one you want.

    Returns
    =======

    dup

    """
    from sympy.polys.numberfields.resolvent_lookup import resolvent_coeff_lambdas
    degree = T.degree()
    L = resolvent_coeff_lambdas[(degree, number)]
    T_coeffs = T.rep.to_list()[1:]
    return [ZZ(1)] + [c(*T_coeffs) for c in L]

