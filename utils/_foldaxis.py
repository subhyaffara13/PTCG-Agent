
def _foldaxis(axis, x):
  new_shape = list(x.shape)
  new_shape[axis:axis+2] = [x.shape[axis] * x.shape[axis + 1]]
  return x.reshape(new_shape)

