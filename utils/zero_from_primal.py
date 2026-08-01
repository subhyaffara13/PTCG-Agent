
def zero_from_primal(val, symbolic_zeros=False):
  def f(x):
    t_aval = typeof(x).to_tangent_aval()
    return SymbolicZero(t_aval) if symbolic_zeros else zeros_like_aval(t_aval)
  return tree_map(f, val)

