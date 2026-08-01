
def _get_and_check_dtype(
    arrays: Sequence[basearray.Array | np.ndarray | literals.TypedNdArray],
    dtype: DTypeLike | ExtendedDType | None,
    fname: str,
):
  if dtype is None:
    if arrays:
      dtype = arrays[0].dtype
    else:
      raise ValueError(
          "If the Array has no addressable shards, `dtype` must be provided "
          f"via the `dtype` argument to `jax.{fname}`.")
  else:
    dtype = dtypes.check_and_canonicalize_user_dtype(dtype, fname)
    if arrays and arrays[0].dtype != dtype:
      raise ValueError(
          f"If `dtype` is provided to `jax.{fname}`, it must match the dtype "
          f"of the addressable shards. Got dtype={dtype} and shard "
          f"dtype={arrays[0].dtype}`.")
  return dtype

