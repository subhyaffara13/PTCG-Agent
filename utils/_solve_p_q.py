
def _solve_P_Q(U, V, structure=None):
    """
    A helper function for expm_2009.

    Parameters
    ----------
    U : ndarray
        Pade numerator.
    V : ndarray
        Pade denominator.
    structure : str, optional
        A string describing the structure of both matrices `U` and `V`.
        Only `upper_triangular` is currently supported.

    Notes
    -----
    The `structure` argument is inspired by similar args
    for theano and cvxopt functions.

    """
    P = U + V
    Q = -U + V
    if issparse(U) or is_pydata_spmatrix(U):
        return spsolve(Q, P)
    elif structure is None:
        return solve(Q, P)
    elif structure == UPPER_TRIANGULAR:
        return solve_triangular(Q, P)
    else:
        raise ValueError('unsupported matrix structure: ' + str(structure))


def _solve_P_Q(P: ArrayLike, Q: ArrayLike, upper_triangular: bool = False) -> Array:
  if upper_triangular:
    return solve_triangular(Q, P)
  else:
    return jnp_linalg.solve(Q, P)

