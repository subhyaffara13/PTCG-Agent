
def rand_some_inf(rng):
  """Return a random sampler that produces infinities in floating types."""
  base_rand = rand_default(rng)

  # TODO: Complex numbers are not correctly tested
  # If blocks should be switched in order, and relevant tests should be fixed
  def rand(shape, dtype):
    """The random sampler function."""
    if not _dtypes.issubdtype(dtype, np.floating):
      # only float types have inf
      return base_rand(shape, dtype)

    if _dtypes.issubdtype(dtype, np.complexfloating):
      base_dtype = np.real(np.array(0, dtype=dtype)).dtype
      out = (rand(shape, base_dtype) +
             np.array(1j, dtype) * rand(shape, base_dtype))
      return _cast_to_shape(out, shape, dtype)

    dims = _dims_of_shape(shape)
    posinf_flips = rng.rand(*dims) < 0.1
    neginf_flips = rng.rand(*dims) < 0.1

    vals = base_rand(shape, dtype)
    vals = np.where(posinf_flips, np.array(np.inf, dtype=dtype), vals)
    vals = np.where(neginf_flips, np.array(-np.inf, dtype=dtype), vals)

    return _cast_to_shape(np.asarray(vals, dtype=dtype), shape, dtype)

  return rand

