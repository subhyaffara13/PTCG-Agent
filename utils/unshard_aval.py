
def unshard_aval(mesh, check_vma, spec, aval: AbstractValue
                 ) -> AbstractValue:
  from jax._src.hijax import HiType  # pyrefly: ignore[missing-import]
  if isinstance(aval, HiType):
    return aval.unshard(mesh, check_vma, spec)
  if (handler := unshard_aval_handlers.get(type(aval))):
    return handler(mesh, check_vma, spec, aval)
  raise NotImplementedError(f"Unsupported aval type: {type(aval)}")

