
def rand_uniform(rng, low=0.0, high=1.0):
  assert low < high
  post = lambda x: x * (high - low) + low
  return partial(_rand_dtype, rng.rand, post=post)

