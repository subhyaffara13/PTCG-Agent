
def project_to_interior(x, eps):
  """Project x onto interior of simplex.

  Args:
    x: np.array of shape (dim,)
    eps: float, ensure x remains at least eps / dim away from facets of simplex
  Returns:
    np.array, distribution x with min(x) >= eps / dim
  """
  min_x = np.min(x)
  d = len(x)
  if min_x < eps / d:
    t = (eps / d - min_x) / (1. / d - min_x)
    x = x * (1 - t) + 1 / d * t
  return x

