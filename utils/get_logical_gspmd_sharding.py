
def get_logical_gspmd_sharding(logical_shape, dtype, phys_sharding):
  elt_aval = core.physical_element_aval(dtype)
  phys_hlo_sharding = phys_sharding._to_xla_hlo_sharding(
      len(logical_shape) + elt_aval.ndim)
  partitions, num_replicas = get_num_ways_dim_sharded(phys_hlo_sharding)
  suffix = [] if num_replicas == 1 else [num_replicas]
  # Create logical sharding by cutting off the replicated trailing dims.
  logical_op_sharding = phys_hlo_sharding.to_proto().clone()
  tad = partitions[:-elt_aval.ndim] + suffix
  logical_op_sharding.tile_assignment_dimensions = tad
  return GSPMDSharding(phys_sharding._internal_device_list,
                       xc.HloSharding.from_proto(logical_op_sharding))

