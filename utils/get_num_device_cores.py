
def get_num_device_cores() -> int:
  if abstract_device := mesh_lib.get_abstract_mesh().abstract_device:
    return abstract_device.num_cores
  return pxla.get_default_device().num_cores

