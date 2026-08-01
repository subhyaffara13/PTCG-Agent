
def _all_to_all_transpose_rule(
    cts, x, axis_name, split_axis, concat_axis, axis_index_groups, tiled
):
  return (all_to_all(
      cts,
      axis_name=axis_name,
      split_axis=concat_axis,
      concat_axis=split_axis,
      axis_index_groups=axis_index_groups,
      tiled=tiled),)

