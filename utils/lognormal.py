
def lognormal(key: ArrayLike,
              sigma: RealArray = np.float32(1),
              shape: Shape | None = None,
              dtype: DTypeLikeFloat | None = None,
              *,
              out_sharding: NamedSharding | P | None = None) -> Array:
  r""" Sample lognormal random values with given shape and float dtype.

  The values are distributed according to the probability density function:

  .. math::
      f(x) = \frac{1}{x\sqrt{2\pi\sigma^2}}\exp\left(-\frac{(\log x)^2}{2\sigma^2}\right)

  on the domain :math:`x > 0`.

  Args:
    key: a PRNG key used as the random key.
    sigma: a float or array of floats broadcast-compatible with ``shape`` representing
      the standard deviation of the underlying normal distribution. Default 1.
    shape: optional, a tuple of nonnegative integers specifying the result
      shape. The default (None) produces a result shape equal to ``()``.
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
    A random array with the specified dtype and with shape given by ``shape``.
  """
  key, _ = _check_prng_key("lognormal", key)
  dtype = dtypes.check_and_canonicalize_user_dtype(float if dtype is None else dtype)
  if not dtypes.issubdtype(dtype, np.inexact):
    raise ValueError(f"dtype argument to `lognormal` must be a float or complex dtype, "
                    f"got {dtype}")
  shape = _check_broadcast_shapes("lognormal", shape, sigma)
  out_sharding = canonicalize_sharding(out_sharding, "lognormal")
  _check_all_safe_to_cast("lognormal", dtype, sigma)
  return maybe_auto_axes(_lognormal, out_sharding, shape=shape, dtype=dtype)(key, sigma)

