
def get_device_kind() -> str:
  if abstract_device := mesh_lib.get_abstract_mesh().abstract_device:
    return abstract_device.device_kind
  return pxla.get_default_device().device_kind

