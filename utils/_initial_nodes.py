
def _initial_nodes(n):
    """Initial guesses for the Hermite roots

    Computes an initial approximation to the non-negative
    roots :math:`x_k` of the Hermite polynomial :math:`H_n`
    of order :math:`n`. The Tricomi and Gatteschi initial
    guesses are used in the region where they are accurate.

    Parameters
    ----------
    n : int
        Quadrature order

    Returns
    -------
    xk : ndarray
        Approximate roots

    See Also
    --------
    roots_hermite_asy
    """
    # Turnover point
    # linear polynomial fit to error of 10, 25, 40, ..., 1000 point rules
    fit = 0.49082003*n - 4.37859653
    turnover = around(fit).astype(int)
    # Compute all approximations
    ia = arange(1, int(floor(n*0.5)+1))
    ib = ia[::-1]
    xasq = _initial_nodes_a(n, ia[:turnover+1])
    xbsq = _initial_nodes_b(n, ib[turnover+1:])
    # Combine
    iv = sqrt(hstack([xasq, xbsq]))
    # Central node is always zero
    if n % 2 == 1:
        iv = hstack([0.0, iv])
    return iv

