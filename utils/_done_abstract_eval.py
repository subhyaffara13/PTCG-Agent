
def _done_abstract_eval(aval):
  if not isinstance(aval, core.AbstractFuture):
    raise TypeError(f"async done op got {aval}, want core.AbstractFuture")
  return aval.inner_aval

