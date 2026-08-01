
def _eval_jaxpr_impl(*args, jaxpr):
  return core.jaxpr_as_fun(jaxpr)(*args)

