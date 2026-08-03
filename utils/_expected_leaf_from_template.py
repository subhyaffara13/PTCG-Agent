from typing import Any

def _expected_leaf_from_template(value: Any) -> _ExpectedLeaf | None:
  """Returns expected shape/dtype based on a restore spec template leaf."""
  if isinstance(value, (jax.Array, jax.ShapeDtypeStruct)):
    return _ExpectedLeaf(tuple(value.shape), value.dtype)
  if isinstance(value, type_handlers.ArrayRestoreArgs):
    shape = None
    if value.global_shape is not None:
      shape = tuple(value.global_shape)
    return _ExpectedLeaf(shape, value.dtype)
  shape = getattr(value, 'shape', None)
  dtype = getattr(value, 'dtype', None)
  if shape is not None or dtype is not None:
    return _ExpectedLeaf(None if shape is None else tuple(shape), dtype)
  return None

