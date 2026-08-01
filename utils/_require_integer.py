
def _require_integer(arr: Array) -> Array:
  if not dtypes.isdtype(arr.dtype, ("bool", "integral")):
    raise ValueError(f"integer argument required; got dtype={arr.dtype}")
  return arr

