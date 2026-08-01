
def _dilate_shape(shape, dilation):
  """Utility function for computing the shape resulting from a dilation."""
  if not np.all(np.greater(dilation, 0)):
    msg = "All dilations must be positive, got {}."
    raise TypeError(msg.format(dilation))
  dilation = (1,) * (len(shape) - len(dilation)) + tuple(dilation)
  return tuple(map(core.dilate_dim, shape, dilation))

