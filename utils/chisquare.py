
def chisquare(f_obs, f_exp=None, ddof=0, axis=0, *, sum_check=True):
    """Perform Pearson's chi-squared test.

    Pearson's chi-squared test [1]_ is a goodness-of-fit test for a multinomial
    distribution with given probabilities; that is, it assesses the null hypothesis
    that the observed frequencies (counts) are obtained by independent
    sampling of *N* observations from a categorical distribution with given
    expected frequencies.

    Parameters
    ----------
    f_obs : array_like
        Observed frequencies in each category.
    f_exp : array_like, optional
        Expected frequencies in each category. By default, the categories are
        assumed to be equally likely.
    ddof : int, optional
        "Delta degrees of freedom": adjustment to the degrees of freedom
        for the p-value.  The p-value is computed using a chi-squared
        distribution with ``k - 1 - ddof`` degrees of freedom, where ``k``
        is the number of categories.  The default value of `ddof` is 0.
    axis : int or None, optional
        The axis of the broadcast result of `f_obs` and `f_exp` along which to
        apply the test.  If axis is None, all values in `f_obs` are treated
        as a single data set.  Default is 0.
    sum_check : bool, optional
        Whether to perform a check that ``sum(f_obs) - sum(f_exp) == 0``. If True,
        (default) raise an error (or, for lazy backends, return NaN) when the relative
        difference exceeds the square root of the precision of the data type.
        See Notes for rationale and possible exceptions.

    Returns
    -------
    res: Power_divergenceResult
        An object containing attributes:

        statistic : float or ndarray
            The chi-squared test statistic.  The value is a float if `axis` is
            None or `f_obs` and `f_exp` are 1-D.
        pvalue : float or ndarray
            The p-value of the test.  The value is a float if `ddof` and the
            result attribute `statistic` are scalars.

    See Also
    --------
    scipy.stats.power_divergence
    scipy.stats.fisher_exact : Fisher exact test on a 2x2 contingency table.
    scipy.stats.barnard_exact : An unconditional exact test. An alternative
        to chi-squared test for small sample sizes.
    :ref:`hypothesis_chisquare` : Extended example

    Notes
    -----
    This test is invalid when the observed or expected frequencies in each
    category are too small.  A typical rule is that all of the observed
    and expected frequencies should be at least 5. According to [2]_, the
    total number of observations is recommended to be greater than 13,
    otherwise exact tests (such as Barnard's Exact test) should be used
    because they do not overreject.

    The default degrees of freedom, k-1, are for the case when no parameters
    of the distribution are estimated. If p parameters are estimated by
    efficient maximum likelihood then the correct degrees of freedom are
    k-1-p. If the parameters are estimated in a different way, then the
    dof can be between k-1-p and k-1. However, it is also possible that
    the asymptotic distribution is not chi-square, in which case this test
    is not appropriate.

    For Pearson's chi-squared test, the total observed and expected counts must match
    for the p-value to accurately reflect the probability of observing such an extreme
    value of the statistic under the null hypothesis.
    This function may be used to perform other statistical tests that do not require
    the total counts to be equal. For instance, to test the null hypothesis that
    ``f_obs[i]`` is Poisson-distributed with expectation ``f_exp[i]``, set ``ddof=-1``
    and ``sum_check=False``. This test follows from the fact that a Poisson random
    variable with mean and variance ``f_exp[i]`` is approximately normal with the
    same mean and variance; the chi-squared statistic standardizes, squares, and sums
    the observations; and the sum of ``n`` squared standard normal variables follows
    the chi-squared distribution with ``n`` degrees of freedom.

    References
    ----------
    .. [1] "Pearson's chi-squared test".
           *Wikipedia*. https://en.wikipedia.org/wiki/Pearson%27s_chi-squared_test
    .. [2] Pearson, Karl. "On the criterion that a given system of deviations from the probable
           in the case of a correlated system of variables is such that it can be reasonably
           supposed to have arisen from random sampling", Philosophical Magazine. Series 5. 50
           (1900), pp. 157-175.

    Examples
    --------
    When only the mandatory `f_obs` argument is given, it is assumed that the
    expected frequencies are uniform and given by the mean of the observed
    frequencies:

    >>> import numpy as np
    >>> from scipy.stats import chisquare
    >>> chisquare([16, 18, 16, 14, 12, 12])
    Power_divergenceResult(statistic=2.0, pvalue=0.84914503608460956)

    The optional `f_exp` argument gives the expected frequencies.

    >>> chisquare([16, 18, 16, 14, 12, 12], f_exp=[16, 16, 16, 16, 16, 8])
    Power_divergenceResult(statistic=3.5, pvalue=0.62338762774958223)

    When `f_obs` is 2-D, by default the test is applied to each column.

    >>> obs = np.array([[16, 18, 16, 14, 12, 12], [32, 24, 16, 28, 20, 24]]).T
    >>> obs.shape
    (6, 2)
    >>> chisquare(obs)
    Power_divergenceResult(statistic=array([2.        , 6.66666667]), pvalue=array([0.84914504, 0.24663415]))

    By setting ``axis=None``, the test is applied to all data in the array,
    which is equivalent to applying the test to the flattened array.

    >>> chisquare(obs, axis=None)
    Power_divergenceResult(statistic=23.31034482758621, pvalue=0.015975692534127565)
    >>> chisquare(obs.ravel())
    Power_divergenceResult(statistic=23.310344827586206, pvalue=0.01597569253412758)

    `ddof` is the change to make to the default degrees of freedom.

    >>> chisquare([16, 18, 16, 14, 12, 12], ddof=1)
    Power_divergenceResult(statistic=2.0, pvalue=0.7357588823428847)

    The calculation of the p-values is done by broadcasting the
    chi-squared statistic with `ddof`.

    >>> chisquare([16, 18, 16, 14, 12, 12], ddof=[0, 1, 2])
    Power_divergenceResult(statistic=2.0, pvalue=array([0.84914504, 0.73575888, 0.5724067 ]))

    `f_obs` and `f_exp` are also broadcast.  In the following, `f_obs` has
    shape (6,) and `f_exp` has shape (2, 6), so the result of broadcasting
    `f_obs` and `f_exp` has shape (2, 6).  To compute the desired chi-squared
    statistics, we use ``axis=1``:

    >>> chisquare([16, 18, 16, 14, 12, 12],
    ...           f_exp=[[16, 16, 16, 16, 16, 8], [8, 20, 20, 16, 12, 12]],
    ...           axis=1)
    Power_divergenceResult(statistic=array([3.5 , 9.25]), pvalue=array([0.62338763, 0.09949846]))

    For a more detailed example, see :ref:`hypothesis_chisquare`.
    """  # noqa: E501
    return _power_divergence(f_obs, f_exp=f_exp, ddof=ddof, axis=axis,
                             lambda_="pearson", sum_check=sum_check)


