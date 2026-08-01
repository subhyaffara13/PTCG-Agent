
def format_shapes(d):
  """Returns a string representing the shapes of a dict of tensors."""
  if len(d) == 1:
    return str(list(d[min(d)].shape))
  else:
    return ", ".join(f"{key}: {list(value.shape)}" for key, value in d.items())

