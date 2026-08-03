from typing import Any

def is_supported_abstract_leaf(x: Any) -> bool:
  """Returns True if the given object is a supported AbstractLeaf."""
  if x is types.PLACEHOLDER:
    return True

  if isinstance(x, type):
    if protocol_utils.is_subclass_protocol(x, array_types.AbstractArray):
      return True
    if protocol_utils.is_subclass_protocol(x, array_types.AbstractShardedArray):
      return True
    return issubclass(x, typing.get_args(array_types.AbstractScalar) + (str,))

  if protocol_utils.is_subclass_protocol(type(x), array_types.AbstractArray):
    return True
  if protocol_utils.is_subclass_protocol(
      type(x), array_types.AbstractShardedArray
  ):
    return True
  return isinstance(x, (array_types.AbstractScalar, str))

