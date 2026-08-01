
def _unpickle_named_sharding(mesh, spec, memory_kind, logical_device_ids):
  return NamedSharding(mesh, spec, memory_kind=memory_kind,
                       _logical_device_ids=logical_device_ids)

