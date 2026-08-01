
def _tridiagonal_solve_jvp_rule(primals, tangents, *, perturb_singular):
  *diags, _ = primals
  *diags_dot, b_dot = tangents
  ans = tridiagonal_solve_p.bind(*primals, perturb_singular=perturb_singular)
  if all(type(p) is ad_util.Zero for p in diags_dot):
    rhs = b_dot
  else:
    # pyrefly: ignore[bad-argument-count]  # pyrefly#2468
    matvec_dot = _tridiagonal_product(*map(ad.instantiate_zeros, diags_dot), ans)
    rhs = ad.add_tangents(b_dot, -matvec_dot)
  ans_dot = tridiagonal_solve_p.bind(
    *diags, rhs, perturb_singular=perturb_singular)
  return ans, ans_dot

