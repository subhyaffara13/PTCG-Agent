
def Pareto(name, xm, alpha):
    r"""
    Create a continuous random variable with the Pareto distribution.

    Explanation
    ===========

    The density of the Pareto distribution is given by

    .. math::
        f(x) := \frac{\alpha\,x_m^\alpha}{x^{\alpha+1}}

    with :math:`x \in [x_m,\infty]`.

    Parameters
    ==========

    xm : Real number, `x_m > 0`, a scale
    alpha : Real number, `\alpha > 0`, a shape

    Returns
    =======

    RandomSymbol

    Examples
    ========

    >>> from sympy.stats import Pareto, density
    >>> from sympy import Symbol

    >>> xm = Symbol("xm", positive=True)
    >>> beta = Symbol("beta", positive=True)
    >>> z = Symbol("z")

    >>> X = Pareto("x", xm, beta)

    >>> density(X)(z)
    beta*xm**beta*z**(-beta - 1)

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Pareto_distribution
    .. [2] https://mathworld.wolfram.com/ParetoDistribution.html

    """

    return rv(name, ParetoDistribution, (xm, alpha))


def pareto(key: ArrayLike,
           b: RealArray,
           shape: Shape | None = None,
           dtype: DTypeLikeFloat | None = None,
           *,
           out_sharding: NamedSharding | P | None = None) -> Array:
  r"""Sample Pareto random values with given shape and float dtype.

  The values are distributed according to the probability density function:

  .. math::
     f(x; b) = b / x^{b + 1}

  on the domain :math:`1 \le x < \infty` with :math:`b > 0`

  Args:
    key: a PRNG key used as the random key.
    b: a float or array of floats broadcast-compatible with ``shape``
      representing the parameter of the distribution.
    shape: optional, a tuple of nonnegative integers specifying the result
      shape. Must be broadcast-compatible with ``b``. The default (None)
      produces a result shape equal to ``b.shape``.
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
    A random array with the specified dtype and with shape given by ``shape`` if
    ``shape`` is not None, or else by ``b.shape``.
  """
  key, _ = _check_prng_key("pareto", key)
  dtype = dtypes.check_and_canonicalize_user_dtype(
      float if dtype is None else dtype)
  if not dtypes.issubdtype(dtype, np.floating):
    raise ValueError(f"dtype argument to `pareto` must be a float "
                     f"dtype, got {dtype}")
  shape = _check_broadcast_shapes("pareto", shape, b)
  _check_all_safe_to_cast("pareto", dtype, b)
  out_sharding = canonicalize_sharding_for_samplers(out_sharding, "pareto", shape)
  return maybe_auto_axes(_pareto, out_sharding,
                         shape=shape, dtype=dtype)(key, b)

