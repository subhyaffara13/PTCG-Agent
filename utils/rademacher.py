
def Rademacher(name):
    r"""
    Create a Finite Random Variable representing a Rademacher distribution.

    Examples
    ========

    >>> from sympy.stats import Rademacher, density

    >>> X = Rademacher('X')
    >>> density(X).dict
    {-1: 1/2, 1: 1/2}

    Returns
    =======

    RandomSymbol

    See Also
    ========

    sympy.stats.Bernoulli

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Rademacher_distribution

    """
    return rv(name, RademacherDistribution)


def rademacher(key: ArrayLike,
               shape: Shape = (),
               dtype: DTypeLikeInt | None = None,
               *,
               out_sharding: NamedSharding | P | None = None) -> Array:
  r"""Sample from a Rademacher distribution.

  The values are distributed according to the probability mass function:

  .. math::
     f(k) = \frac{1}{2}(\delta(k - 1) + \delta(k + 1))

  on the domain :math:`k \in \{-1, 1\}`, where :math:`\delta(x)` is the dirac delta function.

  Args:
    key: a PRNG key.
    shape: The shape of the returned samples. Default ().
    dtype: The type used for samples.
    out_sharding: optional, specifies how the output array should be sharded
      across devices in multi-device computation. Can be a
      :class:`~jax.sharding.NamedSharding`, a :class:`~jax.sharding.PartitionSpec`
      (``P``), or ``None`` (default). When specified, the output will be sharded
      according to the given sharding specification. Primarily used in explicit
      sharding mode.
      See the `explicit sharding tutorial <https://docs.jax.dev/en/latest/parallel.html>`_
      for more details.

  Returns:
    A jnp.array of samples, of shape `shape`. Each element in the output has
    a 50% change of being 1 or -1.

  """
  key, _ = _check_prng_key("rademacher", key)
  dtype = dtypes.check_and_canonicalize_user_dtype(
      int if dtype is None else dtype)
  shape = core.canonicalize_shape(shape)
  out_sharding = canonicalize_sharding_for_samplers(out_sharding, "rademacher", shape)
  return _rademacher(key, shape, dtype, out_sharding)

