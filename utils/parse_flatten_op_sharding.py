
def parse_flatten_op_sharding(
    hlo_sharding: xc.OpSharding | xc.HloSharding,
    mesh: Mesh | AbstractMesh) -> Sequence[PartitionSpec]:
  if isinstance(hlo_sharding, xc.OpSharding):
    hlo_sharding = xc.HloSharding.from_proto(hlo_sharding)
  if hlo_sharding.tuple_elements():
    out: list[PartitionSpec] = []
    for s in hlo_sharding.tuple_elements():
      out.extend(parse_flatten_op_sharding(s, mesh))
    return out
  elif hlo_sharding.is_replicated():
    return [PartitionSpec()]
  elif hlo_sharding.is_maximal() and mesh.size == 1:
    return [PartitionSpec()]
  elif hlo_sharding.is_tiled():
    mesh_shape = mesh.shape
    mesh_axis_order = unflatten_array(
        mesh.shape, hlo_sharding.tile_assignment_devices()
    )
    mesh_axis = iter(mesh_axis_order)
    shape = hlo_sharding.tile_assignment_dimensions()
    partitions = []
    for dim_size in shape:
      dim_partitions = []
      while dim_size > 1:
        axis = next(mesh_axis)
        axis_size = mesh_shape[axis]
        quotient, remainder = divmod(dim_size, axis_size)
        if remainder != 0:
          raise jsharding.IndivisibleError(
              f'{shape=} is incompatible with {mesh_shape=}: '
              f'{dim_size=} is not divisible by {axis_size=}.')
        dim_size = quotient
        dim_partitions.append(axis)
      partitions.append(tuple(dim_partitions))
    if len(hlo_sharding.subgroup_types()) > 1:
      raise NotImplementedError(
          'Unhandled HloSharding type. Please open a bug report!'
      )
    if hlo_sharding.replicate_on_last_tile_dim():
      partitions = partitions[:-1]
    while partitions and partitions[-1] == ():
      partitions.pop()
    return [PartitionSpec(*partitions)]
  else:
    raise AssertionError("Unhandled OpSharding type. Please open a bug report!")

