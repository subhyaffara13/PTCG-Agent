
def _vary_unreduced_cast_transpose_rule(cts, x, *, axes):
  assert ad.is_undefined_primal(x)
  return (core.reduced_vary_cast(cts, axis_name=axes),)

