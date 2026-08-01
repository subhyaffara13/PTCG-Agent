
def _absolute_dims(ndim, dims):
  return tuple(ndim + dim if dim < 0 else dim for dim in dims)

