
def _zseries_mul(z1, z2):
    """Multiply two z-series.

    Multiply two z-series to produce a z-series.

    Parameters
    ----------
    z1, z2 : 1-D ndarray
        The arrays must be 1-D but this is not checked.

    Returns
    -------
    product : 1-D ndarray
        The product z-series.

    Notes
    -----
    This is simply convolution. If symmetric/anti-symmetric z-series are
    denoted by S/A then the following rules apply:

    S*S, A*A -> S
    S*A, A*S -> A

    """
    return np.convolve(z1, z2)

