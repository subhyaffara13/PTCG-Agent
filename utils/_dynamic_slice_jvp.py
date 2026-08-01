
def _dynamic_slice_jvp(primals, tangents, *, slice_sizes):
  tangent_out = tangents[0]
  if type(tangent_out) is not ad_util.Zero:
    tangent_out = dynamic_slice_p.bind(tangent_out, *primals[1:], slice_sizes=slice_sizes)
  return dynamic_slice_p.bind(primals[0], *primals[1:], slice_sizes=slice_sizes), tangent_out

