
def _pbroadcast_transpose_rule(t, x, source, axis_name):
  is_source = axis_index(axis_name) == source
  tsum = psum(t, axis_name)
  return [lax.select(is_source, lax.full_like(t, tsum), lax.full_like(t, 0))]

