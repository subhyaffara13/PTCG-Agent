
def check_replicated_trailing_dims(sharding: jsharding.Sharding,
                                   logical_shape, dtype):
  if isinstance(sharding, NamedSharding) and sharding.mesh._any_axis_manual:
    return
  phys_shape = core.physical_shape(logical_shape, dtype)
  hlo_s = sharding._to_xla_hlo_sharding(len(phys_shape))
  partitions, _ = get_num_ways_dim_sharded(hlo_s)
  num_trailing_dims = len(phys_shape) - len(logical_shape)
  if not all(i == 1 for i in partitions[-num_trailing_dims:]):
    raise AssertionError(
        "The trailing dims of extended dtypes should be replicated. Got"
        f" sharding: {sharding}, partitions: {partitions}, "
        f"num_trailing_dims: {num_trailing_dims}")

