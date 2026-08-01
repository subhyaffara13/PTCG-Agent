
def rand_some_equal(rng):

  def post(x):
    x_ravel = x.ravel()
    if len(x_ravel) == 0:
      return x
    flips = rng.rand(*np.shape(x)) < 0.5
    return np.where(flips, x_ravel[0], x)

  return partial(_rand_dtype, rng.randn, scale=100., post=post)

