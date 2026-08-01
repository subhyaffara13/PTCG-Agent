
def _create_linear_abstract_eval(*, ty, memory_space):
  if not isinstance(ty, core.ShapedArray): raise NotImplementedError(ty)
  return AbstractLinVal(ty, memory_space)

