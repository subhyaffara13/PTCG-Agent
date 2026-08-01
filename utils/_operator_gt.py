
def _operator_gt(self, other):
  m = getattr(other, '__jax_array__', None)
  if m is not None:
    other = m()
  if isinstance(other, _accepted_binop_types):
    return ufuncs.greater(self, cast(ArrayLike, other))
  return NotImplemented

