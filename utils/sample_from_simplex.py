
def sample_from_simplex(n, dim=3, vmin=0.):
  """Samples random points from a k-simplex.

  See Donald B. Rubin (1981) "The Bayesian Bootstrap", page 131.

  Args:
    n: Number of points that are sampled.
    dim: Dimension of the points to be sampled, e.g. dim=3 samples points from
      the 2-simplex.
    vmin: Minimum value of any coordinate of the resulting points, e.g. set
      vmin>0. to exclude points on the faces of the simplex.

  Returns:
    `ndarray(shape=(k, dim))` of uniformly random points on the (num-1)-simplex.
  """
  assert vmin >= 0.
  p = np.random.rand(n, dim - 1)
  p = np.sort(p, axis=1)
  p = np.hstack((np.zeros((n, 1)), p, np.ones((n, 1))))
  return (p[:, 1:] - p[:, 0:-1]) * (1 - 2 * vmin) + vmin

