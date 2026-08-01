
def _lu_jvp_inner(lu, a_dot, permutation):
  # Differentiation of Matrix Functionals Using Triangular Factorization
  # F. R. De Hoog, R. S. Anderssen, and M. A. Lukas
  #
  #     LU = A
  # ==> L'U + LU' = A'
  # ==> inv(L) . L' + U' . inv(U) = inv(L) A' inv(U)
  # ==> L' = L . tril(inv(L) . A' . inv(U), -1)
  #     U' = triu(inv(L) . A' . inv(U)) . U

  a_shape = np.shape(a_dot)
  assert len(a_shape) == 2
  m, n = a_shape
  dtype = lax.dtype(a_dot)
  k = min(m, n)

  l_padding = [(0, 0, 0)] * 2
  l_padding[-1] = (0, m - k, 0)
  zero = lax._const(lu, 0)
  l = lax.pad(_tril(lu[:, :k], -1), zero, l_padding)
  l = l + lax._eye(dtype, (m, m))
  u_eye = lax.pad(lax._eye(dtype, (n - k, n - k)), zero,
                  ((k, 0, 0), (k, 0, 0)))
  u_padding = [(0, 0, 0)] * 2
  u_padding[-2] = (0, n - k, 0)
  u = lax.pad(_triu(lu[:k, :]), zero, u_padding) + u_eye

  la = triangular_solve(l, a_dot[permutation], left_side=True,
                        transpose_a=False, lower=True, unit_diagonal=True)
  lau = triangular_solve(u, la, left_side=False, transpose_a=False,
                         lower=False)
  with config.default_matmul_precision("highest"):
    l_dot = l @ _tril(lau, -1)
    u_dot = _triu(lau) @ u
  return l_dot + u_dot

