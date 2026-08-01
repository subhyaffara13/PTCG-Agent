
def _operator_ror(self, other):
  m = getattr(other, '__jax_array__', None)
  if m is not None:
    other = m()
  if isinstance(other, _accepted_binop_types):
    return ufuncs.bitwise_or(cast(ArrayLike, other), self)
  return NotImplemented

