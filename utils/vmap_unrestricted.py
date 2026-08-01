
def vmap_unrestricted(f: lu.WrappedFun, *args, in_axes, axis_name, axis_size):
  axis_data = batching.AxisData(axis_name, axis_size, None, None)
  tag = core.TraceTag()
  f, out_axes = batching.batch_subtrace(f, tag, axis_data, in_axes)
  outs = f.call_wrapped(*args)
  return outs, out_axes()

