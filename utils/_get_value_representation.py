from typing import Any

def _get_value_representation(x: Any) -> _ValueRepresentation:
  if isinstance(x, (int, float, bool, type(None))) or (
    isinstance(x, np.ndarray) and np.isscalar(x)
  ):
    return _ObjectRepresentation(x)
  elif isinstance(x, meta.Partitioned):
    return _PartitionedArrayRepresentation.from_partitioned(x)
  try:
    return _ArrayRepresentation.from_array(x)
  except:
    return _ObjectRepresentation(x)

