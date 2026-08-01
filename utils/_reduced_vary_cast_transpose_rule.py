
def _reduced_vary_cast_transpose_rule(cts, x, *, axes):
  assert ad.is_undefined_primal(x)
  return (vary_unreduced_cast(cts, axis_name=axes),)

