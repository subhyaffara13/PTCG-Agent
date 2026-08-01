
def _map_shaped_array(
    size: int, axis: int | None, aval: ShapedArray) -> ShapedArray:
  assert axis is None or aval.shape[axis] == size
  if axis is None:
    return aval
  aval_s = aval.sharding
  sharding = aval_s.update(
      spec=aval_s.spec.update(partitions=tuple_delete(aval_s.spec.partitions, axis)))
  return ShapedArray(tuple_delete(aval.shape, axis), aval.dtype,
                     weak_type=aval.weak_type, sharding=sharding,
                     manual_axis_type=aval.mat, memory_space=aval.memory_space)

