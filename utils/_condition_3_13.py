
def _condition_3_13(A_1_norm, n0, m_max, ell):
    """
    A helper function for the _expm_multiply_* functions.

    Parameters
    ----------
    A_1_norm : float
        The precomputed 1-norm of A.
    n0 : int
        Number of columns in the _expm_multiply_* B matrix.
    m_max : int
        A value related to a bound.
    ell : int
        The number of columns used in the 1-norm approximation.
        This is usually taken to be small, maybe between 1 and 5.

    Returns
    -------
    value : bool
        Indicates whether or not the condition has been met.

    Notes
    -----
    This is condition (3.13) in Al-Mohy and Higham (2011).

    """

    # This is the rhs of equation (3.12).
    p_max = _compute_p_max(m_max)
    a = 2 * ell * p_max * (p_max + 3)

    # Evaluate the condition (3.13).
    b = _theta[m_max] / float(n0 * m_max)
    return A_1_norm <= a * b

