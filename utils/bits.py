
def bits(key: ArrayLike,
         shape: Shape = (),
         dtype: DTypeLikeUInt | None = None,
         *,
         out_sharding: NamedSharding | P | None = None) -> Array:
  """Sample uniform bits in the form of unsigned integers.

  Args:
    key: a PRNG key used as the random key.
    shape: optional, a tuple of nonnegative integers representing the result
      shape. Default ``()``.
    dtype: optional, an unsigned integer dtype for the returned values (default
      ``uint64`` if ``jax_enable_x64`` is true, otherwise ``uint32``).
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
  key, _ = _check_prng_key("bits", key)
  if dtype is None:
    dtype = dtypes.default_uint_dtype()
  else:
    dtype = dtypes.check_and_canonicalize_user_dtype(dtype)
  if not dtypes.issubdtype(dtype, np.unsignedinteger):
    raise ValueError("dtype argument to `bits` must be an unsigned int dtype, "
                     f"got {dtype}")
  shape = core.canonicalize_shape(shape)
  out_sharding = canonicalize_sharding_for_samplers(out_sharding, "bits", shape)
  bit_width = dtype.itemsize * 8
  return maybe_auto_axes(_random_bits, out_sharding,
                         bit_width=bit_width, shape=shape)(key)

