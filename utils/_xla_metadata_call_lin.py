
def _xla_metadata_call_lin(is_vjp, nzs, *primals, jaxpr, **meta):
  (primal_jaxpr, num_residuals_out, nzs_out, in_fwd_res,
   tangent_jaxpr) = ad.linearize_jaxpr(jaxpr, nzs, is_vjp=is_vjp)

  tangent_avals_out = [a.to_tangent_aval() for a in jaxpr.out_avals]

  def _filter_zeros(is_nz_l, l):
    return tuple(x for nz, x in zip(is_nz_l, l) if nz)

  def tangent_fun(residuals, *tangents):
    tangents_nz = _filter_zeros(nzs, tangents)
    assert len(residuals) + len(tangents_nz) == len(tangent_jaxpr.invars), (
        len(residuals), len(tangents_nz), len(tangent_jaxpr.invars))
    nz_outs = xla_metadata_call_p.bind(*residuals, *tangents_nz,
                                       jaxpr=tangent_jaxpr, **meta)
    nz_outs_ = iter(nz_outs)
    outs = [next(nz_outs_) if nz else ad.Zero(a)
            for nz, a in zip(nzs_out, tangent_avals_out)]
    assert next(nz_outs_, None) is None
    return outs

  ans = xla_metadata_call_p.bind(*primals, jaxpr=primal_jaxpr, **meta)
  primal_ans, residuals_ans = split_list(ans, [len(ans) - num_residuals_out])
  residuals_ans = subs_list(in_fwd_res, [*jaxpr.consts, *primals], residuals_ans)
  return primal_ans, nzs_out, residuals_ans, tangent_fun

