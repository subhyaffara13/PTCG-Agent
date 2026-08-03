from typing import Any

def _calculate_max_shard_shapes(
    abstract_pytree: dict[str, Any], header: dict[str, Any]
) -> dict[np.dtype, list[int]]:
  """Calculates maximum shard shapes per dtype."""
  max_shard_shape_per_dtype = {}
  for name, _ in abstract_pytree.items():
    if name not in header:
      continue
    info = header[name]
    shape, dtype = _get_array_properties(info)
    current_shard_shape = _get_current_shard_shape(shape)

    if dtype not in max_shard_shape_per_dtype:
      max_shard_shape_per_dtype[dtype] = [1]

    max_shape = max_shard_shape_per_dtype[dtype]

    while len(max_shape) < len(current_shard_shape):
      max_shape.append(0)

    for i in range(1, len(current_shard_shape)):
      max_shape[i] = max(max_shape[i], current_shard_shape[i])
  return max_shard_shape_per_dtype

