
def Gumbel(name, beta, mu, minimum=False):
    r"""
    Create a Continuous Random Variable with Gumbel distribution.

    Explanation
    ===========

    The density of the Gumbel distribution is given by

    For Maximum

    .. math::
        f(x) := \dfrac{1}{\beta} \exp \left( -\dfrac{x-\mu}{\beta}
                - \exp \left( -\dfrac{x - \mu}{\beta} \right) \right)

    with :math:`x \in [ - \infty, \infty ]`.

    For Minimum

    .. math::
        f(x) := \frac{e^{- e^{\frac{- \mu + x}{\beta}} + \frac{- \mu + x}{\beta}}}{\beta}

    with :math:`x \in [ - \infty, \infty ]`.

    Parameters
    ==========

    mu : Real number, `\mu`, a location
    beta : Real number, `\beta > 0`, a scale
    minimum : Boolean, by default ``False``, set to ``True`` for enabling minimum distribution

    Returns
    =======

    RandomSymbol

    Examples
    ========

    >>> from sympy.stats import Gumbel, density, cdf
    >>> from sympy import Symbol
    >>> x = Symbol("x")
    >>> mu = Symbol("mu")
    >>> beta = Symbol("beta", positive=True)
    >>> X = Gumbel("x", beta, mu)
    >>> density(X)(x)
    exp(-exp(-(-mu + x)/beta) - (-mu + x)/beta)/beta
    >>> cdf(X)(x)
    exp(-exp(-(-mu + x)/beta))

    References
    ==========

    .. [1] https://mathworld.wolfram.com/GumbelDistribution.html
    .. [2] https://en.wikipedia.org/wiki/Gumbel_distribution
    .. [3] https://web.archive.org/web/20200628222206/http://www.mathwave.com/help/easyfit/html/analyses/distributions/gumbel_max.html
    .. [4] https://web.archive.org/web/20200628222212/http://www.mathwave.com/help/easyfit/html/analyses/distributions/gumbel_min.html

    """
    return rv(name, GumbelDistribution, (beta, mu, minimum))


def gumbel(key: ArrayLike,
           shape: Shape = (),
           dtype: DTypeLikeFloat | None = None,
           mode: str | None = None,
           *,
           out_sharding: NamedSharding | P | None = None) -> Array:
  """Sample Gumbel random values with given shape and float dtype.

  The values are distributed according to the probability density function:

  .. math::
     f(x) = e^{-(x + e^{-x})}

  Args:
    key: a PRNG key used as the random key.
    shape: optional, a tuple of nonnegative integers representing the result
      shape. Default ().
    dtype: optional, a float dtype for the returned values (default float64 if
      jax_enable_x64 is true, otherwise float32).
    mode: optional, "high" or "low" for how many bits to use when sampling.
      The default is determined by the ``use_high_dynamic_range_gumbel`` config,
      which defaults to "low". When drawing float32 samples, with mode="low" the
      uniform resolution is such that the largest possible gumbel logit is ~16;
      with mode="high" this is increased to ~32, at approximately double the
      computational cost.
    out_sharding: Optional. Specifies how the output array should be sharded
      across devices in multi-device computation. Can be a
      :class:`~jax.sharding.NamedSharding`, a :class:`~jax.sharding.PartitionSpec`
      (``P``), or ``None`` (default). When specified, the output will be sharded
      according to the given sharding specification. Primarily used in explicit
      sharding mode.
      See the `explicit sharding tutorial <https://docs.jax.dev/en/latest/parallel.html>`_
      for more details.

  Returns:
    A random array with the specified shape and dtype.
  """
  key, _ = _check_prng_key("gumbel", key)
  dtype = dtypes.check_and_canonicalize_user_dtype(
      float if dtype is None else dtype)
  if not dtypes.issubdtype(dtype, np.floating):
    raise ValueError(f"dtype argument to `gumbel` must be a float "
                     f"dtype, got {dtype}")
  shape = core.canonicalize_shape(shape)
  if mode is None:
    mode = "high" if config.use_high_dynamic_range_gumbel.value else "low"
  if mode not in ("highest", "high", "low"):
    raise ValueError("Must provide valid mode for gumbel got: %s" % mode)
  out_sharding = canonicalize_sharding_for_samplers(out_sharding, "gumbel", shape)
  return maybe_auto_axes(_gumbel, out_sharding, shape=shape, dtype=dtype,
                         mode=mode)(key)

