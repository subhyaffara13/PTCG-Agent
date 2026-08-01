
def perm(N, k, exact=False):
    """Permutations of N things taken k at a time, i.e., k-permutations of N.

    It's also known as "partial permutations".

    Parameters
    ----------
    N : int, ndarray
        Number of things.
    k : int, ndarray
        Number of elements taken.
    exact : bool, optional
        If ``True``, calculate the answer exactly using long integer arithmetic (`N`
        and `k` must be scalar integers). If ``False``, a floating point approximation
        is calculated (more rapidly) using `poch`. Default is ``False``.

    Returns
    -------
    val : int, ndarray
        The number of k-permutations of N.

    Notes
    -----
    - Array arguments accepted only for exact=False case.
    - If k > N, N < 0, or k < 0, then a 0 is returned.

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.special import perm
    >>> k = np.array([3, 4])
    >>> n = np.array([10, 10])
    >>> perm(n, k)
    array([  720.,  5040.])
    >>> perm(10, 3, exact=True)
    720

    """
    if exact:
        N = np.squeeze(N)[()]  # for backward compatibility (accepted size 1 arrays)
        k = np.squeeze(k)[()]
        if not (isscalar(N) and isscalar(k)):
            raise ValueError("`N` and `k` must be scalar integers with `exact=True`.")

        floor_N, floor_k = int(N), int(k)
        non_integral = not (floor_N == N and floor_k == k)
        if non_integral:
            raise ValueError("Non-integer `N` and `k` with `exact=True` is not "
                             "supported.")

        if (k > N) or (N < 0) or (k < 0):
            return 0

        val = 1
        for i in range(floor_N - floor_k + 1, floor_N + 1):
            val *= i
        return val
    else:
        k, N = asarray(k), asarray(N)
        cond = (k <= N) & (N >= 0) & (k >= 0)
        vals = poch(N - k + 1, k)
        if isinstance(vals, np.ndarray):
            vals[~cond] = 0
        elif not cond:
            vals = np.float64(0)
        return vals

