
def _shard_np_array(xs, shardings, layouts, copy_semantics):
  results = []
  for x, sharding, layout in safe_zip(xs, shardings, layouts):
    devices = sharding._addressable_device_assignment
    if x.dtype == dtypes.float0:
      x = np.zeros(x.shape, dtype=np.dtype(bool))
    aval = core.shaped_abstractify(x)
    if layout is not None:
      results.append(api.device_put(x, Format(layout, sharding)))
    else:
      if sharding.is_fully_replicated:
        shards = [x] * len(devices)
      else:
        indices = tuple(sharding.addressable_devices_indices_map(x.shape).values())
        shards = [x[i] for i in indices]
      results.append(batched_device_put(aval, sharding, shards, devices))
  return results

