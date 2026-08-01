
def _psum_invariant_transpose_rule(cts, arg, *, axes):
  assert ad.is_undefined_primal(arg)
  return (core.pvary(cts, axis_name=axes),)

