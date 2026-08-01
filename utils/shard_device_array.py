
def shard_device_array(x, devices, indices, sharding):
  start_indices, limit_indices, removed_dims = unzip3(
      as_slice_indices(x, idx) for idx in indices)
  if sharding.is_fully_replicated:
    shards = [x] * len(devices)
  else:
    # TODO(yashkatariya): Maybe this should be set when we call the handler in
    # InputsHandler.__call__?
    with (_internal_use_concrete_mesh(empty_concrete_mesh),
          use_abstract_mesh(empty_abstract_mesh)):
      shards = x._multi_slice(start_indices, limit_indices, removed_dims)
  aval = core.shaped_abstractify(x)
  return pxla.batched_device_put(aval, sharding, shards, devices)

