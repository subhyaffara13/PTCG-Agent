
def _constant_reduction(prim, axis_data, arg, axes, axis_index_groups):
  assert axis_data.name in axes
  if axis_index_groups: raise NotImplementedError
  new_axes = tuple(n for n in axes if n != axis_data.name)
  if new_axes:
    arg = (prim.bind(arg, axes=new_axes) if prim is psum_invariant_p else
           prim.bind(arg, axes=new_axes, axis_index_groups=axis_index_groups))
  if prim is psum_p:
    out = lax._const(arg, axis_data.size) * arg
  elif prim in (pmin_p, pmax_p):
    out = arg
  else:
    raise Exception(f"Unrecognized reducer: {prim}")
  return out, None

