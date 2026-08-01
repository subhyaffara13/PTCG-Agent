
def _cond_linearize(is_vjp, nzs, *primals_in, branches, **params):
  idx_nz, *nzs = nzs
  assert not idx_nz
  nzs_out = [ad.linearize_jaxpr(jaxpr, nzs, allow_fwds=False, is_vjp=is_vjp)[2]
             for jaxpr in branches]
  nzs_out = map(any, zip(*nzs_out))
  primal_jaxprs, tangent_jaxprs, branch_res_avals = [], [], []
  for jaxpr in branches:
    primal_jaxpr, num_res_out, _, _, tangent_jaxpr = \
        ad.linearize_jaxpr(jaxpr, nzs, instantiate=nzs_out, allow_fwds=False, is_vjp=is_vjp)
    res_avals = primal_jaxpr.out_avals[len(primal_jaxpr.out_avals)-num_res_out:]
    primal_jaxprs.append(primal_jaxpr)
    tangent_jaxprs.append(tangent_jaxpr)
    branch_res_avals.append(res_avals)

  all_res_avals, res_avals_per_branch = _merge_branch_residuals(branch_res_avals)
  primal_jaxprs = _join_cond_outputs(
      primal_jaxprs, all_res_avals, res_avals_per_branch, len(nzs_out))
  tangent_jaxprs = _join_cond_pe_staged_jaxpr_inputs(
      tangent_jaxprs, all_res_avals, res_avals_per_branch)
  tangent_avals_out = [a.to_tangent_aval() for a in jaxpr.out_avals]

  primals_res_out = cond_p.bind(*primals_in, branches=primal_jaxprs, **params)
  primals, res = split_list(primals_res_out, [len(nzs_out)])

  def tangent_fun(res, *tangents_in):
    nz_tangents_in = [t for t in tangents_in if not isinstance(t, ad.Zero)]
    nz_tangents_out = cond_p.bind(*res, *nz_tangents_in,
                                  branches=tangent_jaxprs, **params)
    nz_tangents_out_ = iter(nz_tangents_out)
    tangents_out = [next(nz_tangents_out_) if nz else ad.Zero(aval)
                   for (aval, nz) in zip(tangent_avals_out, nzs_out)]
    assert next(nz_tangents_out_, None) is None
    return tangents_out

  idx, *_ = primals_in
  return primals, nzs_out, [idx, *res], tangent_fun

