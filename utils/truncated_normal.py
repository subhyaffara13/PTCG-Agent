
def truncated_normal(stddev: RealNumeric = 1e-2,
                     dtype: DTypeLikeInexact | None = None,
                     lower: RealNumeric = -2.0,
                     upper: RealNumeric = 2.0) -> Initializer:
  r"""Builds an initializer that returns truncated-normal random arrays.

  Args:
    stddev: optional; the standard deviation of the untruncated distribution.
      Note that this function does not apply the stddev correction as is done in
      the variancescaling initializers, and users are expected to apply this
      correction themselves via the stddev arg if they wish to employ it.
    dtype: optional; the initializer's default dtype.
    lower: Float representing the lower bound for truncation. Applied before
      the output is multiplied by the stddev.
    upper: Float representing the upper bound for truncation. Applied before
      the output is multiplied by the stddev.

  Returns:
    An initializer that returns arrays whose values follow the truncated normal
    distribution with mean ``0`` and standard deviation ``stddev``, and range
    :math:`\rm{lower * stddev} < x < \rm{upper * stddev}`.

  >>> import jax, jax.numpy as jnp
  >>> initializer = jax.nn.initializers.truncated_normal(5.0)
  >>> initializer(jax.random.key(42), (2, 3), jnp.float32)  # doctest: +SKIP
  Array([[ 2.9047365,  5.2338114,  5.29852  ],
         [-3.836303 , -4.192359 ,  0.6022964]], dtype=float32)
  """
  def init(key: Array,
           shape: core.Shape,
           dtype: DTypeLikeInexact | None = dtype,
           out_sharding: OutShardingType = None) -> Array:
    dtype = dtypes.default_float_dtype() if dtype is None else dtype
    return random.truncated_normal(
        key, lower, upper, shape, dtype,
        out_sharding=out_sharding) * jnp.array(stddev, dtype)
  return init


def truncated_normal(key: ArrayLike,
                     lower: RealArray,
                     upper: RealArray,
                     shape: Shape | None = None,
                     dtype: DTypeLikeFloat | None = None,
                     *,
                     out_sharding: NamedSharding | P | None = None) -> Array:
  r"""Sample truncated standard normal random values with given shape and dtype.

  The values are returned according to the probability density function:

  .. math::
     f(x) \propto e^{-x^2/2}

  on the domain :math:`\rm{lower} < x < \rm{upper}`.

  Args:
    key: a PRNG key used as the random key.
    lower: a float or array of floats representing the lower bound for
      truncation. Must be broadcast-compatible with ``upper``.
    upper: a float or array of floats representing the  upper bound for
      truncation. Must be broadcast-compatible with ``lower``.
    shape: optional, a tuple of nonnegative integers specifying the result
      shape. Must be broadcast-compatible with ``lower`` and ``upper``. The
      default (None) produces a result shape by broadcasting ``lower`` and
      ``upper``.
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
    ``shape`` is not None, or else by broadcasting ``lower`` and ``upper``.
    Returns values in the open interval ``(lower, upper)``.
  """
  if shape is not None:
    shape = core.canonicalize_shape(shape)
  key, _ = _check_prng_key("truncated_normal", key)
  out_sharding = canonicalize_sharding(out_sharding, "truncated_normal")
  dtype = dtypes.check_and_canonicalize_user_dtype(
      float if dtype is None else dtype)
  if not dtypes.issubdtype(dtype, np.floating):
    raise ValueError(f"dtype argument to `truncated_normal` must be a float "
                     f"dtype, got {dtype}")
  return maybe_auto_axes(_truncated_normal, out_sharding,
                         shape=shape, dtype=dtype)(key, lower, upper)

