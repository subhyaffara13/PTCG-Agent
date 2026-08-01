
def untile_aval_nd(axis_sizes, out_axes: ArrayMapping, aval):
  assert isinstance(aval, ShapedArray)
  shape = list(aval.shape)
  for name, axis in out_axes.items():
    shape[axis] *= axis_sizes[name]
  return aval.update(shape=tuple(shape))

