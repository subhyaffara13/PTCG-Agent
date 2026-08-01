
def stirling2(N, K, *, exact=False):
    r"""Generate Stirling number(s) of the second kind.

    Stirling numbers of the second kind count the number of ways to
    partition a set with N elements into K non-empty subsets.

    The values this function returns are calculated using a dynamic
    program which avoids redundant computation across the subproblems
    in the solution. For array-like input, this implementation also
    avoids redundant computation across the different Stirling number
    calculations.

    The numbers are sometimes denoted

    .. math::

        {N \brace{K}}

    see [1]_ for details. This is often expressed-verbally-as
    "N subset K".

    Parameters
    ----------
    N : int, ndarray
        Number of things.
    K : int, ndarray
        Number of non-empty subsets taken.
    exact : bool, optional
        Uses dynamic programming (DP) with floating point
        numbers for smaller arrays and uses a second order approximation due to
        Temme for larger entries  of `N` and `K` that allows trading speed for
        accuracy. See [2]_ for a description. Temme approximation is used for
        values ``n>50``. The max error from the DP has max relative error
        ``4.5*10^-16`` for ``n<=50`` and the max error from the Temme approximation
        has max relative error ``5*10^-5`` for ``51 <= n < 70`` and
        ``9*10^-6`` for ``70 <= n < 101``. Note that these max relative errors will
        decrease further as `n` increases.

    Returns
    -------
    val : int, float, ndarray
        The number of partitions.

    See Also
    --------
    comb : The number of combinations of N things taken k at a time.

    Notes
    -----
    - If N < 0, or K < 0, then 0 is returned.
    - If K > N, then 0 is returned.

    The output type will always be `int` or ndarray of `object`.
    The input must contain either numpy or python integers otherwise a
    TypeError is raised.

    References
    ----------
    .. [1] R. L. Graham, D. E. Knuth and O. Patashnik, "Concrete
        Mathematics: A Foundation for Computer Science," Addison-Wesley
        Publishing Company, Boston, 1989. Chapter 6, page 258.

    .. [2] Temme, Nico M. "Asymptotic estimates of Stirling numbers."
        Studies in Applied Mathematics 89.3 (1993): 233-243.

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.special import stirling2
    >>> k = np.array([3, -1, 3])
    >>> n = np.array([10, 10, 9])
    >>> stirling2(n, k)
    array([9330.0, 0.0, 3025.0])

    """
    output_is_scalar = np.isscalar(N) and np.isscalar(K)
    # make a min-heap of unique (n,k) pairs
    N, K = asarray(N), asarray(K)
    if not np.issubdtype(N.dtype, np.integer):
        raise TypeError("Argument `N` must contain only integers")
    if not np.issubdtype(K.dtype, np.integer):
        raise TypeError("Argument `K` must contain only integers")
    if not exact:
        # NOTE: here we allow np.uint via casting to double types prior to
        # passing to private ufunc dispatcher. All dispatched functions
        # take double type for (n,k) arguments and return double.
        return _stirling2_inexact(N.astype(float), K.astype(float))
    nk_pairs = list(
        set([(n.take(0), k.take(0))
             for n, k in np.nditer([N, K], ['refs_ok'])])
    )
    heapify(nk_pairs)
    # base mapping for small values
    snsk_vals = defaultdict(int)
    for pair in [(0, 0), (1, 1), (2, 1), (2, 2)]:
        snsk_vals[pair] = 1
    # for each pair in the min-heap, calculate the value, store for later
    n_old, n_row = 2, [0, 1, 1]
    while nk_pairs:
        n, k = heappop(nk_pairs)
        if n < 2 or k > n or k <= 0:
            continue
        elif k == n or k == 1:
            snsk_vals[(n, k)] = 1
            continue
        elif n != n_old:
            num_iters = n - n_old
            while num_iters > 0:
                n_row.append(1)
                # traverse from back to remove second row
                for j in range(len(n_row)-2, 1, -1):
                    n_row[j] = n_row[j]*j + n_row[j-1]
                num_iters -= 1
            snsk_vals[(n, k)] = n_row[k]
        else:
            snsk_vals[(n, k)] = n_row[k]
        n_old, n_row = n, n_row
    out_types = [object, object, object] if exact else [float, float, float]
    # for each pair in the map, fetch the value, and populate the array
    it = np.nditer(
        [N, K, None],
        ['buffered', 'refs_ok'],
        [['readonly'], ['readonly'], ['writeonly', 'allocate']],
        op_dtypes=out_types,
    )
    with it:
        while not it.finished:
            it[2] = snsk_vals[(int(it[0]), int(it[1]))]
            it.iternext()
        output = it.operands[2]
        # If N and K were both scalars, convert output to scalar.
        if output_is_scalar:
            output = output.take(0)
    return output


def stirling2(ctx, n, k, exact=False):
    v = ctx._stirling2(int(n), int(k))
    if exact:
        return int(v)
    else:
        return ctx.mpf(v)


def stirling2(n, k):
    """
    Stirling number of the second kind.
    """
    if n < 0 or k < 0:
        raise ValueError
    if k >= n:
        return MPZ(n == k)
    if k <= 1:
        return MPZ(k == 1)
    s = MPZ_ZERO
    t = MPZ_ONE
    for j in xrange(k+1):
        if (k + j) & 1:
            s -= t * MPZ(j)**n
        else:
            s += t * MPZ(j)**n
        t = t * (k - j) // (j + 1)
    return s // ifac(k)

