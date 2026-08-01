
def _check_string_compatible_sharding(s):
  """Checks if target devices are compatible with string arrays."""
  if isinstance(s, xc.Device) and s.device_kind == "cpu":
    return
  if (isinstance(s, Sharding)
      and s._internal_device_list[0].device_kind == "cpu"):
    return
  raise TypeError(
      "String arrays can only be sharded to CPU devices. Received"
      f" unsupported device or sharding: {s}")

