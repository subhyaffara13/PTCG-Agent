
def _cholesky_jvp_rule(primals, tangents):
  x, = primals
  sigma_dot, = tangents
  L = _tril(cholesky_p.bind(x))

  # Forward-mode rule from https://arxiv.org/pdf/1602.07527.pdf
  def phi(X):
    l = _tril(X)
    return l / lax.expand_dims(
        lax._const(X, 1) + lax._eye(X.dtype, (X.shape[-1], X.shape[-1])),
        range(l.ndim - 2))

  tmp = triangular_solve(L, sigma_dot, left_side=False, transpose_a=True,
                         conjugate_a=True, lower=True)
  L_dot = lax.batch_matmul(L, phi(triangular_solve(
      L, tmp, left_side=True, transpose_a=False, lower=True)),
      precision=lax.Precision.HIGHEST)
  return L, L_dot

