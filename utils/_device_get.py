
def _device_get(x):
  if isinstance(x, core.Tracer):
    return x

  # Extended dtypes dispatch via their device_get rule.
  if isinstance(x, basearray.Array) and dtypes.issubdtype(x.dtype, dtypes.extended):
    bufs, tree = tree_util.dispatch_registry.flatten(x)
    return tree.unflatten(device_get(bufs))

  # Other types dispatch via their __array__ method.
  try:
    toarray = x.__array__
  except AttributeError:
    return x
  else:
    return toarray()

