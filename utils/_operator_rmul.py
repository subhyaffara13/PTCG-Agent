
def _operator_rmul(self, other):
  m = getattr(other, '__jax_array__', None)
  if m is not None:
    other = m()
  if isinstance(other, _accepted_binop_types):
    return ufuncs.multiply(cast(ArrayLike, other), self)
  # Explicitly reject sequences where __mul__ may indicate concatenation.
  # Avoid isinstance so as to not catch subclasses like NamedTuple.
  if type(other) in (tuple, list):
    raise TypeError(f"unsupported operand type(s) for *: "
                    f"{type(other).__name__!r} and {type(self).__name__!r}")
  return NotImplemented

