
def physical_hlo_sharding(aval, hlo_sharding: xc.HloSharding) -> xc.HloSharding:
  elt_aval = core.physical_element_aval(aval.dtype)
  new_op_sharding = hlo_sharding.to_proto().clone()
  partitions, num_replicas = get_num_ways_dim_sharded(hlo_sharding)
  suffix = [] if num_replicas == 1 else [num_replicas]
  tad = partitions + [1] * elt_aval.ndim + suffix
  new_op_sharding.tile_assignment_dimensions = tad
  return xc.HloSharding.from_proto(new_op_sharding)

