
def batch_jaxpr_axes(closed_jaxpr, axis_data, in_axes, out_axes_dest):
  return _batch_jaxpr_axes(closed_jaxpr, axis_data, tuple(in_axes), tuple(out_axes_dest))

