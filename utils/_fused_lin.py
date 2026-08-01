
def _fused_lin(_is_vjp, nzs, *primals, jaxpr, out_spaces):
  # TODO(mattjj): why did i do jvp + dce here, not ad.linearize_jaxpr?
  jaxpr_jvp, out_nzs = ad.jvp_jaxpr(jaxpr, nzs, False)
  lin_outs = [False] * len(out_nzs) + [True] * sum(out_nzs)
  jaxpr_lin_, used_inputs = pe.dce_jaxpr(jaxpr_jvp.jaxpr, lin_outs, False)
  jaxpr_lin = pe.close_jaxpr(jaxpr_lin_)
  spaces_lin = tuple(s for s, nz in zip(out_spaces, out_nzs) if nz)
  primals_out = fused_p.bind(*primals, jaxpr=jaxpr, out_spaces=out_spaces)
  tangent_avals_out = [a.to_tangent_aval() for a in jaxpr.out_avals]

  def fused_lin(primals, *tangents):
    nz_tangents = [t for t in tangents if not isinstance(t, ad.Zero)]
    inputs = [x for x, u in zip([*primals, *nz_tangents], used_inputs) if u]
    nz_outs = fused_p.bind(*inputs, jaxpr=jaxpr_lin, out_spaces=spaces_lin)
    nz_outs_ = iter(nz_outs)
    outs = [next(nz_outs_) if nz else ad.Zero(a)
            for nz, a in zip(out_nzs, tangent_avals_out)]
    assert next(nz_outs_, None) is None
    return outs

  return primals_out, out_nzs, primals, fused_lin

