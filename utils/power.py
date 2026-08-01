
def power(test, rvs, n_observations, *, significance=0.01, vectorized=None,
          n_resamples=10000, batch=None, kwargs=None):
    r"""Simulate the power of a hypothesis test under an alternative hypothesis.

    Parameters
    ----------
    test : callable
        Hypothesis test for which the power is to be simulated.
        `test` must be a callable that accepts a sample (e.g. ``test(sample)``)
        or ``len(rvs)`` separate samples (e.g. ``test(samples1, sample2)`` if
        `rvs` contains two callables and `n_observations` contains two values)
        and returns the p-value of the test.
        If `vectorized` is set to ``True``, `test` must also accept a keyword
        argument `axis` and be vectorized to perform the test along the
        provided `axis` of the samples.
        Any callable from `scipy.stats` with an `axis` argument that returns an
        object with a `pvalue` attribute is also acceptable.
    rvs : callable or tuple of callables
        A callable or sequence of callables that generate(s) random variates
        under the alternative hypothesis. Each element of `rvs` must accept
        keyword argument ``size`` (e.g. ``rvs(size=(m, n))``) and return an
        N-d array of that shape. If `rvs` is a sequence, the number of callables
        in `rvs` must match the number of elements of `n_observations`, i.e.
        ``len(rvs) == len(n_observations)``. If `rvs` is a single callable,
        `n_observations` is treated as a single element.
    n_observations : tuple of ints or tuple of int arrays
        If a sequence of ints, each is the sizes of a sample to be passed to `test`.
        If a sequence of integer arrays, the power is simulated for each
        set of corresponding sample sizes. See Examples.
    significance : float or array_like of floats, default: 0.01
        The threshold for significance; i.e., the p-value below which the
        hypothesis test results will be considered as evidence against the null
        hypothesis. Equivalently, the acceptable rate of Type I error under
        the null hypothesis. If an array, the power is simulated for each
        significance threshold.
    vectorized : bool, optional
        If `vectorized` is set to ``False``, `test` will not be passed keyword
        argument `axis` and is expected to perform the test only for 1D samples.
        If ``True``, `test` will be passed keyword argument `axis` and is
        expected to perform the test along `axis` when passed N-D sample arrays.
        If ``None`` (default), `vectorized` will be set ``True`` if ``axis`` is
        a parameter of `test`. Use of a vectorized test typically reduces
        computation time.
    n_resamples : int, default: 10000
        Number of samples drawn from each of the callables of `rvs`.
        Equivalently, the number tests performed under the alternative
        hypothesis to approximate the power.
    batch : int, optional
        The number of samples to process in each call to `test`. Memory usage is
        proportional to the product of `batch` and the largest sample size. Default
        is ``None``, in which case `batch` equals `n_resamples`.
    kwargs : dict, optional
        Keyword arguments to be passed to `rvs` and/or `test` callables.
        Introspection is used to determine which keyword arguments may be
        passed to each callable.
        The value corresponding with each keyword must be an array.
        Arrays must be broadcastable with one another and with each array in
        `n_observations`. The power is simulated for each set of corresponding
        sample sizes and arguments. See Examples.

    Returns
    -------
    res : PowerResult
        An object with attributes:

        power : float or ndarray
            The estimated power against the alternative.
        pvalues : ndarray
            The p-values observed under the alternative hypothesis.

    Notes
    -----
    The power is simulated as follows:

    - Draw many random samples (or sets of samples), each of the size(s)
      specified by `n_observations`, under the alternative specified by
      `rvs`.
    - For each sample (or set of samples), compute the p-value according to
      `test`. These p-values are recorded in the ``pvalues`` attribute of
      the result object.
    - Compute the proportion of p-values that are less than the `significance`
      level. This is the power recorded in the ``power`` attribute of the
      result object.

    Suppose that `significance` is an array with shape ``shape1``, the elements
    of `kwargs` and `n_observations` are mutually broadcastable to shape ``shape2``,
    and `test` returns an array of p-values of shape ``shape3``. Then the result
    object ``power`` attribute will be of shape ``shape1 + shape2 + shape3``, and
    the ``pvalues`` attribute will be of shape ``shape2 + shape3 + (n_resamples,)``.

    Examples
    --------
    Suppose we wish to simulate the power of the independent sample t-test
    under the following conditions:

    - The first sample has 10 observations drawn from a normal distribution
      with mean 0.
    - The second sample has 12 observations drawn from a normal distribution
      with mean 1.0.
    - The threshold on p-values for significance is 0.05.

    >>> import numpy as np
    >>> from scipy import stats
    >>> rng = np.random.default_rng(2549598345528)
    >>>
    >>> test = stats.ttest_ind
    >>> n_observations = (10, 12)
    >>> rvs1 = rng.normal
    >>> rvs2 = lambda size: rng.normal(loc=1, size=size)
    >>> rvs = (rvs1, rvs2)
    >>> res = stats.power(test, rvs, n_observations, significance=0.05)
    >>> res.power
    0.6116

    With samples of size 10 and 12, respectively, the power of the t-test
    with a significance threshold of 0.05 is approximately 60% under the chosen
    alternative. We can investigate the effect of sample size on the power
    by passing sample size arrays.

    >>> import matplotlib.pyplot as plt
    >>> nobs_x = np.arange(5, 21)
    >>> nobs_y = nobs_x
    >>> n_observations = (nobs_x, nobs_y)
    >>> res = stats.power(test, rvs, n_observations, significance=0.05)
    >>> ax = plt.subplot()
    >>> ax.plot(nobs_x, res.power)
    >>> ax.set_xlabel('Sample Size')
    >>> ax.set_ylabel('Simulated Power')
    >>> ax.set_title('Simulated Power of `ttest_ind` with Equal Sample Sizes')
    >>> plt.show()

    Alternatively, we can investigate the impact that effect size has on the power.
    In this case, the effect size is the location of the distribution underlying
    the second sample.

    >>> n_observations = (10, 12)
    >>> loc = np.linspace(0, 1, 20)
    >>> rvs2 = lambda size, loc: rng.normal(loc=loc, size=size)
    >>> rvs = (rvs1, rvs2)
    >>> res = stats.power(test, rvs, n_observations, significance=0.05,
    ...                   kwargs={'loc': loc})
    >>> ax = plt.subplot()
    >>> ax.plot(loc, res.power)
    >>> ax.set_xlabel('Effect Size')
    >>> ax.set_ylabel('Simulated Power')
    >>> ax.set_title('Simulated Power of `ttest_ind`, Varying Effect Size')
    >>> plt.show()

    We can also use `power` to estimate the Type I error rate (also referred to by the
    ambiguous term "size") of a test and assess whether it matches the nominal level.
    For example, the null hypothesis of `jarque_bera` is that the sample was drawn from
    a distribution with the same skewness and kurtosis as the normal distribution. To
    estimate the Type I error rate, we can consider the null hypothesis to be a true
    *alternative* hypothesis and calculate the power.

    >>> test = stats.jarque_bera
    >>> n_observations = 10
    >>> rvs = rng.normal
    >>> significance = np.linspace(0.0001, 0.1, 1000)
    >>> res = stats.power(test, rvs, n_observations, significance=significance)
    >>> size = res.power

    As shown below, the Type I error rate of the test is far below the nominal level
    for such a small sample, as mentioned in its documentation.

    >>> ax = plt.subplot()
    >>> ax.plot(significance, size)
    >>> ax.plot([0, 0.1], [0, 0.1], '--')
    >>> ax.set_xlabel('nominal significance level')
    >>> ax.set_ylabel('estimated test size (Type I error rate)')
    >>> ax.set_title('Estimated test size vs nominal significance level')
    >>> ax.set_aspect('equal', 'box')
    >>> ax.legend(('`ttest_1samp`', 'ideal test'))
    >>> plt.show()

    As one might expect from such a conservative test, the power is quite low with
    respect to some alternatives. For example, the power of the test under the
    alternative that the sample was drawn from the Laplace distribution may not
    be much greater than the Type I error rate.

    >>> rvs = rng.laplace
    >>> significance = np.linspace(0.0001, 0.1, 1000)
    >>> res = stats.power(test, rvs, n_observations, significance=0.05)
    >>> print(res.power)
    0.0587

    This is not a mistake in SciPy's implementation; it is simply due to the fact
    that the null distribution of the test statistic is derived under the assumption
    that the sample size is large (i.e. approaches infinity), and this asymptotic
    approximation is not accurate for small samples. In such cases, resampling
    and Monte Carlo methods (e.g. `permutation_test`, `goodness_of_fit`,
    `monte_carlo_test`) may be more appropriate.

    """
    tmp = _power_iv(rvs, test, n_observations, significance,
                    vectorized, n_resamples, batch, kwargs)
    (rvs, test, nobs, significance,
     vectorized, n_resamples, batch, args, kwds, shape, xp) = tmp

    batch_nominal = batch or n_resamples
    pvalues = []  # results of various nobs/kwargs combinations
    for i in range(nobs.shape[0]):
        nobs_i, args_i = nobs[i, ...], args[i, ...]
        kwargs_i = dict(zip(kwds, args_i))
        pvalues_i = []  # results of batches; fixed nobs/kwargs combination
        for k in range(0, n_resamples, batch_nominal):
            batch_actual = min(batch_nominal, n_resamples - k)
            resamples = [rvs_j(size=(batch_actual, int(nobs_ij)), **kwargs_i)
                         for rvs_j, nobs_ij in zip(rvs, nobs_i)]
            res = test(*resamples, **kwargs_i, axis=-1)
            p = getattr(res, 'pvalue', res)
            pvalues_i.append(p)
        # Concatenate results from batches
        pvalues_i = xp.concat(pvalues_i, axis=-1)
        pvalues.append(pvalues_i)
    # `test` can return result with array of p-values
    shape += pvalues_i.shape[:-1]
    # Concatenate results from various nobs/kwargs combinations
    pvalues = xp.concat(pvalues, axis=0)
    # nobs/kwargs arrays were raveled to single axis; unravel
    pvalues = xp.reshape(pvalues, shape + (-1,))
    if significance.ndim > 0:
        newdims = tuple(range(significance.ndim, pvalues.ndim + significance.ndim))
        significance = xpx.expand_dims(significance, axis=newdims)

    float_dtype = xp_result_type(significance, pvalues, xp=xp)
    powers = xp.mean(xp.astype(pvalues < significance, float_dtype), axis=-1)

    return PowerResult(power=powers, pvalues=pvalues)


