import re

def _desc_to_leaf(leaf_desc: str | None) -> str | None | jax.ShapeDtypeStruct:
  if leaf_desc is None:
    return None
  if not re.match(_ARRAY_TYPE_REGEX, leaf_desc):
    return leaf_desc
  shape_dtype_match = re.match(_ARRAY_TYPE_REGEX, leaf_desc)
  assert shape_dtype_match is not None
  dtype_str, shape_str = shape_dtype_match.groups()
  shape = [int(x.strip()) for x in shape_str.strip("]").strip().split(",")
            if len(x.strip()) > 0]
  return jax.ShapeDtypeStruct(shape, jax.numpy.dtype(dtype_str))