def chisquare(key: ArrayLike,
              df: RealArray,
              shape: Shape | None = None,
              dtype: DTypeLikeFloat | None = None,
              *,
              out_sharding: NamedSharding | P | None = None) -> Array:
  r"""Sample Chisquare random values with given shape and float dtype.

  The values are distributed according to the probability density function:

  .. math::
     f(x; \nu) \propto x^{\nu/2 - 1}e^{-x/2}

  on the domain :math:`0 < x < \infty`, where :math:`\nu > 0` represents the
  degrees of freedom, given by the parameter ``df``.

  Args:
    key: a PRNG key used as the random key.
    df: a float or array of floats broadcast-compatible with ``shape``
      representing the parameter of the distribution.
    shape: optional, a tuple of nonnegative integers specifying the result
      shape. Must be broadcast-compatible with ``df``. The default (None)
      produces a result shape equal to ``df.shape``.
    dtype: optional, a float dtype for the returned values (default float64 if
      jax_enable_x64 is true, otherwise float32).
    out_sharding: optional, Specifies how the output array should be sharded
      across devices in multi-device computation. Can be a
      :class:`~jax.sharding.NamedSharding`, a :class:`~jax.sharding.PartitionSpec`
      (``P``), or ``None`` (default). When specified, the output will be sharded
      according to the given sharding specification. Primarily used in explicit
      sharding mode.
      See the `explicit sharding tutorial <https://docs.jax.dev/en/latest/parallel.html>`_
      for more details.

  Returns:
    A random array with the specified dtype and with shape given by ``shape`` if
    ``shape`` is not None, or else by ``df.shape``.
  """
  key, _ = _check_prng_key("chisquare", key)
  dtype = dtypes.check_and_canonicalize_user_dtype(
      float if dtype is None else dtype)
  if not dtypes.issubdtype(dtype, np.floating):
    raise ValueError("dtype argument to `chisquare` must be a float "
                     f"dtype, got {dtype}")
  shape = _check_broadcast_shapes("chisquare", shape, df)
  _check_all_safe_to_cast("chisquare", dtype, df)
  out_sharding = canonicalize_sharding_for_samplers(out_sharding, "chisquare", shape)
  return _chisquare(key, df, shape, dtype, out_sharding)

