
def estimate_smallest_singular_value(U):
    """Given upper triangular matrix ``U`` estimate the smallest singular
    value and the correspondent right singular vector in O(n**2) operations.

    Parameters
    ----------
    U : ndarray
        Square upper triangular matrix.

    Returns
    -------
    s_min : float
        Estimated smallest singular value of the provided matrix.
    z_min : ndarray
        Estimated right singular vector.

    Notes
    -----
    The procedure is based on [1]_ and is done in two steps. First, it finds
    a vector ``e`` with components selected from {+1, -1} such that the
    solution ``w`` from the system ``U.T w = e`` is as large as possible.
    Next it estimate ``U v = w``. The smallest singular value is close
    to ``norm(w)/norm(v)`` and the right singular vector is close
    to ``v/norm(v)``.

    The estimation will be better more ill-conditioned is the matrix.

    References
    ----------
    .. [1] Cline, A. K., Moler, C. B., Stewart, G. W., Wilkinson, J. H.
           An estimate for the condition number of a matrix.  1979.
           SIAM Journal on Numerical Analysis, 16(2), 368-375.
    """

    U = np.atleast_2d(U)
    m, n = U.shape

    if m != n:
        raise ValueError("A square triangular matrix should be provided.")

    # A vector `e` with components selected from {+1, -1}
    # is selected so that the solution `w` to the system
    # `U.T w = e` is as large as possible. Implementation
    # based on algorithm 3.5.1, p. 142, from reference [2]
    # adapted for lower triangular matrix.

    p = np.zeros(n)
    w = np.empty(n)

    # Implemented according to:  Golub, G. H., Van Loan, C. F. (2013).
    # "Matrix computations". Forth Edition. JHU press. pp. 140-142.
    for k in range(n):
        wp = (1-p[k]) / U.T[k, k]
        wm = (-1-p[k]) / U.T[k, k]
        pp = p[k+1:] + U.T[k+1:, k]*wp
        pm = p[k+1:] + U.T[k+1:, k]*wm

        if abs(wp) + norm(pp, 1) >= abs(wm) + norm(pm, 1):
            w[k] = wp
            p[k+1:] = pp
        else:
            w[k] = wm
            p[k+1:] = pm

    # The system `U v = w` is solved using backward substitution.
    v = solve_triangular(U, w)

    v_norm = norm(v)
    w_norm = norm(w)

    # Smallest singular value
    s_min = w_norm / v_norm

    # Associated vector
    z_min = v / v_norm

    return s_min, z_min

