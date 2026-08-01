
def _axis_read(axis_names, axis_name):
  try:
    return max(i for i, name in enumerate(axis_names) if name == axis_name)
  except ValueError:
    raise NameError(f"unbound axis name: {axis_name}") from None

