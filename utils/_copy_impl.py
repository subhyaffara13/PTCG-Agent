
def _copy_impl(prim, *args, **kwargs):
  return dispatch.apply_primitive(prim, *args, **kwargs)

