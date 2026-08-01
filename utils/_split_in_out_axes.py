
def _split_in_out_axes(xs: Mapping[CollectionFilter, Any]):
  unpack = lambda v: v.axis if isinstance(v, (In, Out)) else v
  in_axes = {k: unpack(v) for k, v in xs.items() if not isinstance(v, Out)}
  out_axes = {k: unpack(v) for k, v in xs.items() if not isinstance(v, In)}
  return in_axes, out_axes

