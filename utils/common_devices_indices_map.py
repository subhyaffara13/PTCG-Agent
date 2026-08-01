
def common_devices_indices_map(
    s: Sharding, global_shape: Shape) -> Mapping[Device, Index]:
  s.shard_shape(global_shape)  # raises a good error message
  hlo_sharding = s._to_xla_hlo_sharding(len(global_shape))
  if (xc.OpSharding.Type.UNREDUCED in hlo_sharding.subgroup_types() or
      hlo_sharding.is_unreduced()):
    raise NotImplementedError(
        "device_indices_map doesn't work with unreduced. Please file a bug at"
        ' https://github.com/jax-ml/jax/issues')
  indices = op_sharding_to_indices(hlo_sharding, global_shape,
                                   len(s._device_assignment))
  return dict(safe_zip(s._device_assignment, indices))