def power(x, p):
    """
    Return x to the power p, (x**p).

    If `x` contains negative values, the output is converted to the
    complex domain.

    Parameters
    ----------
    x : array_like
        The input value(s).
    p : array_like of ints
        The power(s) to which `x` is raised. If `x` contains multiple values,
        `p` has to either be a scalar, or contain the same number of values
        as `x`. In the latter case, the result is
        ``x[0]**p[0], x[1]**p[1], ...``.

    Returns
    -------
    out : ndarray or scalar
        The result of ``x**p``. If `x` and `p` are scalars, so is `out`,
        otherwise an array is returned.

    See Also
    --------
    numpy.power

    Examples
    --------
    >>> import numpy as np
    >>> np.set_printoptions(precision=4)

    >>> np.emath.power(2, 2)
    4

    >>> np.emath.power([2, 4], 2)
    array([ 4, 16])

    >>> np.emath.power([2, 4], -2)
    array([0.25  ,  0.0625])

    >>> np.emath.power([-2, 4], 2)
    array([ 4.-0.j, 16.+0.j])

    >>> np.emath.power([2, 4], [2, 4])
    array([ 4, 256])

    """
    x = _fix_real_lt_zero(x)
    p = _fix_int_lt_zero(p)
    return nx.power(x, p)


