
def _custom_jvp_call_transpose_fancy(params, jaxpr, args, ct, _):
  del params
  return ad.backward_pass3(jaxpr.jaxpr, False, jaxpr.consts, args, ct)

