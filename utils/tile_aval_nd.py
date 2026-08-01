
def tile_aval_nd(axis_sizes, in_axes: ArrayMapping, aval):
  assert isinstance(aval, ShapedArray)
  shape = list(aval.shape)
  for name, axis in in_axes.items():
    assert shape[axis] % axis_sizes[name] == 0
    shape[axis] //= axis_sizes[name]
  return aval.update(shape=tuple(shape))

