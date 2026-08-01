
def uniform_dist(x):
  """Returns a uniform distribution with same shape as the given numpy array.

  Args:
    x: numpy array
  Returns:
    constant numpy array of same shape as input x, sums to 1
  """
  return np.ones_like(x) / float(x.size)

