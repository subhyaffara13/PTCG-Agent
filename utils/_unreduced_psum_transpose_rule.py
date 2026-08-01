
def _unreduced_psum_transpose_rule(cts, arg, *, axes):
  assert ad.is_undefined_primal(arg)
  return (preduced(cts, axis_name=axes),)

