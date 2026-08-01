
def _preduced_transpose_rule(cts, arg, *, axes):
  assert ad.is_undefined_primal(arg)
  return (unreduced_psum(cts, axis_name=axes),)

