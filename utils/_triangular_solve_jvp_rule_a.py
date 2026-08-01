
def _triangular_solve_jvp_rule_a(
    g_a, ans, a, b, *, left_side, lower, transpose_a, conjugate_a,
    unit_diagonal):
  m, n = b.shape[-2:]
  k = 1 if unit_diagonal else 0
  g_a = _tril(g_a, k=-k) if lower else _triu(g_a, k=k)
  g_a = lax.neg(g_a)
  g_a = _T(g_a) if transpose_a else g_a
  g_a = g_a.conj() if conjugate_a else g_a
  dot = partial(lax.dot if g_a.ndim == 2 else lax.batch_matmul,
                precision=lax.Precision.HIGHEST)

  def a_inverse(rhs):
    return triangular_solve(a, rhs, left_side=left_side, lower=lower,
                            transpose_a=transpose_a, conjugate_a=conjugate_a,
                            unit_diagonal=unit_diagonal)

  # triangular_solve is about the same cost as matrix multiplication (~n^2 FLOPs
  # for matrix/vector inputs). Order these operations in whichever order is
  # cheaper.
  if left_side:
    assert g_a.shape[-2:] == a.shape[-2:] == (m, m) and ans.shape[-2:] == (m, n)
    if m > n:
      return a_inverse(dot(g_a, ans))  # A^{-1} (∂A X)
    else:
      return dot(a_inverse(g_a), ans)  # (A^{-1} ∂A) X
  else:
    assert g_a.shape[-2:] == a.shape[-2:] == (n, n) and ans.shape[-2:] == (m, n)
    if m < n:
      return a_inverse(dot(ans, g_a))  # (X ∂A) A^{-1}
    else:
      return dot(ans, a_inverse(g_a))  # X (∂A A^{-1})

