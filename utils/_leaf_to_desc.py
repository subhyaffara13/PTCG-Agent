
def _leaf_to_desc(leaf) -> str:
  if leaf is None:
    return "null"
  elif _is_array_like(leaf):
    return _ARRAY_TYPE_FORMAT.format(
        dtype=leaf.dtype.name, shape=", ".join(map(str, leaf.shape)))
  else:
    return type(leaf).__name__

