
def rand_nonzero(rng):
  post = lambda x: np.where(x == 0, np.array(1, dtype=x.dtype), x)
  return partial(_rand_dtype, rng.randn, scale=3, post=post)

