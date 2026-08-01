
def _layout_constraint_batcher(axis_data, vals_in, dims_in, layout):
  x, = vals_in
  d, = dims_in
  if d is None:
    return layout_constraint_p.bind(x, layout=layout), None
  vmapped_layout = get_layout_for_vmap(d, layout)
  y = layout_constraint_p.bind(x, layout=vmapped_layout)
  return y, d

