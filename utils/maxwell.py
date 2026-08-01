
def Maxwell(name, a):
    r"""
    Create a continuous random variable with a Maxwell distribution.

    Explanation
    ===========

    The density of the Maxwell distribution is given by

    .. math::
        f(x) := \sqrt{\frac{2}{\pi}} \frac{x^2 e^{-x^2/(2a^2)}}{a^3}

    with :math:`x \geq 0`.

    .. TODO - what does the parameter mean?

    Parameters
    ==========

    a : Real number, `a > 0`

    Returns
    =======

    RandomSymbol

    Examples
    ========

    >>> from sympy.stats import Maxwell, density, E, variance
    >>> from sympy import Symbol, simplify

    >>> a = Symbol("a", positive=True)
    >>> z = Symbol("z")

    >>> X = Maxwell("x", a)

    >>> density(X)(z)
    sqrt(2)*z**2*exp(-z**2/(2*a**2))/(sqrt(pi)*a**3)

    >>> E(X)
    2*sqrt(2)*a/sqrt(pi)

    >>> simplify(variance(X))
    a**2*(-8 + 3*pi)/pi

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Maxwell_distribution
    .. [2] https://mathworld.wolfram.com/MaxwellDistribution.html

    """

    return rv(name, MaxwellDistribution, (a, ))


def maxwell(key: ArrayLike,
            shape: Shape = (),
            dtype: DTypeLikeFloat | None = None,
            *,
            out_sharding: NamedSharding | P | None = None) -> Array:
  r"""Sample from a one sided Maxwell distribution.

  The values are distributed according to the probability density function:

  .. math::
     f(x) \propto x^2 e^{-x^2 / 2}

  on the domain :math:`0 \le x < \infty`.

  Args:
    key: a PRNG key.
    shape: optional, the batch dimensions of the result. Default ().
    dtype: optional, a float dtype for the returned values (default float64 if
      jax_enable_x64 is true, otherwise float32).
    out_sharding: optional, specifies how the output array should be sharded
      across devices in multi-device computation. Can be a
      :class:`~jax.sharding.NamedSharding`, a :class:`~jax.sharding.PartitionSpec`
      (``P``), or ``None`` (default). When specified, the output will be sharded
      according to the given sharding specification. Primarily used in explicit
      sharding mode.
      See the `explicit sharding tutorial <https://docs.jax.dev/en/latest/parallel.html>`_
      for more details.

  Returns:
    A jnp.array of samples, of shape `shape`.

  """
  # Generate samples using:
  # sqrt(X^2 + Y^2 + Z^2), X,Y,Z ~N(0,1)
  key, _ = _check_prng_key("maxwell", key)
  dtype = dtypes.check_and_canonicalize_user_dtype(
      float if dtype is None else dtype)
  if not dtypes.issubdtype(dtype, np.floating):
    raise ValueError(f"dtype argument to `maxwell` must be a float "
                     f"dtype, got {dtype}")
  shape = core.canonicalize_shape(shape)
  out_sharding = canonicalize_sharding_for_samplers(out_sharding, "maxwell", shape)
  return _maxwell(key, shape, dtype, out_sharding)

