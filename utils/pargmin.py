
def pargmin(x, axis_name):
  if isinstance(axis_name, (tuple, list)):
    raise TypeError(f"pargmin only accepts a single axis, got {axis_name}")
  return _axis_index_of_val(x, pmin(x, axis_name), axis_name)

