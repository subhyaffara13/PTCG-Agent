
def _check_all_safe_to_cast(name: str, dtype: DTypeLike, *args):
  for arg in args:
    if not dtypes.safe_to_cast(arg, dtype):
      raise dtypes.TypePromotionError(f"In arguments to {name}, cannot safely cast argument of type {jnp.asarray(arg).dtype} to {dtype}")

