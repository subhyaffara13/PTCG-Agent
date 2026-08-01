
def _solve_sylvester_triangular_scan(R: Array, S: Array, F: Array) -> Array:
  """
  Solves the Sylvester equation using Bartels-Stewart algorithm
  .. math::

    RY + YS^T = F

  where R and S are upper triangular matrices following a Schur decomposition.

  Args:
    R: Matrix of shape m x m
    S: Matrix of shape n x n
    F: Matrix of shape m x n

  Returns:
    Y: Matrix of shape m x n
  """
  R, S, F = promote_args_inexact("_solve_sylvester_triangular_scan", R, S, F)

  m, n = F.shape
  total = m * n
  # scan the matrix from bottom-right to top-left
  flat_indices = jnp.arange(total - 1, -1, -1)
  Y0 = jnp.zeros((m * n,), dtype=F.dtype)

  def scan_fn(Y_flat, idx):
    i = idx // n
    j = idx % n
    Y = Y_flat.reshape((m, n))
    rhs = F[i, j]

    # Row term: gets contributions from R and already filled in Y. mask ensures that we only get non-zero elements from R because it is upper triangular
    k_row = jnp.arange(m)
    row_mask = k_row > i
    r_row = R[i, :]
    y_col = Y[:, j]
    row_term = jnp.sum(jnp.where(row_mask, r_row * y_col, 0.0))

    # Col term: same as Row term but now uses S instead of R.
    k_col = jnp.arange(n)
    col_mask = k_col > j
    y_row = Y[i, :]
    s_col = S[:, j]
    col_term = jnp.sum(jnp.where(col_mask, y_row * s_col, 0.0))

    # Here we are solving for the current Y[i, j]
    rhs -= row_term + col_term
    val = rhs / (R[i, i] + S[j, j])

    Y_flat = Y_flat.at[i * n + j].set(val)
    return Y_flat, None

  Y_flat_final, _ = lax.scan(scan_fn, Y0, flat_indices)
  return Y_flat_final.reshape((m, n))

