
def _eval_jaxpr_linearize(is_vjp, nzs, *primals_in, jaxpr):
  lin_out = ad.linearize_jaxpr(jaxpr, nzs, is_vjp=is_vjp)
  primal_jaxpr, num_res_out, nzs_out, in_fwd_res, tangent_jaxpr = lin_out
  primals_and_res = eval_jaxpr_p.bind(*primals_in, jaxpr=primal_jaxpr)
  primals_out, non_fwd_res = split_list(
      primals_and_res, [len(primals_and_res) - num_res_out])
  res = subs_list(in_fwd_res, [*jaxpr.consts, *primals_in], non_fwd_res)

  def tangent_fun(res, *tangents):
    nz_tangents = [ad.instantiate_zeros(x) for nz, x in zip(nzs, tangents) if nz]
    nz_tangents_out = eval_jaxpr_p.bind(*res, *nz_tangents, jaxpr=tangent_jaxpr)
    tangent_avals_out = [v.aval.to_tangent_aval() for v in jaxpr.jaxpr.outvars]
    nz_tangents_out_ = iter(nz_tangents_out)
    tangents_out = [next(nz_tangents_out_) if nz else ad_util.Zero(aval)
                    for aval, nz in zip(tangent_avals_out, nzs_out)]
    assert next(nz_tangents_out_, None) is None
    return tangents_out

  return primals_out, nzs_out, res, tangent_fun

