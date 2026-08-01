
def _pvary_batcher(vals_in, dims_in, *, axes):
  if any(type(axis) is int for axis in axes):
    raise NotImplementedError
  (x,), (d,) = vals_in, dims_in
  y = core.pvary_p.bind(x, axes=axes)
  return y, d

