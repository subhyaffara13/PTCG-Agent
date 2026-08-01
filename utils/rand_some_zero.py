
def rand_some_zero(rng):
  """Return a random sampler that produces some zeros."""
  base_rand = rand_default(rng)

  def rand(shape, dtype):
    """The random sampler function."""
    dims = _dims_of_shape(shape)
    zeros = rng.rand(*dims) < 0.5

    vals = base_rand(shape, dtype)
    vals = np.where(zeros, np.array(0, dtype=dtype), vals)

    return _cast_to_shape(np.asarray(vals, dtype=dtype), shape, dtype)

  return rand

