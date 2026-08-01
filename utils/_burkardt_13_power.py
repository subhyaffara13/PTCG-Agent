
def _burkardt_13_power(n, p):
    """
    A helper function for testing matrix functions.

    Parameters
    ----------
    n : int greater than 1
        Order of the square matrix to be returned.
    p : non-negative integer
        Power of the matrix.

    Returns
    -------
    out : ndarray representing a square matrix
        A Forsythe matrix of order n, raised to the power p.

    """
    # Input validation.
    if n != int(n) or n < 2:
        raise ValueError('n must be an integer greater than 1')
    n = int(n)
    if p != int(p) or p < 0:
        raise ValueError('p must be a non-negative integer')
    p = int(p)

    # Construct the matrix explicitly.
    a, b = divmod(p, n)
    large = np.power(10.0, -n*a)
    small = large * np.power(10.0, -n)
    return np.diag([large]*(n-b), b) + np.diag([small]*b, b-n)

