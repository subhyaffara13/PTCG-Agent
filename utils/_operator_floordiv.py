
def _operator_floordiv(self, other):
  m = getattr(other, '__jax_array__', None)
  if m is not None:
    other = m()
  if isinstance(other, _accepted_binop_types):
    return ufuncs.floor_divide(self, cast(ArrayLike, other))
  return NotImplemented

