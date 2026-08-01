
def to_default_dtype(arr: ArrayLike) -> np.ndarray:
  """Convert a value to an array with JAX's default dtype.

  This is generally used for type conversions of values returned by numpy functions,
  to make their dtypes take into account the state of the ``jax_enable_x64`` flag.
  """
  arr = np.asarray(arr)
  dtype_fn = _dtypes.default_types.get(arr.dtype.kind)
  return arr.astype(dtype_fn()) if dtype_fn else arr

