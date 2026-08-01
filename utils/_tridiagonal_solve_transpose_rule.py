
def _tridiagonal_solve_transpose_rule(
    cotangent, dl, d, du, b, *, perturb_singular):
  # Tridiagonal solve is nonlinear in the tridiagonal arguments and linear
  # otherwise.
  assert not (ad.is_undefined_primal(dl) or ad.is_undefined_primal(d) or
              ad.is_undefined_primal(du)) and ad.is_undefined_primal(b)
  if type(cotangent) is ad_util.Zero:
    cotangent_b = ad_util.Zero(b.aval)
  else:
    dl_trans = lax.concatenate((lax.full_like(du[..., -1:], 0), du[..., :-1]),
                               du.ndim-1)
    du_trans = lax.concatenate((dl[..., 1:], lax.full_like(dl[..., :1], 0)),
                               dl.ndim-1)
    cotangent_b = tridiagonal_solve(dl_trans, d, du_trans, cotangent,
                                    perturb_singular=perturb_singular)
  return [None, None, None, cotangent_b]

