
def _triangular_solve_transpose_rule(
    cotangent, a, b, *, left_side, lower, transpose_a, conjugate_a,
    unit_diagonal):
  # Triangular solve is nonlinear in its first argument and linear in its second
  # argument, analogous to `div` but swapped.
  assert not ad.is_undefined_primal(a) and ad.is_undefined_primal(b)
  if type(cotangent) is ad_util.Zero:
    cotangent_b = ad_util.Zero(b.aval)
  else:
    cotangent_b = triangular_solve(a, cotangent, left_side=left_side,
                                   lower=lower, transpose_a=not transpose_a,
                                   conjugate_a=conjugate_a,
                                   unit_diagonal=unit_diagonal)
  return [None, cotangent_b]

