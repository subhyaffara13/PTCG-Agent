
def _match_axes_jaxpr(f, store, axis_data, out_axes_dest, out_axes, trace, in_axes,
                      *in_vals):
  out_vals = f(trace, in_axes, *in_vals)
  out_axes = out_axes()
  out_axes_dest = [(None if src is None else 0)
                   if dst is zero_if_mapped else dst
                   for src, dst in unsafe_zip(out_axes, out_axes_dest)]
  if len(out_axes_dest) != len(out_axes):
    out_axis_dest, = out_axes_dest
    out_axes_dest = [out_axis_dest] * len(out_axes)
  out_vals = map(partial(matchaxis, axis_data), out_axes, out_axes_dest, out_vals)
  out_batched = [dst is not None for dst in out_axes_dest]
  store.store(out_batched)
  return out_vals

