
def _pjit_linearize(is_vjp, nzs, *primals_in, jaxpr, in_shardings, out_shardings,
                    in_layouts, out_layouts, donated_invars, ctx_mesh, name,
                    keep_unused, inline, compiler_options_kvs):
  (primal_jaxpr, num_residuals_out, nzs_out, in_fwd_res,
   tangent_jaxpr) = ad.linearize_jaxpr(jaxpr, nzs, is_vjp=is_vjp)
  num_residuals_in = len(in_fwd_res)
  num_primals_out = len(primal_jaxpr.out_avals) - num_residuals_out

  res_shardings_in = (UNSPECIFIED,) * num_residuals_in
  res_layouts_in = (None,) * num_residuals_in
  res_donated = (False,) * num_residuals_in
  primal_out_shardings = tuple(out_shardings) + (UNSPECIFIED,) * num_residuals_out
  primal_out_layouts = tuple(out_layouts) + (None,) * num_residuals_out

  config.enable_checks.value and core.check_jaxpr(primal_jaxpr.jaxpr)
  config.enable_checks.value and core.check_jaxpr(tangent_jaxpr.jaxpr)

  def keep_where(l, should_keep):
    return tuple(x for x, keep in zip(l, should_keep) if keep)

  # Input-to-output forwarding.
  in_fwd = pe._jaxpr_forwarding(primal_jaxpr.jaxpr)
  in_fwd_primal, in_fwd_res_ = split_list(in_fwd, [num_primals_out])
  assert all(f is None for f in in_fwd_res_)
  in_fwd = [
      fwd if isinstance(os, UnspecifiedValue) and ol is None else None
      for os, ol, fwd in zip(out_shardings, out_layouts, in_fwd_primal)
  ] + in_fwd_res_
  del in_fwd_res_, in_fwd_primal
  keep = [f is None for f in in_fwd]
  primal_jaxpr = pe.prune_closed_jaxpr_outputs(primal_jaxpr, keep)
  primal_out_shardings = keep_where(primal_out_shardings, keep)
  primal_out_layouts = keep_where(primal_out_layouts, keep)
  _, kept_res = split_list(keep, [num_primals_out])
  num_kept_residuals = sum(kept_res)
  del keep, kept_res, num_primals_out

  # Output-to-output forwarding.
  num_primals_out = len(primal_jaxpr.out_avals) - num_kept_residuals
  out_vars, res_vars = split_list(primal_jaxpr.jaxpr.outvars, [num_primals_out])
  idx_map = {id(v): i for i, v in enumerate(out_vars)}
  out_fwd = [None] * num_primals_out + [idx_map.get(id(v)) for v in res_vars]
  keep = [f is None for f in out_fwd]
  primal_jaxpr = pe.prune_closed_jaxpr_outputs(primal_jaxpr, keep)
  primal_out_shardings = keep_where(primal_out_shardings, keep)
  primal_out_layouts = keep_where(primal_out_layouts, keep)
  del keep

  tangent_avals_out = [a.to_tangent_aval() for a in jaxpr.out_avals]

  def tangent_fun(residuals, *tangents):
    tangents_nz = _filter_zeros(nzs, tangents)
    nz_tangents_out = jit_p.bind(
        *residuals, *tangents_nz, jaxpr=tangent_jaxpr,
        in_shardings=res_shardings_in + _filter_zeros(nzs, in_shardings),
        out_shardings=_filter_zeros(nzs_out, out_shardings),
        in_layouts=res_layouts_in + _filter_zeros(nzs, in_layouts),
        out_layouts=_filter_zeros(nzs_out, out_layouts),
        donated_invars=res_donated + _filter_zeros(nzs, donated_invars),
        ctx_mesh=ctx_mesh,
        name=name,
        keep_unused=keep_unused,
        inline=inline,
        compiler_options_kvs=compiler_options_kvs)
    nz_tangents_out_ = iter(nz_tangents_out)
    tangents_out = [next(nz_tangents_out_) if nz else ad.Zero(aval)
                   for (aval, nz) in zip(tangent_avals_out, nzs_out)]
    assert next(nz_tangents_out_, None) is None
    return tangents_out

  def _filter_zeros(is_nz_l, l):
    return tuple(x for nz, x in zip(is_nz_l, l) if nz)

  assert len(in_shardings) == len(primal_jaxpr.in_avals)
  ans = jit_p.bind(*primals_in, jaxpr=primal_jaxpr,
                   in_shardings=in_shardings,
                   out_shardings=primal_out_shardings,
                   in_layouts=in_layouts,
                   out_layouts=primal_out_layouts,
                   donated_invars=donated_invars,
                   ctx_mesh=ctx_mesh,
                   name=name,
                   keep_unused=keep_unused,
                   inline=inline,
                   compiler_options_kvs=compiler_options_kvs)
  ans = subs_list(out_fwd, ans, ans)
  ans = subs_list(in_fwd, primals_in, ans)
  primal_ans, residuals_ans = split_list(ans, [len(ans) - num_residuals_out])
  residuals_ans = subs_list(in_fwd_res, [*jaxpr.consts, *primals_in], residuals_ans)
  return primal_ans, nzs_out, residuals_ans, tangent_fun

