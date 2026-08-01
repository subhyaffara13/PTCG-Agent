
def _dynamic_slice_ur_rule(operand, *starts_and_dyn_sizes, slice_sizes):
  if core.getu(operand):
    raise NotImplementedError(
        'unreduced rule for dynamic_slice is not implemented. Please'
        ' file an issue at https://github.com/jax-ml/jax/issues')
  return frozenset(), core.getr(operand)