def power(a, b, third=None):
    """
    Returns element-wise base array raised to power from second array.

    This is the masked array version of `numpy.power`. For details see
    `numpy.power`.

    See Also
    --------
    numpy.power

    Notes
    -----
    The *out* argument to `numpy.power` is not supported, `third` has to be
    None.

    Examples
    --------
    >>> import numpy as np
    >>> import numpy.ma as ma
    >>> x = [11.2, -3.973, 0.801, -1.41]
    >>> mask = [0, 0, 0, 1]
    >>> masked_x = ma.masked_array(x, mask)
    >>> masked_x
    masked_array(data=[11.2, -3.973, 0.801, --],
             mask=[False, False, False,  True],
       fill_value=1e+20)
    >>> ma.power(masked_x, 2)
    masked_array(data=[125.43999999999998, 15.784728999999999,
                   0.6416010000000001, --],
             mask=[False, False, False,  True],
       fill_value=1e+20)
    >>> y = [-0.5, 2, 0, 17]
    >>> masked_y = ma.masked_array(y, mask)
    >>> masked_y
    masked_array(data=[-0.5, 2.0, 0.0, --],
             mask=[False, False, False,  True],
       fill_value=1e+20)
    >>> ma.power(masked_x, masked_y)
    masked_array(data=[0.2988071523335984, 15.784728999999999, 1.0, --],
             mask=[False, False, False,  True],
       fill_value=1e+20)

    """
    if third is not None:
        raise MaskError("3-argument power not supported.")
    # Get the masks
    ma = getmask(a)
    mb = getmask(b)
    m = mask_or(ma, mb)
    # Get the rawdata
    fa = getdata(a)
    fb = getdata(b)
    # Get the type of the result (so that we preserve subclasses)
    if isinstance(a, MaskedArray):
        basetype = type(a)
    else:
        basetype = MaskedArray
    # Get the result and view it as a (subclass of) MaskedArray
    with np.errstate(divide='ignore', invalid='ignore'):
        result = np.where(m, fa, umath.power(fa, fb)).view(basetype)
    result._update_from(a)
    # Find where we're in trouble w/ NaNs and Infs
    invalid = np.logical_not(np.isfinite(result.view(ndarray)))
    # Add the initial mask
    if m is not nomask:
        if not result.ndim:
            return masked
        result._mask = np.logical_or(m, invalid)
    # Fix the invalid parts
    if invalid.any():
        if not result.ndim:
            return masked
        elif result._mask is nomask:
            result._mask = invalid
        result._data[invalid] = result.fill_value
    return result


