
def _pvary_transpose_rule(cts, arg, *, axes):
  assert ad.is_undefined_primal(arg)
  return (psum_invariant_p.bind(cts, axes=axes),)

