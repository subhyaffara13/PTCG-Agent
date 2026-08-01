
def _eval_jaxpr_jvp(primals, tangents, *, jaxpr):
  nonzeros = [type(t) is not ad_util.Zero for t in tangents]
  jaxpr_jvp, nonzeros_out = ad.jvp_jaxpr(jaxpr, nonzeros, False)
  nz_tangents = [t for t, nz in zip(tangents, nonzeros) if nz]
  outs = eval_jaxpr_p.bind(*primals, *nz_tangents, jaxpr=jaxpr_jvp)
  primals_out, tangents_out = split_list(outs, [len(jaxpr.out_avals)])
  nz_tangents_out = iter(tangents_out)
  tangents_out = [next(nz_tangents_out) if nz else ad_util.Zero(aval.to_tangent_aval())
                  for aval, nz in zip(jaxpr.out_avals, nonzeros_out)]
  return primals_out, tangents_out

