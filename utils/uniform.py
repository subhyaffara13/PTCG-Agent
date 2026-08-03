import random

def uniform(
    key: torch.Tensor,
    *shape: tuple[int, ...],
    low: float = 0.0,
    high: float = 1.0,
    dtype: torch.dtype | None = None,
) -> torch.Tensor:
    r"""Generate uniformly distributed random values from a PRNG key.

    Produces a tensor of the given shape filled with values drawn uniformly
    from the interval ``[low, high)``. The output is fully determined by the
    key, so calling with the same key always returns the same result. The output
    is placed on the same device as ``key``.

    Supports batched keys: if ``key`` has shape ``(*batch, K)``, the leading
    dimensions of ``shape`` must be broadcastable with ``*batch`` and each key
    independently generates its slice of the output.

    Args:
        key (Tensor): A PRNG key returned by :func:`key`, :func:`split`, or
            :func:`fold_in`.
        *shape (int): The desired output shape.
        low (float): Lower bound (inclusive) of the uniform distribution. Default: ``0.0``.
        high (float): Upper bound (exclusive) of the uniform distribution. Default: ``1.0``.
        dtype (:class:`torch.dtype`, optional): The desired dtype. Default: ``torch.float32``.

    Returns:
        A tensor of the given shape filled with uniform random values.

    Example::

        >>> key = torch.func._random.key(42, device="cuda")  # doctest: +SKIP
        >>> torch.func._random.uniform(key, (1000,))  # doctest: +SKIP
    """
    if len(shape) == 1 and isinstance(shape[0], Sequence):
        # pyrefly: ignore [bad-argument-type]
        shape = tuple(shape[0])
    if dtype is None:
        dtype = torch.float32
    # pyrefly: ignore [no-matching-overload]
    result = torch.empty(shape, dtype=dtype, device=key.device)
    return uniform_(key, result, low=low, high=high)


def uniform(
    x: Tensor,
    low: bool | int | float = 0.0,
    high: bool | int | float = 1.0,
    generator: torch.Generator | None = None,
):
    return prims._uniform_helper(
        x.shape,
        stride=x.stride(),
        low=sym_float(low),
        high=sym_float(high),
        dtype=x.dtype,
        device=x.device,
        generator=generator,
    )


def uniform(low=0.0, high=1.0, size=None):
    if size is None:
        size = ()
    dtype = _dtypes_impl.default_dtypes().float_dtype
    values = torch.empty(size, dtype=dtype).uniform_(low, high)
    return array_or_scalar(values, return_scalar=size == ())


def Uniform(name, left, right):
    r"""
    Create a continuous random variable with a uniform distribution.

    Explanation
    ===========

    The density of the uniform distribution is given by

    .. math::
        f(x) := \begin{cases}
                  \frac{1}{b - a} & \text{for } x \in [a,b]  \\
                  0               & \text{otherwise}
                \end{cases}

    with :math:`x \in [a,b]`.

    Parameters
    ==========

    a : Real number, :math:`-\infty < a`, the left boundary
    b : Real number, :math:`a < b < \infty`, the right boundary

    Returns
    =======

    RandomSymbol

    Examples
    ========

    >>> from sympy.stats import Uniform, density, cdf, E, variance
    >>> from sympy import Symbol, simplify

    >>> a = Symbol("a", negative=True)
    >>> b = Symbol("b", positive=True)
    >>> z = Symbol("z")

    >>> X = Uniform("x", a, b)

    >>> density(X)(z)
    Piecewise((1/(-a + b), (b >= z) & (a <= z)), (0, True))

    >>> cdf(X)(z)
    Piecewise((0, a > z), ((-a + z)/(-a + b), b >= z), (1, True))

    >>> E(X)
    a/2 + b/2

    >>> simplify(variance(X))
    a**2/12 - a*b/6 + b**2/12

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Uniform_distribution_%28continuous%29
    .. [2] https://mathworld.wolfram.com/UniformDistribution.html

    """

    return rv(name, UniformDistribution, (left, right))


def uniform(scale: RealNumeric = 1e-2,
            dtype: DTypeLikeInexact | None = None) -> Initializer:
  """Builds an initializer that returns real uniformly-distributed random arrays.

  Args:
    scale: optional; the upper bound of the random distribution.
    dtype: optional; the initializer's default dtype.

  Returns:
    An initializer that returns arrays whose values are uniformly distributed in
    the range ``[0, scale)``.

  >>> import jax, jax.numpy as jnp
  >>> initializer = jax.nn.initializers.uniform(10.0)
  >>> initializer(jax.random.key(42), (2, 3), jnp.float32)  # doctest: +SKIP
  Array([[7.298188 , 8.691938 , 8.7230015],
         [2.0818567, 1.8662417, 5.5022564]], dtype=float32)
  """
  def init(key: Array,
           shape: core.Shape,
           dtype: DTypeLikeInexact | None = dtype,
           out_sharding: OutShardingType = None) -> Array:
    dtype = dtypes.default_float_dtype() if dtype is None else dtype
    return random.uniform(key, shape, dtype,
                          out_sharding=out_sharding) * jnp.array(scale, dtype)
  return init


def uniform(key: ArrayLike,
            shape: Shape = (),
            dtype: DTypeLikeFloat | None = None,
            minval: RealArray = 0.,
            maxval: RealArray = 1.,
            *,
            out_sharding: NamedSharding | P | None = None) -> Array:
  """Sample uniform random values in [minval, maxval) with given shape/dtype.

  Args:
    key: a PRNG key used as the random key.
    shape: optional, a tuple of nonnegative integers representing the result
      shape. Default ().
    dtype: optional, a float dtype for the returned values (default float64 if
      jax_enable_x64 is true, otherwise float32).
    minval: optional, a minimum (inclusive) value broadcast-compatible with shape for the range (default 0).
    maxval: optional, a maximum (exclusive) value broadcast-compatible with shape for the range (default 1).
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
  key, _ = _check_prng_key("uniform", key)
  dtype = dtypes.check_and_canonicalize_user_dtype(
      float if dtype is None else dtype)
  shape = core.canonicalize_shape(shape)
  out_sharding = canonicalize_sharding_for_samplers(out_sharding, "uniform", shape)

  if not dtypes.issubdtype(dtype, np.floating):
    raise ValueError(f"dtype argument to `uniform` must be a float dtype, "
                     f"got {dtype}")
  return maybe_auto_axes(_uniform, out_sharding,
                         shape=shape, dtype=dtype)(key, minval, maxval)

