
def _all_to_all_batcher(vals_in, dims_in, *, axis_name, split_axis, concat_axis, axis_index_groups,
                        tiled):
  x, = vals_in
  d, = dims_in
  result = all_to_all_p.bind(
      x,
      axis_name=axis_name,
      split_axis=split_axis + (d <= split_axis),
      concat_axis=concat_axis + (d <= concat_axis),
      axis_index_groups=axis_index_groups,
      tiled=tiled,
  )
  return result, d

