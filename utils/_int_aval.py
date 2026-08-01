
def _int_aval(value):
  if config.enable_x64.value:
    if value < _int64_min or value > _int64_max:
      raise OverflowError(f"Python int {value} too large to convert to int64")
    return _int64_aval
  else:
    if value < _int32_min or value > _int32_max:
      raise OverflowError(f"Python int {value} too large to convert to int32")
    return _int32_aval

