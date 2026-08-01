
def add_jaxvals(x: ArrayLike, y: ArrayLike) -> Array:
  from jax._src.hijax import HiType  # pyrefly: ignore[missing-import]
  ty = typeof(x)
  if isinstance(ty, HiType):
    return ty.vspace_add(x, y)
  x, y = core.auto_insert_reshard(x, y)
  return add_jaxvals_p.bind(x, y)

