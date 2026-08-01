
def _operator_rtruediv(self, other):
  m = getattr(other, '__jax_array__', None)
  if m is not None:
    other = m()
  if isinstance(other, _accepted_binop_types):
    return ufuncs.true_divide(cast(ArrayLike, other), self)
  return NotImplemented


def _operator_rtruediv(a, b):
    return operator.truediv(b, a)

