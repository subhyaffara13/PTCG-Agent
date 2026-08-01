
def empty_like_aval(aval):
  from jax._src.hijax import HiType  # pyrefly: ignore[missing-import]
  if isinstance(aval, HiType):
    return aval.raise_val(*map(empty_like_aval, aval.lo_ty()))
  return aval_empty_likers[type(aval)](aval)

