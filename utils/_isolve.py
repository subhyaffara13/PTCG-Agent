
def _isolve(_isolve_solve, A, b, x0=None, *, tol=1e-5, atol=0.0,
            maxiter=None, M=None, check_symmetric=False):
  if x0 is None:
    x0 = tree_map(jnp.zeros_like, b)

  b, x0 = api.device_put((b, x0))

  if maxiter is None:
    size = sum(bi.size for bi in tree_leaves(b))
    maxiter = 10 * size  # copied from scipy

  if M is None:
    M = _identity
  A = _normalize_matvec(A)
  M = _normalize_matvec(M)

  if tree_structure(x0) != tree_structure(b):
    raise ValueError(
        'x0 and b must have matching tree structure: '
        f'{tree_structure(x0)} vs {tree_structure(b)}')

  if _shapes(x0) != _shapes(b):
    raise ValueError(
        'arrays in x0 and b must have matching shapes: '
        f'{_shapes(x0)} vs {_shapes(b)}')

  isolve_solve = partial(
      _isolve_solve, x0=x0, tol=tol, atol=atol, maxiter=maxiter, M=M)

  # real-valued positive-definite linear operators are symmetric
  def real_valued(x):
    return not issubclass(x.dtype.type, np.complexfloating)
  symmetric = all(map(real_valued, tree_leaves(b))) \
    if check_symmetric else False
  x = lax.custom_linear_solve(
      A, b, solve=isolve_solve, transpose_solve=isolve_solve,
      symmetric=symmetric)
  info = None
  return x, info

