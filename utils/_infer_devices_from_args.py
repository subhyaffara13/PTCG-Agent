
def _infer_devices_from_args(args: Sequence[Any]) -> xc.DeviceList | None:
  """Returns a representative device list from function call arguments."""
  device_list_set: set[xc.DeviceList] = set()
  for x in args:
    sharding = getattr(x, "sharding", None)
    if sharding is not None:
      device_list_set.add(x.sharding._internal_device_list)
  if not device_list_set:
    return None
  if len(device_list_set) != 1:
    raise ValueError(
        "All arguments must use the same device list, but got"
        f" multiple device lists: {device_list_set}."
    )
  return device_list_set.pop()

