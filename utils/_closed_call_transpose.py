
def _closed_call_transpose(ct, *args, call_jaxpr, **params):
  jaxpr_, consts = call_jaxpr.jaxpr, call_jaxpr.consts
  jaxpr_ = pe.convert_constvars_jaxpr(jaxpr_)
  call_transpose_fancy(core.closed_call_p, ct, *consts, *args,
                       call_jaxpr=jaxpr_, **params)

