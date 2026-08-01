
def _different_device_order_reshard(
    x: array.ArrayImpl, target_sharding: NamedSharding, copy: ArrayCopySemantics
) -> array.ArrayImpl:
  x._check_if_deleted()
  inp_sharding = x.sharding
  assert isinstance(inp_sharding, NamedSharding)

  inp_device_list = inp_sharding._internal_device_list
  target_device_list = target_sharding._internal_device_list

  donate_argnums = 0 if copy == ArrayCopySemantics.DONATE_INPUT else None
  if inp_device_list == target_device_list:
    return api.jit(_device_put_reshard, out_shardings=target_sharding,
                   donate_argnums=donate_argnums)(x)

  if inp_sharding.is_fully_replicated:
    logical_device_ids = None
  else:
    logical_device_ids = _cached_logical_device_ids(
        inp_device_list, target_device_list,
    )

  new_mesh = Mesh(
      target_sharding.mesh.devices.reshape(inp_sharding.mesh.axis_sizes),
      inp_sharding.mesh.axis_names)
  new_s = NamedSharding(
      new_mesh, inp_sharding.spec, memory_kind=target_sharding.memory_kind,
      _logical_device_ids=logical_device_ids)
  new_x = xc.reorder_shards(x, new_s, ArrayCopySemantics.REUSE_INPUT)
  return api.jit(_device_put_reshard, out_shardings=target_sharding,
                donate_argnums=donate_argnums)(new_x)

