
def to_shape_dtype_struct(
    arr: ArrayLike,
    dtype: jnp.dtype | None = None,
    scalar_dtype: ScalarType | None = None,
    support_format: bool = False,  # TODO(b/460844509) - True by default.
) -> jax.ShapeDtypeStruct | ScalarType:
  """Get ShapeDtypeStruct from array-like object.

  Args:
    arr: Array-like object. This can include jax.Array, jax.ShapeDtypeStruct,
      ArrayRestoreArgs, value_metadata.ArrayMetadata - anything that has
      `shape`/`global_shape`, `dtype`, and `sharding` properties. It may also be
      a numpy array or a scalar value.
    dtype: Optional dtype that overrides the dtype of `arr` in the result.
    scalar_dtype: Optional dtype to use for scalars. Useful for converting to
      Python scalar types.
    support_format: Whether to support layout in the result.

  Returns:
    jax.ShapeDtypeStruct or scalar value.
  """
  if isinstance(arr, jax.Array) and jax.dtypes.issubdtype(
      arr.dtype, jax.dtypes.prng_key
  ):
    # For random keys, extract the dtype and shape as a regular Jax array.
    # Stored metadata will help restoring the original random key.
    arr = jax.random.key_data(arr)

  if _is_scalar(arr):
    if scalar_dtype is not None:
      return scalar_dtype(arr)
    return arr
  elif isinstance(arr, np.ndarray):
    dtype = dtype or arr.dtype
    return jax.ShapeDtypeStruct(_get_shape(arr), dtype)
  else:
    shape = _get_shape(arr)
    dtype = dtype or arr.dtype
    sharding = arr.sharding
    if isinstance(sharding, sharding_metadata.ShardingMetadata):
      sharding = sharding.to_jax_sharding()
    else:
      sharding = arrays_sharding_lib.get_sharding_or_format(
          arr, support_format=support_format
      )
    return jax.ShapeDtypeStruct(shape, dtype, sharding=sharding)

