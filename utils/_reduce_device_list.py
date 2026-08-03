from typing import Any, Callable

def _reduce_device_list(
    device_list: DeviceList,
) -> tuple[Callable[..., DeviceList], Any]:
  device_ids = [d.id for d in device_list]
  return _unreduce_device_list, (device_ids,)

