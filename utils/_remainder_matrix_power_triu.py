
def _remainder_matrix_power_triu(T, t):
    """
    Compute a fractional power of an upper triangular matrix.

    The fractional power is restricted to fractions -1 < t < 1.
    This uses algorithm (3.1) of [1]_.
    The Pade approximation itself uses algorithm (4.1) of [2]_.

    Parameters
    ----------
    T : (N, N) array_like
        Upper triangular matrix whose fractional power to evaluate.
    t : float
        Fractional power between -1 and 1 exclusive.

    Returns
    -------
    X : (N, N) array_like
        The fractional power of the matrix.

    References
    ----------
    .. [1] Nicholas J. Higham and Lijing Lin (2013)
           "An Improved Schur-Pade Algorithm for Fractional Powers
           of a Matrix and their Frechet Derivatives."

    .. [2] Nicholas J. Higham and Lijing lin (2011)
           "A Schur-Pade Algorithm for Fractional Powers of a Matrix."
           SIAM Journal on Matrix Analysis and Applications,
           32 (3). pp. 1056-1078. ISSN 0895-4798

    """
    m_to_theta = {
            1: 1.51e-5,
            2: 2.24e-3,
            3: 1.88e-2,
            4: 6.04e-2,
            5: 1.24e-1,
            6: 2.00e-1,
            7: 2.79e-1,
            }
    n, n = T.shape
    T0 = T
    T0_diag = np.diag(T0)
    if np.array_equal(T0, np.diag(T0_diag)):
        U = np.diag(T0_diag ** t)
    else:
        R, s, m = _inverse_squaring_helper(T0, m_to_theta)

        # Evaluate the Pade approximation.
        # Note that this function expects the negative of the matrix
        # returned by the inverse squaring helper.
        U = _fractional_power_pade(-R, t, m)

        # Undo the inverse scaling and squaring.
        # Be less clever about this
        # if the principal branch does not exist at T0;
        # this happens when a diagonal entry of T0
        # is negative with imaginary part 0.
        eivals = np.diag(T0)
        has_principal_branch = all(x.real > 0 or x.imag != 0 for x in eivals)
        for i in range(s, -1, -1):
            if i < s:
                U = U.dot(U)
            else:
                if has_principal_branch:
                    p = t * np.exp2(-i)
                    U[np.diag_indices(n)] = T0_diag ** p
                    for j in range(n-1):
                        l1 = T0[j, j]
                        l2 = T0[j+1, j+1]
                        t12 = T0[j, j+1]
                        f12 = _fractional_power_superdiag_entry(l1, l2, t12, p)
                        U[j, j+1] = f12
    if not np.array_equal(U, np.triu(U)):
        raise Exception('U is not upper triangular')
    return U

