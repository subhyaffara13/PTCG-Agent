
def grad_norm(dist, grad, eps=1e-8, simplex_tol=1e-9):
  """Compute norm of gradient projected onto the tangent space of simplex.

  *assumes context is gradient descent (not ascent)

  Args:
    dist: np.array, distribution
    grad: np.array, gradient (same shape as distribution)
    eps: float, elements of dist in [eps, 1 - eps] are considered to be in the
      interior of the simplex. gradients on border of simplex
    simplex_tol: float, tolerance for checking if a point lies on the simplex,
      sum(vec) <= 1 + simplex_tol and all(vec > -simplex_tol). should be smaller
      than eps descent steps or points that are "leaving" simplex will be
      mislabeled
  Returns:
    float, norm of projected gradient
  """
  if simplex_tol >= eps:
    raise ValueError("simplex_tol should be less than eps")
  grad_proj = project_grad(grad)
  g_norm = np.linalg.norm(grad_proj)
  if g_norm > 0:
    # take a gradient descent step in the direction grad_proj with len eps
    # to determine if the update is "leaving" the simplex
    dist -= eps * grad_proj / g_norm
    if not ((np.sum(dist) <= 1 + simplex_tol) and np.all(dist >= -simplex_tol)):
      g_norm = 0.
  return g_norm

