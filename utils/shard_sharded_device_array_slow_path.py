
def shard_sharded_device_array_slow_path(x, devices, indices, sharding):
  candidates = defaultdict(list)
  bufs = [buf.data for buf in x.addressable_shards]
  arr_indices = tuple(x.sharding.devices_indices_map(x.shape).values())
  for buf, idx in safe_zip(bufs, arr_indices):
    candidates[hashed_index(idx)].append(buf)

  bufs = []
  for idx, device in safe_zip(indices, devices):
    # Look up all buffers that contain the correct slice of the logical array.
    candidates_list = candidates[hashed_index(idx)]
    if not candidates_list:
      return pxla.shard_args([sharding], [None],
                             [xc.ArrayCopySemantics.REUSE_INPUT], [x._value],
                             canonicalize=False)[0]
    # Try to find a candidate buffer already on the correct device,
    # otherwise copy one of them.
    for buf in candidates_list:
      if buf.devices() == {device}:
        bufs.append(buf)
        break
    else:
      bufs.append(candidates_list[-1])
  return pxla.batched_device_put(x.aval, sharding, bufs, devices)

