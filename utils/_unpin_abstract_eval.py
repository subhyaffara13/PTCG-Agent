
def _unpin_abstract_eval(aval):
  if not isinstance(aval, AbstractLinVal): raise TypeError(aval)
  return aval.inner_aval

