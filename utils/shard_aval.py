
def shard_aval(mesh, manual_axes, check_vma, spec, aval: AbstractValue
               ) -> AbstractValue:
  from jax._src.hijax import HiType  # pyrefly: ignore[missing-import]
  if isinstance(aval, HiType):
    return aval.shard(mesh, manual_axes, check_vma, spec)
  if (handler := shard_aval_handlers.get(type(aval))):
    return handler(mesh, manual_axes, check_vma, spec, aval)
  raise NotImplementedError(f"Unsupported aval type: {type(aval)}")

