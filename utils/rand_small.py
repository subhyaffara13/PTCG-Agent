
def rand_small(rng):
  return partial(_rand_dtype, rng.randn, scale=1e-3)

