
def euclidean_projection_onto_simplex(y, eps=1e-3, subset=True):
  """O(n log n) Euclidean projection of y onto the simplex.

  Args:
    y: np.array
    eps: float, ensure x remains at least eps / dim away from facets of simplex
    subset: bool, whether to project onto a subset of the simplex defined by eps
  Returns:
    np.array, y projected onto the simplex
  """
  if np.all(y >= 0.) and np.abs(np.sum(y) - 1.) < 1e-8:
    return y
  d = len(y)
  u = sorted(y, reverse=True)
  sum_uj = 0.
  rho = 0.
  for j in range(d):
    sum_uj += u[j]
    tj = (1. - sum_uj) / (j + 1.)
    if u[j] + tj <= 0:
      rho = j - 1
      sum_uj = sum_uj - u[j]
      break
    else:
      rho = j
  lam = (1. - sum_uj) / (rho + 1.)
  x = np.array([max(y[i] + lam, 0.) for i in range(d)])
  if subset:
    scale = 1. - eps * float(d + 1) / d
    offset = eps / float(d)
    x = scale * x + offset
    x /= x.sum()
  return x

