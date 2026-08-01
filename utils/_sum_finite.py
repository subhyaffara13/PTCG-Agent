
def _sum_finite(x):
    """
    For a 1D array x, return a tuple containing the sum of the
    finite values of x and the number of nonfinite values.

    This is a utility function used when evaluating the negative
    loglikelihood for a distribution and an array of samples.

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.stats._distn_infrastructure import _sum_finite
    >>> tot, nbad = _sum_finite(np.array([-2, -np.inf, 5, 1]))
    >>> tot
    4.0
    >>> nbad
    1
    """
    finite_x = np.isfinite(x)
    bad_count = finite_x.size - np.count_nonzero(finite_x)
    return np.sum(x[finite_x]), bad_count

