
def rand_fullrange(rng, standardize_nans=False):
  """Random numbers that span the full range of available bits."""
  def gen(shape, dtype, post=lambda x: x):
    dtype = np.dtype(dtype)
    size = dtype.itemsize * math.prod(_dims_of_shape(shape))
    vals = rng.randint(0, np.iinfo(np.uint8).max, size=size, dtype=np.uint8)
    vals = post(vals).view(dtype)
    if shape is PYTHON_SCALAR_SHAPE:
      # Sampling from the full range of the largest available uint type
      # leads to overflows in this case; sample from signed ints instead.
      if dtype == np.uint64:
        vals = vals.astype(np.int64)
      elif dtype == np.uint32 and not config.enable_x64.value:
        vals = vals.astype(np.int32)
    vals = vals.reshape(shape)
    # Non-standard NaNs cause errors in numpy equality assertions.
    if standardize_nans and np.issubdtype(dtype, np.floating):
      vals[np.isnan(vals)] = np.nan
    return _cast_to_shape(vals, shape, dtype)
  return gen

