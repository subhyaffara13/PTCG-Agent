
def _device_put_eager_rule(mesh, *xs, srcs, devices, copy_semantics):
  del mesh, srcs, copy_semantics
  for device in devices:
    if device is not None:
      raise ValueError("device_put with explicit device not allowed within "
                       f"shard_map-decorated functions, but got device {device}")
  return xs

