
def _splitaxis(axis, factor, x):
  new_shape = list(x.shape)
  assert new_shape[axis] % factor == 0, (new_shape[axis], factor)
  new_shape[axis:axis+1] = [factor, new_shape[axis] // factor]
  return x.reshape(new_shape)

