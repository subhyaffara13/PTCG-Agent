
def _unmap_shaped_array(
    size: int, axis: int | None, explicit_mesh_axis, aval: ShapedArray
    ) -> ShapedArray:
  if axis is None:
    return aval
  elif type(axis) is int:
    aval_s = aval.sharding
    sharding = aval_s.update(spec=aval_s.spec.update(partitions=tuple_insert(
        aval_s.spec.partitions, axis, explicit_mesh_axis)))
    return ShapedArray(tuple_insert(aval.shape, axis, size), aval.dtype,
                       weak_type=aval.weak_type, sharding=sharding,
                       manual_axis_type=aval.mat,
                       memory_space=aval.memory_space)
  else:
    raise TypeError(axis)

