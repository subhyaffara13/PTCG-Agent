
def _token_shard_arg(xs, shardings, layouts, copy_semantics):
  results = []
  for x, sharding, layout in safe_zip(xs, shardings, layouts):
    assert layout is None
    x.block_until_ready()
    x = np.array([], dtype=bool)
    aval = core.typeof(x)
    devices = sharding._addressable_device_assignment
    results.append(pxla.batched_device_put(
        aval, sharding, [x] * len(devices), devices))
  return results

