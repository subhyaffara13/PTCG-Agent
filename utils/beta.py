
def Beta(name, alpha, beta):
    r"""
    Create a Continuous Random Variable with a Beta distribution.

    The density of the Beta distribution is given by

    .. math::
        f(x) := \frac{x^{\alpha-1}(1-x)^{\beta-1}} {\mathrm{B}(\alpha,\beta)}

    with :math:`x \in [0,1]`.

    Parameters
    ==========

    alpha : Real number, `\alpha > 0`, a shape
    beta : Real number, `\beta > 0`, a shape

    Returns
    =======

    RandomSymbol

    Examples
    ========

    >>> from sympy.stats import Beta, density, E, variance
    >>> from sympy import Symbol, simplify, pprint, factor

    >>> alpha = Symbol("alpha", positive=True)
    >>> beta = Symbol("beta", positive=True)
    >>> z = Symbol("z")

    >>> X = Beta("x", alpha, beta)

    >>> D = density(X)(z)
    >>> pprint(D, use_unicode=False)
     alpha - 1        beta - 1
    z         *(1 - z)
    --------------------------
          B(alpha, beta)

    >>> simplify(E(X))
    alpha/(alpha + beta)

    >>> factor(simplify(variance(X)))
    alpha*beta/((alpha + beta)**2*(alpha + beta + 1))

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Beta_distribution
    .. [2] https://mathworld.wolfram.com/BetaDistribution.html

    """

    return rv(name, BetaDistribution, (alpha, beta))


def beta(ctx, x, y):
    x = ctx.convert(x)
    y = ctx.convert(y)
    if ctx.isinf(y):
        x, y = y, x
    if ctx.isinf(x):
        if x == ctx.inf and not ctx._im(y):
            if y == ctx.ninf:
                return ctx.nan
            if y > 0:
                return ctx.zero
            if ctx.isint(y):
                return ctx.nan
            if y < 0:
                return ctx.sign(ctx.gamma(y)) * ctx.inf
        return ctx.nan
    xy = ctx.fadd(x, y, prec=2*ctx.prec)
    return ctx.gammaprod([x, y], [xy])


def beta(key: ArrayLike,
         a: RealArray,
         b: RealArray,
         shape: Shape | None = None,
         dtype: DTypeLikeFloat | None = None,
         *,
         out_sharding: NamedSharding | P | None = None) -> Array:
  r"""Sample Beta random values with given shape and float dtype.

  The values are distributed according to the probability density function:

  .. math::
     f(x;a,b) \propto x^{a - 1}(1 - x)^{b - 1}

  on the domain :math:`0 \le x \le 1`.

  Args:
    key: a PRNG key used as the random key.
    a: a float or array of floats broadcast-compatible with ``shape``
      representing the first parameter "alpha".
    b: a float or array of floats broadcast-compatible with ``shape``
      representing the second parameter "beta".
    shape: optional, a tuple of nonnegative integers specifying the result
      shape. Must be broadcast-compatible with ``a`` and ``b``. The default
      (None) produces a result shape by broadcasting ``a`` and ``b``.
    dtype: optional, a float dtype for the returned values (default float64 if
      jax_enable_x64 is true, otherwise float32).
    out_sharding: Optional. Specifies how the output array should be sharded
      across devices in multi-device computation. Can be a
      :class:`~jax.sharding.NamedSharding`, a :class:`~jax.sharding.PartitionSpec`
      (``P``), or ``None`` (default). When specified, the output will be sharded
      according to the given sharding specification. Primarily used in explicit
      sharding mode.
      See the `explicit sharding tutorial <https://docs.jax.dev/en/latest/parallel.html>`_
      for more details.

  Returns:
    A random array with the specified dtype and shape given by ``shape`` if
    ``shape`` is not None, or else by broadcasting ``a`` and ``b``.
  """
  key, _ = _check_prng_key("beta", key)
  dtype = dtypes.check_and_canonicalize_user_dtype(
      float if dtype is None else dtype)
  if not dtypes.issubdtype(dtype, np.floating):
    raise ValueError(f"dtype argument to `beta` must be a float "
                     f"dtype, got {dtype}")
  _check_all_safe_to_cast("beta", dtype, a, b)
  shape = _check_broadcast_shapes("beta", shape, a, b)
  out_sharding = canonicalize_sharding_for_samplers(out_sharding, "beta", shape)

  return maybe_auto_axes(_beta, out_sharding,
                         shape=shape, dtype=dtype)(key, a, b)


def beta(a: ArrayLike, b: ArrayLike) -> Array:
  r"""The beta function

  JAX implementation of :obj:`scipy.special.beta`.

  .. math::

     \mathrm{beta}(a, b) = B(a, b) = \frac{\Gamma(a)\Gamma(b)}{\Gamma(a + b)}

  where :math:`\Gamma` is the :func:`~jax.scipy.special.gamma` function.

  Args:
    a: arraylike, real-valued. Parameter *a* of the beta distribution.
    b: arraylike, real-valued. Parameter *b* of the beta distribution.

  Returns:
    array containing the values of the beta function.

  See Also:
    - :func:`jax.scipy.special.gamma`
    - :func:`jax.scipy.special.betaln`
  """
  a, b = promote_args_inexact("beta", a, b)
  if dtypes.issubdtype(a.dtype, np.complexfloating):
    raise ValueError("beta does not support complex-valued inputs.")
  sign = gammasgn(a) * gammasgn(b) * gammasgn(a + b)
  return sign * lax.exp(betaln(a, b))

