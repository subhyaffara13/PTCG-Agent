
def _all_gather_invariant_lowering(
    ctx, x, *, all_gather_dimension, axis_name, axis_size, tiled, platform=None):
  return _all_gather_lowering(
      ctx, x, all_gather_dimension=all_gather_dimension, axis_name=axis_name,
      axis_index_groups=None, axis_size=axis_size, tiled=tiled,
      platform=platform)

