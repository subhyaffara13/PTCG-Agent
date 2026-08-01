
def unmapped_aval(size: AxisSize, axis: int | None,
                  aval: AbstractValue, explicit_mesh_axis=None) -> AbstractValue:
  from jax._src.hijax import HiType  # pyrefly: ignore[missing-import]
  if isinstance(aval, HiType):
    return aval.inc_rank(size, axis)  # pyrefly: ignore[bad-argument-type]
  _, handler = aval_mapping_handlers.get(type(aval), (None, None))
  if handler is not None:
    return handler(size, axis, explicit_mesh_axis, aval)
  else:
    raise TypeError(f"no unmapping handler for {aval} of type {type(aval)}")

