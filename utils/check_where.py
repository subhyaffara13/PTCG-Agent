
def check_where(name: str, where: ArrayLike | None) -> Array | None:
  if where is None:
    return where
  where = ensure_arraylike(name, where)
  if where.dtype != bool:
    raise ValueError(
      f"jnp.{name}: where must be None or a boolean array; got {where.dtype=}."
    )
  return where

