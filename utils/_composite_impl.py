
def _composite_impl(*args, jaxpr, **_):
  return core.jaxpr_as_fun(jaxpr)(*args)

