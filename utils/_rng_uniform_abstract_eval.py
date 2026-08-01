
def _rng_uniform_abstract_eval(a, b, *, shape):
  if a.dtype != b.dtype:
    raise ValueError(
      "Arguments to rng_uniform must have identical dtypes, got {} "
      "and {}.".format(a.dtype, b.dtype))
  if a.shape != () or b.shape != ():
    raise ValueError(
      "Arguments to rng_uniform must be scalars; got shapes {} and {}."
      .format(a.shape, b.shape))
  return a.update(shape=shape, dtype=a.dtype,
                  weak_type=(a.weak_type and b.weak_type))

