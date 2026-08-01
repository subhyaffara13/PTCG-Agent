
def rand_positive(rng):
  post = lambda x: x + 1
  return partial(_rand_dtype, rng.rand, scale=2, post=post)

