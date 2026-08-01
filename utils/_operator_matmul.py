
def _operator_matmul(self, other):
  m = getattr(other, '__jax_array__', None)
  if m is not None:
    other = m()
  if isinstance(other, _accepted_binop_types):
    return tensor_contractions.matmul(self, cast(ArrayLike, other))
  return NotImplemented

