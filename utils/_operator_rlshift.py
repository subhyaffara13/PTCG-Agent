
def _operator_rlshift(self, other):
  m = getattr(other, '__jax_array__', None)
  if m is not None:
    other = m()
  if isinstance(other, _accepted_binop_types):
    return ufuncs.left_shift(cast(ArrayLike, other), self)
  return NotImplemented

