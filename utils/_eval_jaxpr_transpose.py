
def _eval_jaxpr_transpose(ct, *args, jaxpr):
  jaxpr_, consts = jaxpr.jaxpr, jaxpr.consts
  jaxpr_ = pe.convert_constvars_jaxpr(jaxpr_)
  ad.call_transpose_fancy(core.closed_call_p, ct, *consts, *args,
                          call_jaxpr=jaxpr_)

