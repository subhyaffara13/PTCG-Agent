
def iterated_vmap_binary_bcast(shape1, shape2, f):
  ndim1, ndim2 = len(shape1), len(shape2)
  if ndim1 == ndim2 == 0:
    return f
  if 0 in [ndim1, ndim2]:
    if ndim1 == 0:
      return lambda x, y: iterated_vmap_unary(ndim2, lambda y: f(x, y))(y)
    else:
      return lambda x, y: iterated_vmap_unary(ndim1, lambda x: f(x, y))(x)
  assert len(shape1) == len(shape2)
  for sz1, sz2 in reversed(zip(shape1, shape2)):
    if sz1 == sz2:
      f = api.vmap(f, out_axes=0)
    else:
      assert sz1 == 1 or sz2 == 1, (sz1, sz2)
      f = squeeze_vmap(f, sz1 == 1)
  return f

