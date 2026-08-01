
def rand_some_nan(rng):
  """Return a random sampler that produces nans in floating types."""
  base_rand = rand_default(rng)

  def rand(shape, dtype):
    """The random sampler function."""
    if _dtypes.issubdtype(dtype, np.complexfloating):
      base_dtype = np.real(np.array(0, dtype=dtype)).dtype
      out = (rand(shape, base_dtype) +
             np.array(1j, dtype) * rand(shape, base_dtype))
      return _cast_to_shape(out, shape, dtype)

    if not _dtypes.issubdtype(dtype, np.floating):
      # only float types have inf
      return base_rand(shape, dtype)

    dims = _dims_of_shape(shape)
    r = rng.rand(*dims)
    nan_flips = r < 0.1
    neg_nan_flips = r < 0.05

    vals = base_rand(shape, dtype)
    vals = np.where(nan_flips, np.array(np.nan, dtype=dtype), vals)
    vals = np.where(neg_nan_flips, np.array(-np.nan, dtype=dtype), vals)

    return _cast_to_shape(np.asarray(vals, dtype=dtype), shape, dtype)

  return rand

