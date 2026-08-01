
def rand_small_positive(rng):
  return partial(_rand_dtype, rng.rand, scale=2e-5)

