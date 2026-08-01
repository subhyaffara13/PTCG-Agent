
def _is_type1(scc, t):
    eqs, funcs = scc

    try:
        (A1, A0), b = linear_ode_to_matrix(eqs, funcs, t, 1)
    except (ODENonlinearError, ODEOrderError):
        return False

    if _matrix_is_constant(A0, t) and b.is_zero_matrix:
        return True

    return False

