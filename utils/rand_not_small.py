
def rand_not_small(rng, offset=10.):
  post = lambda x: x + np.where(x > 0, offset, -offset)
  return partial(_rand_dtype, rng.randn, scale=3., post=post)

