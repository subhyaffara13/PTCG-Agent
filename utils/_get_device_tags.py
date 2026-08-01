
def _get_device_tags():
  """returns a set of tags defined for the device under test"""
  if is_device_rocm():
    return {device_under_test(), "rocm"}
  elif is_device_cuda():
    return {device_under_test(), "cuda"}
  else:
    return {device_under_test()}

