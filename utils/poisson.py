
def Poisson(name, lamda):
    r"""
    Create a discrete random variable with a Poisson distribution.

    Explanation
    ===========

    The density of the Poisson distribution is given by

    .. math::
        f(k) := \frac{\lambda^{k} e^{- \lambda}}{k!}

    Parameters
    ==========

    lamda : Positive number, a rate

    Returns
    =======

    RandomSymbol

    Examples
    ========

    >>> from sympy.stats import Poisson, density, E, variance
    >>> from sympy import Symbol, simplify

    >>> rate = Symbol("lambda", positive=True)
    >>> z = Symbol("z")

    >>> X = Poisson("x", rate)

    >>> density(X)(z)
    lambda**z*exp(-lambda)/factorial(z)

    >>> E(X)
    lambda

    >>> simplify(variance(X))
    lambda

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Poisson_distribution
    .. [2] https://mathworld.wolfram.com/PoissonDistribution.html

    """
    return rv(name, PoissonDistribution, lamda)


def poisson(key: ArrayLike,
            lam: RealArray,
            shape: Shape | None = None,
            dtype: DTypeLikeInt | None = None,
            *,
            out_sharding: NamedSharding | P | None = None) -> Array:
  r"""Sample Poisson random values with given shape and integer dtype.

  The values are distributed according to the probability mass function:

  .. math::
     f(k; \lambda) = \frac{\lambda^k e^{-\lambda}}{k!}

  Where `k` is a non-negative integer and :math:`\lambda > 0`.

  Args:
    key: a PRNG key used as the random key.
    lam: rate parameter (mean of the distribution), must be >= 0. Must be broadcast-compatible with ``shape``
    shape: optional, a tuple of nonnegative integers representing the result
      shape. Default (None) produces a result shape equal to ``lam.shape``.
    dtype: optional, a integer dtype for the returned values (default int64 if
      jax_enable_x64 is true, otherwise int32).
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
    ``shape is not None, or else by ``lam.shape``.
  """
  key, _ = _check_prng_key("poisson", key)
  dtype = dtypes.check_and_canonicalize_user_dtype(
      int if dtype is None else dtype)
  # TODO(frostig): generalize underlying poisson implementation and
  # remove this check
  keys_dtype = typing.cast(prng.KeyTy, key.dtype)
  key_impl = keys_dtype._impl
  if key_impl is not threefry2x32.threefry_prng_impl:
    raise NotImplementedError(
        '`poisson` is only implemented for the threefry2x32 RNG, '
        f'not {key_impl}')
  if shape is not None:
    shape = core.canonicalize_shape(shape)
  else:
    shape = np.shape(lam)
  out_sharding = canonicalize_sharding_for_samplers(out_sharding, "poisson", shape)
  lam = jnp.broadcast_to(lam, shape)
  lam = lax.convert_element_type(lam, np.float32)
  return maybe_auto_axes(_poisson, out_sharding, shape=shape, dtype=dtype)(key, lam)

