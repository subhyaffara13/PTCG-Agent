
def Rayleigh(name, sigma):
    r"""
    Create a continuous random variable with a Rayleigh distribution.

    Explanation
    ===========

    The density of the Rayleigh distribution is given by

    .. math ::
        f(x) := \frac{x}{\sigma^2} e^{-x^2/2\sigma^2}

    with :math:`x > 0`.

    Parameters
    ==========

    sigma : Real number, `\sigma > 0`

    Returns
    =======

    RandomSymbol

    Examples
    ========

    >>> from sympy.stats import Rayleigh, density, E, variance
    >>> from sympy import Symbol

    >>> sigma = Symbol("sigma", positive=True)
    >>> z = Symbol("z")

    >>> X = Rayleigh("x", sigma)

    >>> density(X)(z)
    z*exp(-z**2/(2*sigma**2))/sigma**2

    >>> E(X)
    sqrt(2)*sqrt(pi)*sigma/2

    >>> variance(X)
    -pi*sigma**2/2 + 2*sigma**2

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Rayleigh_distribution
    .. [2] https://mathworld.wolfram.com/RayleighDistribution.html

    """

    return rv(name, RayleighDistribution, (sigma, ))


def rayleigh(key: ArrayLike,
             scale: RealArray,
             shape: Shape | None = None,
             dtype: DTypeLikeFloat | None = None,
             *,
             out_sharding: NamedSharding | P | None = None) -> Array:
  r"""Sample Rayleigh random values with given shape and float dtype.

  The values are returned according to the probability density function:

  .. math::
     f(x;\sigma) \propto xe^{-x^2/(2\sigma^2)}

  on the domain :math:`-\infty < x < \infty`, and where :math:`\sigma > 0` is the scale
  parameter of the distribution.

  Args:
    key: a PRNG key used as the random key.
    scale: a float or array of floats broadcast-compatible with ``shape``
      representing the parameter of the distribution.
    shape: optional, a tuple of nonnegative integers specifying the result
      shape. Must be broadcast-compatible with ``scale``. The default (None)
      produces a result shape equal to ``scale.shape``.
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
    ``shape`` is not None, or else by ``scale.shape``.
  """
  key, _ = _check_prng_key("rayleigh", key)
  dtype = dtypes.check_and_canonicalize_user_dtype(
      float if dtype is None else dtype)
  if not dtypes.issubdtype(dtype, np.floating):
    raise ValueError("dtype argument to `rayleigh` must be a float "
                     f"dtype, got {dtype}")
  shape = _check_broadcast_shapes("rayleigh", shape, scale)
  out_sharding = canonicalize_sharding_for_samplers(out_sharding, "rayleigh", shape)
  _check_all_safe_to_cast("rayleigh", dtype, scale)
  return maybe_auto_axes(_rayleigh, out_sharding,
                         shape=shape, dtype=dtype)(key, scale)