def power(G, k):
    """Returns the specified power of a graph.

    The $k$th power of a simple graph $G$, denoted $G^k$, is a
    graph on the same set of nodes in which two distinct nodes $u$ and
    $v$ are adjacent in $G^k$ if and only if the shortest path
    distance between $u$ and $v$ in $G$ is at most $k$.

    Parameters
    ----------
    G : graph
        A NetworkX simple graph object.

    k : positive integer
        The power to which to raise the graph `G`.

    Returns
    -------
    NetworkX simple graph
        `G` to the power `k`.

    Raises
    ------
    ValueError
        If the exponent `k` is not positive.

    NetworkXNotImplemented
        If `G` is not a simple graph.

    Examples
    --------
    The number of edges will never decrease when taking successive
    powers:

    >>> G = nx.path_graph(4)
    >>> list(nx.power(G, 2).edges)
    [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3)]
    >>> list(nx.power(G, 3).edges)
    [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]

    The `k` th power of a cycle graph on *n* nodes is the complete graph
    on *n* nodes, if `k` is at least ``n // 2``:

    >>> G = nx.cycle_graph(5)
    >>> H = nx.complete_graph(5)
    >>> nx.is_isomorphic(nx.power(G, 2), H)
    True
    >>> G = nx.cycle_graph(8)
    >>> H = nx.complete_graph(8)
    >>> nx.is_isomorphic(nx.power(G, 4), H)
    True

    References
    ----------
    .. [1] J. A. Bondy, U. S. R. Murty, *Graph Theory*. Springer, 2008.

    Notes
    -----
    This definition of "power graph" comes from Exercise 3.1.6 of
    *Graph Theory* by Bondy and Murty [1]_.

    """
    if k <= 0:
        raise ValueError("k must be a positive integer")
    H = nx.Graph()
    H.add_nodes_from(G)
    # update BFS code to ignore self loops.
    for n in G:
        seen = {}  # level (number of hops) when seen in BFS
        level = 1  # the current level
        nextlevel = G[n]
        while nextlevel:
            thislevel = nextlevel  # advance to next level
            nextlevel = {}  # and start a new list (fringe)
            for v in thislevel:
                if v == n:  # avoid self loop
                    continue
                if v not in seen:
                    seen[v] = level  # set the level of vertex v
                    nextlevel.update(G[v])  # add neighbors of v
            if k <= level:
                break
            level += 1
        H.add_edges_from((n, nbr) for nbr in seen)
    return H


def power(x, y=2):
    return int(x) ** y


