
def _operator_add(self, other):
  m = getattr(other, '__jax_array__', None)
  if m is not None:
    other = m()
  if isinstance(other, _accepted_binop_types):
    return ufuncs.add(self, cast(ArrayLike, other))
  # Explicitly reject sequences where __add__ may indicate concatenation.
  # Avoid isinstance so as to not catch subclasses like NamedTuple.
  if type(other) in (tuple, list):
    raise TypeError(f"unsupported operand type(s) for +: "
                    f"{type(self).__name__!r} and {type(other).__name__!r}")
  return NotImplemented

