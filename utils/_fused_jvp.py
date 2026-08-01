
def _fused_jvp(primals, tangents, *, jaxpr, out_spaces):
  nzs = [not isinstance(t, ad.Zero) for t in tangents]
  jaxpr_jvp, out_nzs = ad.jvp_jaxpr(jaxpr, nzs, False)
  nz_tangents = [t for t in tangents if not isinstance(t, ad.Zero)]
  spaces_jvp = (*out_spaces, *[s for s, nz in zip(out_spaces, out_nzs) if nz])
  outs = fused_p.bind(*primals, *nz_tangents, jaxpr=jaxpr_jvp,
                      out_spaces=spaces_jvp)
  primals_out, nz_tangents_out = outs[:len(out_nzs)], outs[len(out_nzs):]
  nz_outs = iter(nz_tangents_out)
  tangents_out = [next(nz_outs) if nz else ad.Zero(aval.to_tangent_aval())
                  for aval, nz in zip(jaxpr.out_avals, out_nzs)]
  assert next(nz_outs, None) is None
  return primals_out, tangents_out

