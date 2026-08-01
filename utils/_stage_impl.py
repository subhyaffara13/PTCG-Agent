
def _stage_impl(x):
  # eval() must return Arrays, but the value being staged might be, e.g., a
  # literal constant.
  if not isinstance(x, core.Array):
    return dispatch.apply_primitive(stage_p, x)
  return x

