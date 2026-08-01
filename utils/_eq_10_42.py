
def _eq_10_42(lam_1, lam_2, t_12):
    """
    Equation (10.42) of Functions of Matrices: Theory and Computation.

    Notes
    -----
    This is a helper function for _fragment_2_1 of expm_2009.
    Equation (10.42) is on page 251 in the section on Schur algorithms.
    In particular, section 10.4.3 explains the Schur-Parlett algorithm.
    expm([[lam_1, t_12], [0, lam_1])
    =
    [[exp(lam_1), t_12*exp((lam_1 + lam_2)/2)*sinch((lam_1 - lam_2)/2)],
    [0, exp(lam_2)]
    """

    # The plain formula t_12 * (exp(lam_2) - exp(lam_2)) / (lam_2 - lam_1)
    # apparently suffers from cancellation, according to Higham's textbook.
    # A nice implementation of sinch, defined as sinh(x)/x,
    # will apparently work around the cancellation.
    a = 0.5 * (lam_1 + lam_2)
    b = 0.5 * (lam_1 - lam_2)
    return t_12 * _exp_sinch(a, b)

