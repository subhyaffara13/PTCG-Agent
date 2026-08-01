
def _gmres_incremental(A, b, x0, unit_residual, residual_norm, ptol, restart, M):
  """
  Implements a single restart of GMRES. The restart-dimensional Krylov subspace
  K(A, x0) = span(A(x0), A@x0, A@A@x0, ..., A^restart @ x0) is built, and the
  projection of the true solution into this subspace is returned.

  This implementation builds the QR factorization during the Arnoldi process.
  """
  # https://www-users.cs.umn.edu/~saad/Calais/PREC.pdf

  V = tree_map(
      lambda x: jnp.pad(x[..., None], ((0, 0),) * x.ndim + ((0, restart),)),
      unit_residual,
  )
  dtype = dtypes.result_type(*tree_leaves(b))
  # use eye() to avoid constructing a singular matrix in case of early
  # termination
  R = jnp.eye(restart, restart + 1, dtype=dtype)

  givens = jnp.zeros((restart, 2), dtype=dtype)
  beta_vec = jnp.zeros((restart + 1), dtype=dtype)
  beta_vec = beta_vec.at[0].set(residual_norm.astype(dtype))

  def loop_cond(carry):
    k, err, _, _, _, _ = carry
    return jnp.logical_and(k < restart, err > ptol)

  def arnoldi_qr_step(carry):
    k, _, V, R, beta_vec, givens = carry
    V, H, _ = _kth_arnoldi_iteration(k, A, M, V, R)
    R_row, givens = _apply_givens_rotations(H[k, :], givens, k)
    R = R.at[k, :].set(R_row)
    beta_vec = _rotate_vectors(beta_vec, k, *givens[k, :])
    err = abs(beta_vec[k + 1])
    return k + 1, err, V, R, beta_vec, givens

  carry = (0, residual_norm, V, R, beta_vec, givens)
  carry = lax.while_loop(loop_cond, arnoldi_qr_step, carry)
  k, residual_norm, V, R, beta_vec, _ = carry
  del k  # Until we figure out how to pass this to the user.

  y = jsp_linalg.solve_triangular(R[:, :-1].T, beta_vec[:-1])
  dx = tree_map(lambda X: _dot(X[..., :-1], y), V)

  x = _add(x0, dx)
  residual = M(_sub(b, A(x)))
  unit_residual, residual_norm = _safe_normalize(residual)
  # TODO(shoyer): "Inner loop tolerance control" on ptol, like SciPy
  return x, unit_residual, residual_norm

