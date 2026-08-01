
def rand_bool(rng):
  def generator(shape, dtype):
    return _cast_to_shape(
      np.asarray(rng.rand(*_dims_of_shape(shape)) < 0.5, dtype=dtype),
      shape, dtype)
  return generator

