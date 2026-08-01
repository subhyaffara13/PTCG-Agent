
def zeros_like_aval(aval: core.AbstractValue) -> Array:
  from jax._src.hijax import HiType  # pyrefly: ignore[missing-import]
  if isinstance(aval, HiType):
    return aval.vspace_zero()
  return aval_zeros_likers[type(aval)](aval)

