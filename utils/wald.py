
def wald(key: ArrayLike,
         mean: RealArray,
         shape: Shape | None = None,
         dtype: DTypeLikeFloat | None = None,
         *,
         out_sharding: NamedSharding | P | None = None) -> Array:
  r"""Sample Wald random values with given shape and float dtype.

  The values are returned according to the probability density function:

  .. math::
     f(x;\mu) = \frac{1}{\sqrt{2\pi x^3}} \exp\left(-\frac{(x - \mu)^2}{2\mu^2 x}\right)

  on the domain :math:`-\infty < x < \infty`, and where :math:`\mu > 0` is the location
  parameter of the distribution.


  Args:
    key: a PRNG key used as the random key.
    mean: a float or array of floats broadcast-compatible with ``shape``
      representing the mean parameter of the distribution.
    shape: optional, a tuple of nonnegative integers specifying the result
      shape. Must be broadcast-compatible with ``mean``. The default
      (None) produces a result shape equal to ``np.shape(mean)``.
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
    A random array with the specified dtype and with shape given by ``shape`` if
    ``shape`` is not None, or else by ``mean.shape``.
  """
  key, _ = _check_prng_key("wald", key)
  dtype = dtypes.check_and_canonicalize_user_dtype(
      float if dtype is None else dtype)
  if not dtypes.issubdtype(dtype, np.floating):
    raise ValueError("dtype argument to `wald` must be a float "
                     f"dtype, got {dtype}")
  shape = _check_broadcast_shapes("wald", shape, mean)
  out_sharding = canonicalize_sharding(out_sharding, "wald")
  _check_all_safe_to_cast("wald", dtype, mean)
  return maybe_auto_axes(_wald, out_sharding, shape=shape, dtype=dtype)(key, mean)

