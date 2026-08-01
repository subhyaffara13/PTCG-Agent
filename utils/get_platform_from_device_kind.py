
def get_platform_from_device_kind(device_kind) -> str:
  device_kind = device_kind.lower()
  if 'cpu' in device_kind:
    return 'cpu'
  elif 'tpu' in device_kind:
    return 'tpu'
  elif any(x in device_kind for x in ['nvidia', 'tesla', 'amd']):
    return 'gpu'
  else:
    raise ValueError(f'Got unexpected {device_kind=}')

