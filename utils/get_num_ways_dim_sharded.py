
def get_num_ways_dim_sharded(hlo_sharding: xc.HloSharding
                             ) -> tuple[list[int], int]:
  assert not hlo_sharding.is_manual()
  if hlo_sharding.is_replicated():
    return [], 1
  if hlo_sharding.is_unreduced():
    return [], 1
  partitions = hlo_sharding.tile_assignment_dimensions()
  subgroup_types = hlo_sharding.subgroup_types()

  if subgroup_types == [xc.OpSharding.Type.REPLICATED]:
    return list(partitions[:-1]), partitions[-1]
  elif subgroup_types == [xc.OpSharding.Type.UNREDUCED]:
    return list(partitions[:-1]), 1
  elif set(subgroup_types) == {xc.OpSharding.Type.REPLICATED,
                               xc.OpSharding.Type.UNREDUCED}:
    replicated_loc = subgroup_types.index(xc.OpSharding.Type.REPLICATED)
    return list(partitions[:-2]), partitions[-2:][replicated_loc]
  elif hlo_sharding.replicate_on_last_tile_dim():
    return list(partitions[:-1]), partitions[-1]
  else:
    if subgroup_types:
      raise NotImplementedError(f"Unhandled OpSharding type: {hlo_sharding}. "
                                "Please open a bug report!")
    return list(partitions), 1

