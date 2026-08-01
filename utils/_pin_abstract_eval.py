
def _pin_abstract_eval(aval, *, to):
  if to not in (None, 'hbm', 'vmem'): raise ValueError
  if not isinstance(aval, core.ShapedArray): raise NotImplementedError(aval)
  return AbstractLinVal(aval, to)

