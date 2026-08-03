import random

def normal(
    key: torch.Tensor,
    *shape: tuple[int, ...],
    mean: float = 0.0,
    std: float = 1.0,
    dtype: torch.dtype | None = None,
) -> torch.Tensor:
    r"""Generate normally distributed random values from a PRNG key.

    Produces a tensor of the given shape filled with values drawn from a normal
    distribution with the specified ``mean`` and ``std``. The output is fully
    determined by the key, so calling with the same key always returns the same
    result. The output is placed on the same device as ``key``.

    Supports batched keys: if ``key`` has shape ``(*batch, K)``, the leading
    dimensions of ``shape`` must be broadcastable with ``*batch`` and each key
    independently generates its slice of the output.

    Args:
        key (Tensor): A PRNG key returned by :func:`key`, :func:`split`, or
            :func:`fold_in`.
        *shape (int): The desired output shape.
        mean (float): Mean of the normal distribution. Default: ``0.0``.
        std (float): Standard deviation of the normal distribution. Default: ``1.0``.
        dtype (:class:`torch.dtype`, optional): The desired dtype. Default: ``torch.float32``.

    Returns:
        A tensor of the given shape filled with normal random values.

    Example::

        >>> key = torch.func._random.key(42, device="cuda")  # doctest: +SKIP
        >>> torch.func._random.normal(key, (1000,))  # doctest: +SKIP
    """
    if len(shape) == 1 and isinstance(shape[0], Sequence):
        # pyrefly: ignore [bad-argument-type]
        shape = tuple(shape[0])
    if dtype is None:
        dtype = torch.float32
    # pyrefly: ignore [no-matching-overload]
    result = torch.empty(shape, dtype=dtype, device=key.device)
    return normal_(key, result, mean=mean, std=std)


def normal(loc=0.0, scale=1.0, size=None):
    if size is None:
        size = ()
    dtype = _dtypes_impl.default_dtypes().float_dtype
    values = torch.empty(size, dtype=dtype).normal_(loc, scale)
    return array_or_scalar(values, return_scalar=size == ())


def normal(
    mean=0,
    std=1,
    size=None,
    *,
    generator=None,
    dtype=None,
    layout=None,
    device=None,
    pin_memory=None,
):
    if layout is not None and layout != torch.strided:
        raise AssertionError(f"layout must be None or torch.strided, got {layout}")

    if not isinstance(std, TensorLike):
        torch._check(
            std >= 0, lambda: f"normal expects std >= 0.0, but found std {std}"
        )

    if size is None:
        tensors = tuple(t for t in (mean, std) if isinstance(t, TensorLike))
        torch._check(
            len(tensors) > 0,
            lambda: "normal expects that either mean or std is a tensor, or size is defined",
        )
        torch._check(
            layout is None and pin_memory is None,
            lambda: "Cannot pass layout, or pin_memory without size",
        )

        size = _broadcast_shapes(*(t.shape for t in tensors))
        dtype = tensors[0].dtype
        device = tensors[0].device
    else:
        torch._check(
            not isinstance(mean, TensorLike) and not isinstance(std, TensorLike),
            lambda: "normal expects mean and std to be scalars when size is defined",
        )
        dtype = torch.get_default_dtype() if dtype is None else dtype
        device = torch.device("cpu") if device is None else device

    normal_samples = prims.normal(
        size,
        mean=0.0,
        std=1.0,
        dtype=dtype,
        device=device,
        requires_grad=False,
        generator=generator,
    )
    return std * normal_samples + mean


def normal(
    g: jit_utils.GraphContext,
    mean,
    std,
    sizes=None,
    generator=None,
    dtype=None,
    layout=None,
    device=None,
    pin_memory=None,
):
    # If you can sample from a given distribution with mean 0 and variance 1, then you can easily sample from a
    # scale-location transformation of that distribution, which has mean mu and variance sigma's square. If x is a sample
    # from a mean 0 and variance 1 distribution then
    #       sigma x+mu
    # is a sample with mean mu and variance sigma's square.
    if sizes is not None and not symbolic_helper._is_none(sizes):
        mean = opset9.expand(g, mean, sizes, None)
    result = opset9.mul(g, std, g.op("RandomNormalLike", mean))
    return add(g, result, mean)


def normal(x, mu, sigma):
    return 1/sqrt(2*pi*sigma**2)*exp(-(x - mu)**2/2/sigma**2)


