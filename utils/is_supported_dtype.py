
def is_supported_dtype(dtype: DTypeLike) -> bool:
  """Check if dtype is supported by jax.dlpack."""
  if dtype is None:
    # NumPy will silently cast this to float64, which may be surprising.
    raise TypeError(f"Expected a string or dtype-like object; got {dtype=}")
  return np.dtype(dtype) in SUPPORTED_DTYPES_SET

