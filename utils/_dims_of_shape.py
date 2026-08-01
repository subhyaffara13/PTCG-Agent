
def _dims_of_shape(shape):
  """Converts `shape` to a tuple of dimensions."""
  if type(shape) in (list, tuple):
    return shape
  elif isinstance(shape, ScalarShape):
    return ()
  elif np.ndim(shape) == 0:
    return (shape,)
  else:
    raise TypeError(type(shape))