def power(lhs: _ods_ir.Value[_ods_ir.RankedTensorType], rhs: _ods_ir.Value[_ods_ir.RankedTensorType], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return PowOp(lhs=lhs, rhs=rhs, results=results, loc=loc, ip=ip).result


def power(lhs: _ods_ir.Value[_ods_ir.RankedTensorType], rhs: _ods_ir.Value[_ods_ir.RankedTensorType], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return PowOp(lhs=lhs, rhs=rhs, results=results, loc=loc, ip=ip).result


def power(x1: ArrayLike, x2: ArrayLike, /) -> Array:
  """Calculate element-wise base ``x1`` exponential of ``x2``.

  JAX implementation of :obj:`numpy.power`.

  Args:
    x1: scalar or array. Specifies the bases.
    x2: scalar or array. Specifies the exponent. ``x1`` and ``x2`` should either
      have same shape or be broadcast compatible.

  Returns:
    An array containing the base ``x1`` exponentials of ``x2`` with same dtype
    as input.

  Note:
    - When ``x2`` is a concrete integer scalar, ``jnp.power`` lowers to
      :func:`jax.lax.integer_pow`.
    - When ``x2`` is a traced scalar or an array, ``jnp.power`` lowers to
      :func:`jax.lax.pow`.
    - ``jnp.power`` raises a ``TypeError`` for integer type raised to a concrete
      negative integer power. For a non-concrete power, the operation is invalid
      and the returned value is implementation-defined.
    - ``jnp.power`` returns ``nan`` for negative value raised to the power of
      non-integer values.

  See also:
    - :func:`jax.lax.pow`: Computes element-wise power, :math:`x^y`.
    - :func:`jax.lax.integer_pow`: Computes element-wise power :math:`x^y`, where
      :math:`y` is a fixed integer.
    - :func:`jax.numpy.float_power`: Computes the first array raised to the power
      of second array, element-wise, by promoting to the inexact dtype.
    - :func:`jax.numpy.pow`: Computes the first array raised to the power of second
      array, element-wise.

  Examples:
    Inputs with scalar integers:

    >>> jnp.power(4, 3)
    Array(64, dtype=int32, weak_type=True)

    Inputs with same shape:

    >>> x1 = jnp.array([2, 4, 5])
    >>> x2 = jnp.array([3, 0.5, 2])
    >>> jnp.power(x1, x2)
    Array([ 8.,  2., 25.], dtype=float32)

    Inputs with broadcast compatibility:

    >>> x3 = jnp.array([-2, 3, 1])
    >>> x4 = jnp.array([[4, 1, 6],
    ...                 [1.3, 3, 5]])
    >>> jnp.power(x3, x4)
    Array([[16.,  3.,  1.],
           [nan, 27.,  1.]], dtype=float32)
  """
  check_arraylike("power", x1, x2)

  # Must do __jax_array__ conversion prior to dtype check.
  m1 = getattr(x1, "__jax_array__", None)
  x1 = m1() if m1 is not None else x1
  m2 = getattr(x2, "__jax_array__", None)
  x2 = m2() if m2 is not None else x2

  check_no_float0s("power", x1, x2)

  # We apply special cases, both for algorithmic and autodiff reasons:
  #  1. for *concrete* integer scalar powers (and arbitrary bases), we use
  #     unrolled binary exponentiation specialized on the exponent, which is
  #     more precise for e.g. x ** 2 when x is a float (algorithmic reason!);
  #  2. for integer bases and integer powers, use unrolled binary exponentiation
  #     where the number of steps is determined by a max bit width of 64
  #     (algorithmic reason!);
  #  3. for integer powers and float/complex bases, we apply the lax primitive
  #     without any promotion of input types because in this case we want the
  #     function to be differentiable wrt its first argument at 0;
  #  3. for other cases, perform jnp dtype promotion on the arguments then apply
  #     lax.pow.

  # Case 1: concrete integer scalar powers:
  if core.is_concrete(x2):
    try:
      x2 = operator.index(x2)  # pyrefly: ignore[bad-argument-type]
    except TypeError:
      pass
    else:
      x1, = promote_dtypes_numeric(x1)
      return lax.integer_pow(x1, x2)

  # Handle cases #2 and #3 under a jit:
  out = _power(x1, x2)
  jnp_error._set_error_if_nan(out)
  return out

