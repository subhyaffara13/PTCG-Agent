
def _use_cholesky(u, m, n, params):
  """QDWH iteration using Cholesky decomposition.

  Args:
  u: a matrix, with static (padded) shape M x N
  m, n: the dynamic shape of the matrix, where m <= M and n <= N.
  params: the QDWH parameters.
  """
  a_minus_e, c, e = params
  _, N = u.shape
  x = c * (u.T.conj() @ u) + jnp.eye(N, dtype=dtypes.dtype(u))
  # Pads the lower-right corner with the identity matrix to prevent the Cholesky
  # decomposition from failing due to the matrix not being PSD if padded with
  # zeros.
  x = _mask(x, (n, n), jnp.eye(N, dtype=x.dtype))

  # `y` is lower triangular.
  y = lax_linalg.cholesky(x, symmetrize_input=False)

  z = lax_linalg.triangular_solve(
      y, u.T, left_side=True, lower=True, conjugate_a=True).conj()

  z = lax_linalg.triangular_solve(y, z, left_side=True, lower=True,
                                  transpose_a=True, conjugate_a=True).T.conj()

  return e * u + a_minus_e * z

