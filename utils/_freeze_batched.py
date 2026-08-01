
def _freeze_batched(axis_data, vals_in, dims_in):
  ref, = vals_in
  dim, = dims_in
  return core.freeze_p.bind(ref), dim

