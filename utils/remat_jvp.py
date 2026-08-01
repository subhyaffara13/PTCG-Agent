
def remat_jvp(primals, tangents, jaxpr, prevent_cse, differentiated, policy):
  assert not jaxpr.constvars
  in_nonzeros = [type(t) is not ad_util.Zero for t in tangents]
  jaxpr_jvp_, out_nz = ad.jvp_jaxpr(pe.close_jaxpr(jaxpr), in_nonzeros, False)
  nonzero_tangents = [t for t in tangents if type(t) is not ad_util.Zero]
  jaxpr_jvp = pe.convert_constvars_jaxpr(jaxpr_jvp_.jaxpr)
  if isinstance(prevent_cse, tuple):
    prevent_cse += (True,) * len(nonzero_tangents)
  outs = remat_p.bind(
      *jaxpr_jvp_.consts, *primals, *nonzero_tangents, jaxpr=jaxpr_jvp,
      prevent_cse=prevent_cse, differentiated=differentiated, policy=policy)
  out_primals, out_tangents_ = split_list(outs, [len(jaxpr.outvars)])
  out_tangents_ = iter(out_tangents_)
  out_tangents = [next(out_tangents_) if nz else ad_util.p2tz(p)
                  for p, nz in zip(out_primals, out_nz)]
  return out_primals, out_tangents

