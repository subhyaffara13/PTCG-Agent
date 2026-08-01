
def _get_f_tangent(lin_jaxpr, num_residuals):
  def _f(*args):
    consts = args[:num_residuals]
    nz_tangents = args[num_residuals:]
    return core.eval_jaxpr(lin_jaxpr, consts, *nz_tangents)
  return _f