def Normal(name, mean, std):
    r"""
    Create a continuous random variable with a Normal distribution.

    Explanation
    ===========

    The density of the Normal distribution is given by

    .. math::
        f(x) := \frac{1}{\sigma\sqrt{2\pi}} e^{ -\frac{(x-\mu)^2}{2\sigma^2} }

    Parameters
    ==========

    mu : Real number or a list representing the mean or the mean vector
    sigma : Real number or a positive definite square matrix,
         :math:`\sigma^2 > 0`, the variance

    Returns
    =======

    RandomSymbol

    Examples
    ========

    >>> from sympy.stats import Normal, density, E, std, cdf, skewness, quantile, marginal_distribution
    >>> from sympy import Symbol, simplify, pprint

    >>> mu = Symbol("mu")
    >>> sigma = Symbol("sigma", positive=True)
    >>> z = Symbol("z")
    >>> y = Symbol("y")
    >>> p = Symbol("p")
    >>> X = Normal("x", mu, sigma)

    >>> density(X)(z)
    sqrt(2)*exp(-(-mu + z)**2/(2*sigma**2))/(2*sqrt(pi)*sigma)

    >>> C = simplify(cdf(X))(z) # it needs a little more help...
    >>> pprint(C, use_unicode=False)
       /  ___          \
       |\/ 2 *(-mu + z)|
    erf|---------------|
       \    2*sigma    /   1
    -------------------- + -
             2             2

    >>> quantile(X)(p)
    mu + sqrt(2)*sigma*erfinv(2*p - 1)

    >>> simplify(skewness(X))
    0

    >>> X = Normal("x", 0, 1) # Mean 0, standard deviation 1
    >>> density(X)(z)
    sqrt(2)*exp(-z**2/2)/(2*sqrt(pi))

    >>> E(2*X + 1)
    1

    >>> simplify(std(2*X + 1))
    2

    >>> m = Normal('X', [1, 2], [[2, 1], [1, 2]])
    >>> pprint(density(m)(y, z), use_unicode=False)
              2          2
             y    y*z   z
           - -- + --- - -- + z - 1
      ___    3     3    3
    \/ 3 *e
    ------------------------------
                 6*pi

    >>> marginal_distribution(m, m[0])(1)
     1/(2*sqrt(pi))


    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Normal_distribution
    .. [2] https://mathworld.wolfram.com/NormalDistributionFunction.html

    """

    if isinstance(mean, list) or getattr(mean, 'is_Matrix', False) and\
        isinstance(std, list) or getattr(std, 'is_Matrix', False):
        from sympy.stats.joint_rv_types import MultivariateNormal
        return MultivariateNormal(name, mean, std)
    return rv(name, NormalDistribution, (mean, std))


def normal(stddev: RealNumeric = 1e-2,
           dtype: DTypeLikeInexact | None = None) -> Initializer:
  """Builds an initializer that returns real normally-distributed random arrays.

  Args:
    stddev: optional; the standard deviation of the distribution.
    dtype: optional; the initializer's default dtype.

  Returns:
    An initializer that returns arrays whose values are normally distributed
    with mean ``0`` and standard deviation ``stddev``.

  >>> import jax, jax.numpy as jnp
  >>> initializer = jax.nn.initializers.normal(5.0)
  >>> initializer(jax.random.key(42), (2, 3), jnp.float32)  # doctest: +SKIP
  Array([[ 3.0613258 ,  5.6129413 ,  5.6866574 ],
         [-4.063663  , -4.4520254 ,  0.63115686]], dtype=float32)
  """
  def init(key: Array,
           shape: core.Shape,
           dtype: DTypeLikeInexact | None = dtype,
           out_sharding: OutShardingType = None) -> Array:
    dtype = dtypes.default_float_dtype() if dtype is None else dtype
    return random.normal(key, shape, dtype,
                         out_sharding=out_sharding) * jnp.array(stddev, dtype)
  return init


def normal(key: ArrayLike,
           shape: Shape = (),
           dtype: DTypeLikeFloat | None = None,
           *,
           out_sharding: NamedSharding | P | None = None) -> Array:
  r"""Sample standard normal random values with given shape and float dtype.

  The values are returned according to the probability density function:

  .. math::
     f(x) = \frac{1}{\sqrt{2\pi}}e^{-x^2/2}

  on the domain :math:`-\infty < x < \infty`

  Args:
    key: a PRNG key used as the random key.
    shape: optional, a tuple of nonnegative integers representing the result
      shape. Default ().
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
    A random array with the specified shape and dtype.
  """
  key, _ = _check_prng_key("normal", key)
  shape = core.canonicalize_shape(shape)
  out_sharding = canonicalize_sharding_for_samplers(out_sharding, "normal", shape)
  dtype = dtypes.check_and_canonicalize_user_dtype(
      float if dtype is None else dtype)
  if not dtypes.issubdtype(dtype, np.inexact):
    raise ValueError(f"dtype argument to `normal` must be a float or complex dtype, "
                     f"got {dtype}")
  return maybe_auto_axes(_normal, out_sharding, shape=shape, dtype=dtype)(key)

