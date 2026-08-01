
def mapped_aval(size: AxisSize, axis, aval: AbstractValue) -> AbstractValue:
  from jax._src.hijax import HiType  # pyrefly: ignore[missing-import]
  if isinstance(aval, HiType):
    return aval.dec_rank(size, axis)  # pyrefly: ignore[bad-argument-type]
  handler, _ = aval_mapping_handlers.get(type(aval), (None, None))
  if handler is not None:
    return handler(size, axis, aval)
  else:
    raise TypeError(f"no mapping handler for {aval} of type {type(aval)}")

