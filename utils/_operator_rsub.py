
def _operator_rsub(self, other):
  m = getattr(other, '__jax_array__', None)
  if m is not None:
    other = m()
  if isinstance(other, _accepted_binop_types):
    return ufuncs.subtract(cast(ArrayLike, other), self)
  return NotImplemented


def _operator_rsub(a, b):
    return operator.sub(b, a)

