
def _operator_ne(self, other):
  m = getattr(other, '__jax_array__', None)
  if m is not None:
    other = m()
  if isinstance(other, _accepted_binop_types):
    return ufuncs.not_equal(self, cast(ArrayLike, other))
  # Explicitly reject non-array inputs to avoid Python returning scalar True.
  # Avoid isinstance so as to not catch subclasses like NamedTuple.
  # TODO(jakevdp): raise for *all* non-array types.
  if type(other) in (dict, list, set, tuple):
    raise TypeError(f"unsupported operand type(s) for ==: "
                    f"{type(self).__name__!r} and {type(other).__name__!r}")
  return NotImplemented

