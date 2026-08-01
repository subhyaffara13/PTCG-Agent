
def _compute_on_lin(is_vjp, nzs, *primals, jaxpr, compute_type,
                    out_memory_spaces, compiler_options_json):
  (primal_jaxpr, num_res_out, nzs_out, in_fwd_res,
   tangent_jaxpr) = ad.linearize_jaxpr(jaxpr, nzs, is_vjp=is_vjp)

  tangent_avals_out = [a.to_tangent_aval() for a in jaxpr.out_avals]
  def _filter_zeros(is_nz_l, l):
    return tuple(x for nz, x in zip(is_nz_l, l) if nz)

  def tangent_fun(residuals, *tangents):
    tangents_nz = _filter_zeros(nzs, tangents)
    assert len(residuals) + len(tangents_nz) == len(tangent_jaxpr.invars), (
        len(residuals), len(tangents_nz), len(tangent_jaxpr.invars))
    tangent_out_mem_spaces = _filter_zeros(nzs_out, out_memory_spaces)
    nz_outs = compute_on_p.bind(*residuals, *tangents_nz,
                                jaxpr=tangent_jaxpr, compute_type=compute_type,
                                out_memory_spaces=tangent_out_mem_spaces,
                                compiler_options_json=compiler_options_json)
    nz_outs_ = iter(nz_outs)
    outs = [next(nz_outs_) if nz else ad.Zero(a)
            for nz, a in zip(nzs_out, tangent_avals_out)]
    assert next(nz_outs_, None) is None
    return outs

  primal_out_mem_spaces = out_memory_spaces + (core.MemorySpace.Device,) * num_res_out
  ans = compute_on_p.bind(*primals, jaxpr=primal_jaxpr, compute_type=compute_type,
                          out_memory_spaces=primal_out_mem_spaces,
                          compiler_options_json=compiler_options_json)
  primal_ans, residuals_ans = split_list(ans, [len(ans) - num_res_out])
  residuals_ans = subs_list(in_fwd_res, [*jaxpr.consts, *primals], residuals_ans)
  return primal_ans, nzs_out, residuals_ans, tangent_fun

