
def rand_default(rng, scale=3):
  return partial(_rand_dtype, rng.randn, scale=scale)

