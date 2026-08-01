
def _array_shard_arg(xs, shardings, layouts, copy_semantics):
  util.test_event("_array_shard_arg")
  results = []
  batch_xs, batch_devs, batch_shardings, batch_indices = [], [], [], []
  batch_cs = []

  for i, (x, sharding, layout, cs) in enumerate(
      safe_zip(xs, shardings, layouts, copy_semantics)):
    x._check_if_deleted()
    try:
      same_sharding = _sharding_indices_and_eq(x.sharding, sharding, len(x.shape))
    except NotImplementedError:
      same_sharding = _fallback_check_via_indices(x.sharding, sharding, x.shape)
    same_layout = True if layout is None else x.format.layout == layout

    if not x.is_fully_addressable:
      if same_sharding and same_layout:
        results.append(x)
      else:
        raise NotImplementedError(
            "Cannot reshard an input that is not fully addressable")
    else:
      devices = sharding._internal_device_list.addressable_device_list
      if same_sharding and same_layout:
        # Add a placeholder result that will be filled in later.
        results.append(None)
        # Accumulate arguments to `batched_copy_array_to_devices_with_sharding`.
        batch_xs.append(x)
        batch_devs.append(devices)
        batch_shardings.append(sharding)
        batch_indices.append(i)
        batch_cs.append(cs)
      # Resharding starts here:
      elif not same_layout:
        results.append(api.device_put(x, Format(layout, sharding)))
      else:
        indices = sharding.addressable_devices_indices_map(x.shape).values()
        if x.sharding.num_devices == 1:
          results.append(shard_device_array(x, devices, indices, sharding))
        else:
          results.append(
              shard_sharded_device_array_slow_path(x, devices, indices, sharding))

  util.test_event("batched_copy_array")
  copy_outs = xc.batched_copy_array_to_devices_with_sharding(
      batch_xs, batch_devs, batch_shardings, batch_cs)
  for i, copy_out in safe_zip(batch_indices, copy_outs):
    assert results[i] is None
    results[i] = copy_out
  return results

