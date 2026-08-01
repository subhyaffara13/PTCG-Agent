
def _coeff_of_divided_diff(x):
    """
    Returns the coefficients of the divided difference.

    Parameters
    ----------
    x : array, shape (n,)
        Array which is used for the computation of divided difference.

    Returns
    -------
    res : array_like, shape (n,)
        Coefficients of the divided difference.

    Notes
    -----
    Vector ``x`` should have unique elements, otherwise an error division by
    zero might be raised.

    No checks are performed.

    """
    n = x.shape[0]
    res = np.zeros(n)
    for i in range(n):
        pp = 1.
        for k in range(n):
            if k != i:
                pp *= (x[i] - x[k])
        res[i] = 1. / pp
    return res

