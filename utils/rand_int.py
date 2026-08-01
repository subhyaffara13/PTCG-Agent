
def rand_int(rng, low=0, high=None):
  def fn(shape, dtype):
    nonlocal high
    gen_dtype = dtype if np.issubdtype(dtype, np.integer) else np.int64
    if low == 0 and high is None:
      if np.issubdtype(dtype, np.integer):
        high = np.iinfo(dtype).max
      else:
        raise ValueError("rand_int requires an explicit `high` value for "
                         "non-integer types.")
    return rng.randint(low, high=high, size=shape,
                       dtype=gen_dtype).astype(dtype)
  return fn

