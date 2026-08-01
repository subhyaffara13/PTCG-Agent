
def itemsize_bits(dtype: DTypeLike) -> int:
  """Number of bits per element for the dtype."""
  # Note: we cannot use dtype.itemsize here because this is
  # incorrect for sub-byte integer types.
  if dtype is None:
    raise ValueError("dtype cannot be None.")
  if dtype == np.dtype(bool):
    return 8  # physical bit layout for boolean dtype
  elif issubdtype(dtype, np.integer):
    return iinfo(dtype).bits
  elif issubdtype(dtype, np.floating):
    return finfo(dtype).bits
  elif issubdtype(dtype, np.complexfloating):
    return 2 * finfo(dtype).bits
  else:
    raise ValueError(f"unexpected input: {dtype=}")

