
def ensure_shaped(*avals: core.AbstractValue) -> tuple[core.ShapedArray | state.AbstractRef, ...]:
  """Cast all inputs to ShapedArray with a runtime instance check."""
  if any(not isinstance(aval, (core.ShapedArray, state.AbstractRef)) for aval in avals):
    raise ValueError(f"Expected ShapedArray; got {[type(aval) for aval in avals]}")
  return tuple(cast(core.ShapedArray | state.AbstractRef, aval) for aval in avals)

