
def geometric(self, p, generator=None):
    if generator is not None:
        raise AssertionError("generator is not supported in refs")
    # TODO: fix inductor rand_like for integer, bool dtypes
    torch._check(
        not utils.is_complex_dtype(self.dtype)
        and not utils.is_boolean_dtype(self.dtype),
        lambda: f"geometric not implemented for {self.dtype}",
    )
    torch._check(
        0 < p and p < 1,
        lambda: f"geometric_ expects p to be in (0, 1), but got p={p}",
    )
    return torch.floor(torch.log1p(-torch.rand_like(self)) / math.log1p(-p)) + 1


def Geometric(name, p):
    r"""
    Create a discrete random variable with a Geometric distribution.

    Explanation
    ===========

    The density of the Geometric distribution is given by

    .. math::
        f(k) := p (1 - p)^{k - 1}

    Parameters
    ==========

    p : A probability between 0 and 1

    Returns
    =======

    RandomSymbol

    Examples
    ========

    >>> from sympy.stats import Geometric, density, E, variance
    >>> from sympy import Symbol, S

    >>> p = S.One / 5
    >>> z = Symbol("z")

    >>> X = Geometric("x", p)

    >>> density(X)(z)
    (4/5)**(z - 1)/5

    >>> E(X)
    5

    >>> variance(X)
    20

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Geometric_distribution
    .. [2] https://mathworld.wolfram.com/GeometricDistribution.html

    """
    return rv(name, GeometricDistribution, p)


def geometric(key: ArrayLike,
              p: RealArray,
              shape: Shape | None = None,
              dtype: DTypeLikeInt | None = None,
              *,
              out_sharding: NamedSharding | P | None = None) -> Array:
  r"""Sample Geometric random values with given shape and float dtype.

  The values are returned according to the probability mass function:

  .. math::
      f(k;p) = p(1-p)^{k-1}

  on the domain :math:`0 < p < 1`.

  Args:
    key: a PRNG key used as the random key.
    p: a float or array of floats broadcast-compatible with ``shape``
      representing the probability of success of an individual trial.
    shape: optional, a tuple of nonnegative integers specifying the result
      shape. Must be broadcast-compatible with ``p``. The default
      (None) produces a result shape equal to ``np.shape(p)``.
    dtype: optional, a int dtype for the returned values (default int64 if
      jax_enable_x64 is true, otherwise int32).
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
    ``shape`` is not None, or else by ``p.shape``.
  """
  key, _ = _check_prng_key("geometric", key)
  dtype = dtypes.check_and_canonicalize_user_dtype(
      int if dtype is None else dtype)
  if not dtypes.issubdtype(dtype, np.integer):
    raise ValueError("dtype argument to `geometric` must be an int "
                     f"dtype, got {dtype}")
  shape = _check_broadcast_shapes("geometric", shape, p)
  out_sharding = canonicalize_sharding_for_samplers(out_sharding, "geometric", shape)
  return _geometric(key, p, shape, dtype, out_sharding)

