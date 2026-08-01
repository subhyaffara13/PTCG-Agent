
def _supports_buffer_protocol(obj):
  try:
    memoryview(obj)
  except TypeError:
    return False
  else:
    return True

