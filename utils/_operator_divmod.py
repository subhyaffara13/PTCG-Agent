
def _operator_divmod(self, other):
  m = getattr(other, '__jax_array__', None)
  if m is not None:
    other = m()
  if isinstance(other, _accepted_binop_types):
    return ufuncs.divmod(self, cast(ArrayLike, other))
  return NotImplemented

